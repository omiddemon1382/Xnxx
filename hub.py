# hub.py — پنل مادر (Master Hub) · تجمیع کانفیگ‌های چند پنل در یک ساب واحد
# ══════════════════════════════════════════════════════════════════════════════
#  ─ هر پنل ورکر یک EXPORT_TOKEN دارد و endpoint /api/export/links می‌دهد
#  ─ این ماژول ورکرها را مدیریت می‌کند، به‌صورت خودکار سینک می‌کند و
#    یک ساب واحد در /sub-hub/{key} می‌سازد که همه کانفیگ‌های همه پنل‌ها را دارد
#  ─ state خودش را در فایل جدا hub_state.json نگه می‌دارد (بدون دست‌زدن به state اصلی)
#  ─ فقط روی پنل مادر قرار می‌گیرد (main.py خودش تشخیص می‌دهد)
# ══════════════════════════════════════════════════════════════════════════════

import asyncio
import base64
import json
import os
import secrets
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import quote

import aiofiles
import httpx
from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, Response, RedirectResponse

from main import (
    require_auth, logger, DATA_DIR,
    LINKS, LINKS_LOCK,
    is_link_allowed, vless_link_for_link, get_host, fmt_bytes,
)

router = APIRouter()

HUB_FILE = DATA_DIR / "hub_state.json"
HUB_LOCK = asyncio.Lock()
SAVE_HUB_LOCK = asyncio.Lock()

WORKERS: dict = {}        # wid → {name,url,token,active,include,created_at,last_sync,last_error,links_count}
REMOTE_LINKS: dict = {}   # "{wid}:{uuid}" → {label, vless_link, active, worker_name, ...}
HUB_KEY: str = secrets.token_urlsafe(16)

AUTO_SYNC_SECONDS = max(30, int(os.environ.get("HUB_SYNC_SECONDS", "300")))  # پیش‌فرض ۵ دقیقه

# مدت کش پاسخ ساب (ثانیه) — جلوی فشار مکرر روی ساب‌گیری را می‌گیرد
SUB_CACHE_TTL = 60
_sub_cache: dict = {"key": None, "at": 0.0, "content": None}


# ── Persistence ───────────────────────────────────────────────────────────────
async def load_hub_state():
    global WORKERS, REMOTE_LINKS, HUB_KEY
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        if HUB_FILE.exists():
            async with aiofiles.open(HUB_FILE, "r", encoding="utf-8") as f:
                data = json.loads(await f.read())
            WORKERS.update(data.get("workers", {}))
            REMOTE_LINKS.update(data.get("remote_links", {}))
            if data.get("hub_key"):
                HUB_KEY = data["hub_key"]
            logger.info(f"Hub state loaded: {len(WORKERS)} workers, {len(REMOTE_LINKS)} remote links")
    except Exception as e:
        logger.warning(f"Hub state load failed: {e}")


async def save_hub_state():
    async with SAVE_HUB_LOCK:
        try:
            DATA_DIR.mkdir(parents=True, exist_ok=True)
            data = {
                "workers": dict(WORKERS),
                "remote_links": dict(REMOTE_LINKS),
                "hub_key": HUB_KEY,
                "saved_at": datetime.now().isoformat(),
            }
            tmp = HUB_FILE.with_suffix(".tmp")
            async with aiofiles.open(tmp, "w", encoding="utf-8") as f:
                await f.write(json.dumps(data, ensure_ascii=False, indent=2))
            tmp.replace(HUB_FILE)
        except Exception as e:
            logger.warning(f"Hub state save failed: {e}")


# ── Sync engine ───────────────────────────────────────────────────────────────
def _normalize_url(url: str) -> str:
    url = (url or "").strip().rstrip("/")
    if url and not url.startswith(("http://", "https://")):
        url = "https://" + url
    return url


async def sync_worker(wid: str) -> dict:
    """کانفیگ‌های یک ورکر را می‌کشد و لیست ریموت همان ورکر را کامل جایگزین می‌کند."""
    async with HUB_LOCK:
        w = WORKERS.get(wid)
    if not w:
        raise HTTPException(status_code=404, detail="worker not found")
    url = _normalize_url(w.get("url"))
    if not url:
        raise HTTPException(status_code=400, detail="worker url خالی است")
    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(25.0, connect=10.0)) as client:
            r = await client.get(f"{url}/api/export/links", params={"token": w.get("token", "")})
        if r.status_code != 200:
            raise RuntimeError(f"HTTP {r.status_code}")
        data = r.json()
        links = data.get("links", []) or []
        now_iso = datetime.now().isoformat()
        newmap = {}
        for l in links:
            if not l.get("uuid"):
                continue
            newmap[f"{wid}:{l['uuid']}"] = {
                "wid": wid,
                "uuid": l["uuid"],
                "label": l.get("label") or "",
                "vless_link": l.get("vless_link") or "",
                "active": bool(l.get("active")),
                "proxy_label": l.get("proxy_label"),
                "used_bytes": int(l.get("used_bytes") or 0),
                "limit_bytes": int(l.get("limit_bytes") or 0),
                "expires_at": l.get("expires_at"),
                "worker_name": w.get("name") or wid[:8],
                "synced_at": now_iso,
            }
        async with HUB_LOCK:
            # کانفیگ‌های قدیمی همین ورکر که دیگر سمت ورکر نیستند حذف می‌شوند
            for k in [k for k in list(REMOTE_LINKS) if k.startswith(wid + ":")]:
                REMOTE_LINKS.pop(k, None)
            REMOTE_LINKS.update(newmap)
            w["last_sync"] = now_iso
            w["last_error"] = None
            w["links_count"] = len(newmap)
        asyncio.create_task(save_hub_state())
        _invalidate_sub_cache()
        return {"ok": True, "wid": wid, "name": w.get("name"), "links": len(newmap)}
    except Exception as e:
        async with HUB_LOCK:
            w["last_error"] = str(e)[:200]
        asyncio.create_task(save_hub_state())
        return {"ok": False, "wid": wid, "name": w.get("name"), "error": str(e)[:200]}


async def sync_all_workers() -> list:
    async with HUB_LOCK:
        ids = [wid for wid, w in WORKERS.items() if w.get("active", True)]
    if not ids:
        return []
    results = await asyncio.gather(*(sync_worker(i) for i in ids), return_exceptions=True)
    out = []
    for r in results:
        if isinstance(r, Exception):
            out.append({"ok": False, "error": str(r)})
        else:
            out.append(r)
    return out


# سینک خودکار پس‌زمینه (lazy-start با اولین درخواست)
_sync_task: asyncio.Task | None = None


def ensure_hub_sync():
    global _sync_task
    if _sync_task is None or _sync_task.done():
        _sync_task = asyncio.create_task(_hub_sync_loop())


async def _hub_sync_loop():
    await asyncio.sleep(3)   # اولین سینک کوتاه بعد از استارت
    while True:
        try:
            res = await sync_all_workers()
            if res:
                logger.info("Hub auto-sync: " + ", ".join(
                    f"{r.get('name','?')}={'OK' if r.get('ok') else 'ERR'}" for r in res))
        except Exception as e:
            logger.warning(f"Hub auto-sync error: {e}")
        await asyncio.sleep(AUTO_SYNC_SECONDS)


# ── Sub cache ─────────────────────────────────────────────────────────────────
def _invalidate_sub_cache():
    _sub_cache["key"] = None


# ── Workers API ───────────────────────────────────────────────────────────────
def _w_public(w: dict) -> dict:
    return {k: v for k, v in w.items() if k != "token"} | {
        "token_set": bool(w.get("token")),
        "token_tail": (w.get("token") or "")[-4:],
    }


@router.post("/api/hub/workers")
async def hub_add_worker(request: Request, _=Depends(require_auth)):
    ensure_hub_sync()
    body = await request.json()
    url = _normalize_url(body.get("url"))
    token = str(body.get("token") or "").strip()
    name = (str(body.get("name") or "").strip() or f"ورکر-{secrets.token_hex(2)}")[:60]
    if not url:
        raise HTTPException(status_code=400, detail="آدرس ورکر الزامی است")
    if not token:
        raise HTTPException(status_code=400, detail="توکن EXPORT_TOKEN ورکر الزامی است")
    wid = secrets.token_urlsafe(8)
    async with HUB_LOCK:
        # جلوگیری از ورکر تکراری (همان URL)
        for existing in WORKERS.values():
            if _normalize_url(existing.get("url")) == url:
                raise HTTPException(status_code=400, detail="این ورکر قبلاً اضافه شده")
        WORKERS[wid] = {
            "name": name, "url": url, "token": token,
            "active": True, "include": True,
            "created_at": datetime.now().isoformat(),
            "last_sync": None, "last_error": None, "links_count": 0,
        }
    asyncio.create_task(save_hub_state())
    res = await sync_worker(wid)   # اولین سینک فوری
    return {"wid": wid, **_w_public(WORKERS[wid]), "first_sync": res}


@router.get("/api/hub/workers")
async def hub_list_workers(_=Depends(require_auth)):
    ensure_hub_sync()
    async with HUB_LOCK:
        snap = {wid: dict(w) for wid, w in WORKERS.items()}
    out = []
    for wid, w in snap.items():
        p = _w_public(w)
        p["wid"] = wid
        out.append(p)
    out.sort(key=lambda x: x.get("created_at") or "", reverse=True)
    return {"workers": out}


@router.patch("/api/hub/workers/{wid}")
async def hub_edit_worker(wid: str, request: Request, _=Depends(require_auth)):
    body = await request.json()
    async with HUB_LOCK:
        w = WORKERS.get(wid)
        if not w:
            raise HTTPException(status_code=404, detail="worker not found")
        if "name" in body:
            w["name"] = (str(body["name"]).strip() or w["name"])[:60]
        if "url" in body and str(body["url"]).strip():
            w["url"] = _normalize_url(body["url"])
        if "token" in body and str(body["token"]).strip():
            w["token"] = str(body["token"]).strip()
        if "active" in body:
            w["active"] = bool(body["active"])
        if "include" in body:
            w["include"] = bool(body["include"])
    asyncio.create_task(save_hub_state())
    _invalidate_sub_cache()
    return {"ok": True}


@router.delete("/api/hub/workers/{wid}")
async def hub_del_worker(wid: str, _=Depends(require_auth)):
    async with HUB_LOCK:
        if wid not in WORKERS:
            raise HTTPException(status_code=404, detail="worker not found")
        name = WORKERS[wid].get("name", wid)
        del WORKERS[wid]
        for k in [k for k in list(REMOTE_LINKS) if k.startswith(wid + ":")]:
            REMOTE_LINKS.pop(k, None)
    asyncio.create_task(save_hub_state())
    _invalidate_sub_cache()
    return {"ok": True, "deleted": wid, "name": name}


@router.post("/api/hub/workers/{wid}/sync")
async def hub_sync_one(wid: str, _=Depends(require_auth)):
    ensure_hub_sync()
    return await sync_worker(wid)


@router.post("/api/hub/sync-all")
async def hub_sync_all(_=Depends(require_auth)):
    ensure_hub_sync()
    results = await sync_all_workers()
    return {"ok": True, "results": results}


# ── Overview + merged links ───────────────────────────────────────────────────
@router.get("/api/hub/overview")
async def hub_overview(request: Request, _=Depends(require_auth)):
    ensure_hub_sync()
    async with HUB_LOCK:
        workers = [_w_public(dict(w)) | {"wid": wid} for wid, w in WORKERS.items()]
        remote = {k: dict(v) for k, v in REMOTE_LINKS.items()}
    workers.sort(key=lambda x: x.get("created_at") or "", reverse=True)
    async with LINKS_LOCK:
        local_count = sum(1 for l in LINKS.values() if is_link_allowed(l))
    return {
        "workers": workers,
        "remote_links_count": sum(1 for l in remote.values() if l.get("active")),
        "local_links_count": local_count,
        "sub_url": f"https://{get_host(request)}/sub-hub/{HUB_KEY}",
        "auto_sync_seconds": AUTO_SYNC_SECONDS,
    }


@router.get("/api/hub/links")
async def hub_links_list(_=Depends(require_auth)):
    ensure_hub_sync()
    async with HUB_LOCK:
        remote = [dict(v) for v in REMOTE_LINKS.values()]
    remote.sort(key=lambda x: (x.get("worker_name") or "", x.get("label") or ""))
    return {"links": remote}


# ── ساب واحد (عمومی) ──────────────────────────────────────────────────────────
def _retitle(base_link: str, remark: str) -> str:
    """remark آخر لینک را عوض می‌کند و بقیه لینک دست‌نخورده می‌ماند."""
    return base_link.split("#", 1)[0] + "#" + quote(remark)


def _build_merged_sub(host: str) -> str:
    lines = []
    # ۱) کانفیگ‌های محلی خود پنل مادر
    async_lock_held = False
    # (این تابع sync است؛ snapshot را از بیرون می‌گیریم)
    return ""


@router.get("/sub-hub/{key}")
async def hub_merged_subscription(key: str, request: Request):
    if not secrets.compare_digest(key, HUB_KEY):
        raise HTTPException(status_code=404, detail="not found")

    # کش کوتاه برای جلوگیری از فشار مکرر
    now = time.monotonic()
    if (_sub_cache["content"] and _sub_cache["key"] == key
            and now - _sub_cache["at"] < SUB_CACHE_TTL):
        content = _sub_cache["content"]
    else:
        lines = []

        # ۱) کانفیگ‌های محلی خود پنل مادر
        host = get_host(request)
        async with LINKS_LOCK:
            local_snap = dict(LINKS)
        for uid, d in local_snap.items():
            if is_link_allowed(d):
                try:
                    base = vless_link_for_link(d, uid, host).split("#", 1)[0]
                    lines.append(base + "#" + quote(f"HUB · {d.get('label','')}"))
                except Exception:
                    pass

        # ۲) کانفیگ‌های ریموت ورکرها (فقط فعال + ورکر فعال و include)
        async with HUB_LOCK:
            workers_snap = {wid: dict(w) for wid, w in WORKERS.items()}
            remote = [dict(v) for v in REMOTE_LINKS.values()]
        for l in remote:
            w = workers_snap.get(l.get("wid") or "")
            if not w or not w.get("active", True) or not w.get("include", True):
                continue
            if not l.get("active") or not l.get("vless_link"):
                continue
            remark = f"{w.get('name','ورکر')} · {l.get('label','')}"
            lines.append(l["vless_link"].split("#", 1)[0] + "#" + quote(remark))

        content = base64.b64encode("\n".join(lines).encode()).decode()
        _sub_cache.update({"key": key, "at": now, "content": content})

    return Response(
        content=content, media_type="text/plain",
        headers={
            "profile-title": quote("OMID HUB"),
            "profile-update-interval": "6",
            "support-url": "https://t.me/omiddemon",
        },
    )


# ══════════════════════════════════════════════════════════════════════════════
# صفحه مدیریت HUB — /hub
# ══════════════════════════════════════════════════════════════════════════════
_HUB_PAGE = r"""<!DOCTYPE html>
<html lang="fa" dir="rtl"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>OMID HUB · مدیریت چند‌پنلی</title>
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;600;700;800&family=Cinzel:wght@700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#05070D;--card:rgba(14,18,30,.8);--bord:rgba(217,168,63,.2);--bordH:rgba(240,205,110,.5);--gold:#f3d98b;--gold2:#d9a83f;--t1:#F4EEDC;--t2:#C9B98F;--t3:#8D8368;--g:#7DDFA8;--r:#FF7B72}
body{font-family:'Vazirmatn',sans-serif;background:radial-gradient(800px 460px at 70% -10%,rgba(217,168,63,.08),transparent 60%),var(--bg);color:var(--t1);min-height:100vh;padding:26px 16px}
.wrap{max-width:880px;margin:0 auto}
h1{font-family:'Cinzel',serif;font-size:21px;letter-spacing:.14em;background:linear-gradient(135deg,#fdf6d8,#f3d98b 45%,#b07f22);-webkit-background-clip:text;background-clip:text;color:transparent;margin-bottom:4px}
.sub{font-size:11.5px;color:var(--t3);margin-bottom:20px}
.card{background:var(--card);border:1px solid var(--bord);border-radius:16px;padding:18px;margin-bottom:14px}
.ct{font-size:13px;font-weight:800;margin-bottom:12px;display:flex;align-items:center;gap:8px}
.ct i{color:var(--gold2)}
.ct .sp{margin-right:auto}
.subrow{display:flex;gap:8px;align-items:center;background:rgba(0,0,0,.35);border:1px solid var(--bord);border-radius:12px;padding:10px 12px;flex-wrap:wrap}
.subrow code{flex:1;min-width:220px;font-family:ui-monospace,monospace;font-size:11px;color:var(--gold);direction:ltr;text-align:left;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.btn{font-family:inherit;font-size:12px;font-weight:700;border-radius:10px;padding:9px 14px;cursor:pointer;border:none;display:inline-flex;align-items:center;gap:6px;transition:.15s}
.btn-p{background:linear-gradient(135deg,#f9ecc0,#eccb7a 46%,#c9962f);color:#2a1e05}
.btn-o{background:transparent;border:1px solid var(--bord);color:var(--t2)}
.btn-o:hover{border-color:var(--bordH);color:var(--gold)}
.btn:disabled{opacity:.5;cursor:not-allowed}
.wcard{display:flex;align-items:flex-start;gap:12px;flex-wrap:wrap;padding:13px 14px;border:1px solid var(--bord);border-radius:13px;margin-bottom:10px;background:rgba(10,14,24,.5)}
.wname{font-weight:800;font-size:13px}
.wurl{font-family:ui-monospace,monospace;font-size:10px;color:var(--t3);direction:ltr;margin-top:2px}
.chip{font-size:9.5px;padding:3px 9px;border-radius:20px;background:rgba(217,168,63,.08);border:1px solid var(--bord);color:var(--t2);display:inline-flex;align-items:center;gap:4px;font-weight:600}
.chip.ok{color:var(--g);border-color:rgba(62,207,142,.35)}
.chip.err{color:var(--r);border-color:rgba(229,72,77,.35)}
.chip.off{opacity:.55}
.wacts{margin-right:auto;display:flex;gap:6px;flex-wrap:wrap}
.bicon{width:30px;height:30px;border-radius:8px;background:rgba(217,168,63,.08);color:var(--gold);border:1px solid var(--bord);display:inline-flex;align-items:center;justify-content:center;cursor:pointer;font-size:14px}
.bicon.dan{color:var(--r);border-color:rgba(229,72,77,.3)}
.row{display:flex;gap:10px;flex-wrap:wrap}
.fg{display:flex;flex-direction:column;gap:5px;flex:1;min-width:170px}
.fg label{font-size:10px;color:var(--t3);font-weight:700}
.fg input{background:rgba(0,0,0,.42);border:1px solid var(--bord);border-radius:10px;padding:10px 12px;color:var(--t1);font-family:inherit;font-size:12px;outline:none;width:100%}
.fg input:focus{border-color:var(--bordH)}
#toasts{position:fixed;bottom:16px;left:16px;display:flex;flex-direction:column;gap:8px;z-index:99}
.toast{background:#0A0E18;border:1px solid var(--bordH);padding:10px 15px;border-radius:11px;font-size:12px;opacity:0;transform:translateY(10px);transition:.25s;max-width:420px}
.toast.show{opacity:1;transform:none}
.toast.err{border-color:rgba(229,72,77,.5);color:var(--r)}
.empty{padding:22px;text-align:center;color:var(--t3);font-size:12px}
.stats3{display:flex;gap:10px;flex-wrap:wrap;margin-top:12px}
.st3{flex:1;min-width:120px;background:rgba(0,0,0,.3);border:1px solid var(--bord);border-radius:12px;padding:11px;text-align:center}
.st3 b{display:block;font-size:19px;color:var(--gold)}
.st3 span{font-size:9.5px;color:var(--t3)}
a.back{display:inline-flex;align-items:center;gap:6px;color:var(--t2);font-size:12px;text-decoration:none;margin-bottom:14px}
a.back:hover{color:var(--gold)}
</style></head><body>
<div class="wrap">
  <a class="back" href="/dashboard"><i class="ti ti-arrow-right"></i>بازگشت به داشبورد</a>
  <h1>OMID HUB</h1>
  <div class="sub">مدیریت پنل‌های ورکر · ساب واحد همه کانفیگ‌ها · سینک خودکار هر <span id="syncInt">۵</span> دقیقه</div>

  <div class="card">
    <div class="ct"><i class="ti ti-link"></i>ساب واحد (همه کانفیگ‌های همه پنل‌ها)</div>
    <div class="subrow"><code id="subUrl">...</code><button class="btn btn-p" onclick="copySub()"><i class="ti ti-copy"></i>کپی</button><button class="btn btn-o" onclick="loadAll()"><i class="ti ti-refresh"></i></button></div>
    <div class="stats3">
      <div class="st3"><b id="stLocal">0</b><span>کانفیگ محلی مادر</span></div>
      <div class="st3"><b id="stRemote">0</b><span>کانفیگ از ورکرها</span></div>
      <div class="st3"><b id="stWorkers">0</b><span>ورکر فعال</span></div>
    </div>
    <div style="margin-top:10px;font-size:11px;color:var(--t3)">این لینک رو توی کلاینت (V2rayNG و...) اضافه کن — شامل همه کانفیگ‌های پنل مادر + همه ورکرهاست. هر کانفیگ از پروکسی پنل خودش خارج می‌شه.</div>
  </div>

  <div class="card">
    <div class="ct"><i class="ti ti-plus"></i>افزودن ورکر جدید</div>
    <div class="row">
      <div class="fg"><label>نام (مثلاً ترکیه)</label><input id="wName" placeholder="ترکیه"></div>
      <div class="fg"><label>آدرس پنل ورکر</label><input id="wUrl" dir="ltr" placeholder="https://xxxx.up.railway.app"></div>
      <div class="fg"><label>EXPORT_TOKEN ورکر</label><input id="wTok" dir="ltr" placeholder="توکن"></div>
    </div>
    <button class="btn btn-p" style="margin-top:12px" id="btnAdd" onclick="addWorker()"><i class="ti ti-plus"></i>افزودن + سینک فوری</button>
  </div>

  <div class="card">
    <div class="ct"><i class="ti ti-server"></i>ورکرها<span class="sp"></span><button class="btn btn-o" onclick="syncAll()"><i class="ti ti-cloud-upload"></i>سینک همه</button></div>
    <div id="wList"></div>
  </div>
</div>
<div id="toasts"></div>
<script>
const $=id=>document.getElementById(id);
function toast(m,e){const t=document.createElement('div');t.className='toast'+(e?' err':'');t.textContent=m;$('toasts').appendChild(t);requestAnimationFrame(()=>t.classList.add('show'));setTimeout(()=>{t.classList.remove('show');setTimeout(()=>t.remove(),300)},3600)}
async function jf(url,opt){const r=await fetch(url,opt);if(r.status===401)location.href='/login';const d=await r.json().catch(()=>({}));if(!r.ok)throw new Error(d.detail||'خطا');return d}
function esc(s){return String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
async function loadAll(){
  try{
    const o=await jf('/api/hub/overview');
    $('subUrl').textContent=o.sub_url;
    $('syncInt').textContent=Math.round(o.auto_sync_seconds/60);
    $('stLocal').textContent=o.local_links_count||0;
    $('stRemote').textContent=o.remote_links_count||0;
    const ws=o.workers||[];
    $('stWorkers').textContent=ws.filter(w=>w.active).length;
    const el=$('wList');
    if(!ws.length){el.innerHTML='<div class="empty">هنوز ورکری اضافه نشده. آدرس و توکن هر پنل رو بالا وارد کن.</div>';return}
    el.innerHTML=ws.map(w=>`
      <div class="wcard">
        <div style="min-width:200px">
          <div class="wname">${esc(w.name)} ${w.active?'':'<span class="chip off">خاموش</span>'} ${w.include===false?'<span class="chip off">بدون ساب</span>':''}</div>
          <div class="wurl">${esc(w.url)}</div>
          <div style="display:flex;gap:6px;margin-top:6px;flex-wrap:wrap">
            <span class="chip"><i class="ti ti-link"></i>${w.links_count||0} کانفیگ</span>
            ${w.last_error?`<span class="chip err"><i class="ti ti-alert-circle"></i>${esc(String(w.last_error).slice(0,42))}</span>`
             :w.last_sync?`<span class="chip ok"><i class="ti ti-check"></i>${new Date(w.last_sync).toLocaleTimeString('fa-IR')}</span>`
             :'<span class="chip">هنوز سینک نشده</span>'}
            <span class="chip">توکن: ***${esc(w.token_tail||'')}</span>
          </div>
        </div>
        <div class="wacts">
          <button class="bicon" title="سینک" onclick="syncOne('${w.wid}')"><i class="ti ti-cloud-upload"></i></button>
          <button class="bicon" title="${w.active?'خاموش':'روشن'}" onclick="toggleW('${w.wid}','active',${!w.active})"><i class="ti ti-${w.active?'eye':'eye-off'}"></i></button>
          <button class="bicon" title="${w.include!==false?'حذف از ساب':'افزودن به ساب'}" onclick="toggleW('${w.wid}','include',${!(w.include!==false)})"><i class="ti ti-${w.include!==false?'checkbox':'square'}"></i></button>
          <button class="bicon dan" title="حذف" onclick="delW('${w.wid}','${esc(w.name)}')"><i class="ti ti-trash"></i></button>
        </div>
      </div>`).join('');
  }catch(e){toast(e.message,true)}
}
async function addWorker(){
  const b=$('btnAdd');b.disabled=true;
  try{
    const d=await jf('/api/hub/workers',{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({name:$('wName').value,url:$('wUrl').value,token:$('wTok').value})});
    const ok=d.first_sync&&d.first_sync.ok;
    toast(ok?`ورکر اضافه شد — ${d.first_sync.links} کانفیگ گرفته شد`:'ورکر اضافه شد ولی سینک اولیه ناموفق بود — آدرس/توکن رو چک کن',!ok);
    $('wName').value='';$('wUrl').value='';$('wTok').value='';loadAll();
  }catch(e){toast(e.message,true)}finally{b.disabled=false}
}
async function syncOne(wid){toast('در حال سینک...');try{const r=await jf(`/api/hub/workers/${wid}/sync`,{method:'POST'});toast(r.ok?`سینک شد — ${r.links} کانفیگ`:`خطا: ${r.error}`,!r.ok);loadAll()}catch(e){toast(e.message,true)}}
async function syncAll(){toast('سینک همه ورکرها...');try{const r=await jf('/api/hub/sync-all',{method:'POST'});const ok=(r.results||[]).filter(x=>x.ok).length;toast(`${ok}/${(r.results||[]).length} ورکر سینک شد`);loadAll()}catch(e){toast(e.message,true)}}
async function toggleW(wid,k,v){try{await jf(`/api/hub/workers/${wid}`,{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({[k]:v})});loadAll()}catch(e){toast(e.message,true)}}
async function delW(wid,name){if(!confirm(`حذف ورکر «${name}»؟ کانفیگ‌هاش از ساب حذف می‌شن (پنل خودش دست نمی‌خوره).`))return;try{await jf(`/api/hub/workers/${wid}`,{method:'DELETE'});toast('حذف شد');loadAll()}catch(e){toast(e.message,true)}}
function copySub(){navigator.clipboard.writeText($('subUrl').textContent).then(()=>toast('لینک ساب کپی شد'))}
loadAll();
</script></body></html>"""


@router.get("/hub", response_class=HTMLResponse)
async def hub_page(request: Request):
    from main import SESSION_COOKIE, is_valid_session
    if not await is_valid_session(request.cookies.get(SESSION_COOKIE)):
        return RedirectResponse(url="/login")
    ensure_hub_sync()
    return HTMLResponse(content=_HUB_PAGE)