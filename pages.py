# pages.py — OMID v14.0 · GOLD EDITION  (سازگار با main.py v14.0)
# شامل: LOGO_SVG, HEARTBEAT_HTML, LOGIN_HTML, DASHBOARD_HTML, get_public_page_html()
# تم: طلایی + مشکی · لوگوی O طلایی با تاج و حلقه‌های مداری
# صفحه ورود VIP: کارت تک‌پنلی (پنل دیتا + چارت زنده + ضربان قلب + فرم ورود)
# پشتیبانی: @omiddemon
# قابلیت‌ها: Multi-IP (پروکسی خروجی SOCKS5/HTTP)، تست IP، پروکسی پیش‌فرض سرور

# ─────────────────────── لوگوی OMID (طلایی با تاج) ───────────────────────
LOGO_SVG = """<svg class="omid-logo" viewBox="0 0 220 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="OMID">
<defs>
<linearGradient id="gGold" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fdf3c8"/><stop offset=".35" stop-color="#f3d98b"/><stop offset=".65" stop-color="#d9a83f"/><stop offset="1" stop-color="#a8741f"/></linearGradient>
<linearGradient id="gRing" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#cfeaff"/><stop offset=".5" stop-color="#5fb2ff"/><stop offset="1" stop-color="#1e5fa8"/></linearGradient>
<radialGradient id="gHalo"><stop offset="0" stop-color="#7fc4ff" stop-opacity=".28"/><stop offset="1" stop-color="#7fc4ff" stop-opacity="0"/></radialGradient>
</defs>
<circle cx="110" cy="112" r="100" fill="url(#gHalo)"/>
<circle class="ring r1" cx="110" cy="112" r="86" fill="none" stroke="url(#gGold)" stroke-width="2" stroke-dasharray="40 14 8 14" stroke-linecap="round" opacity=".8"/>
<circle class="ring r2" cx="110" cy="112" r="72" fill="none" stroke="url(#gRing)" stroke-width="1.4" stroke-dasharray="3 9" stroke-linecap="round" opacity=".8"/>
<circle cx="110" cy="112" r="63" fill="#0a1424"/>
<circle class="o-glow" cx="110" cy="112" r="63" fill="none" stroke="url(#gGold)" stroke-width="1.6" opacity=".55"/>
<path d="M30 152 Q110 194 190 144" stroke="url(#gRing)" stroke-width="2.2" fill="none" opacity=".7"/>
<path d="M26 162 Q110 204 194 154" stroke="#bfe9ff" stroke-width="1" fill="none" opacity=".45"/>
<text x="110" y="146" text-anchor="middle" font-family="Cinzel, serif" font-weight="900" font-size="104" fill="url(#gGold)">O</text>
<g transform="translate(110,42)">
<path d="M-25 10 L-17 -7 L-7 4 L0 -13 L7 4 L17 -7 L25 10 Z" fill="url(#gGold)"/>
<circle cx="-17" cy="-10" r="2.6" fill="#f3d98b"/><circle cx="0" cy="-16" r="2.6" fill="#f3d98b"/><circle cx="17" cy="-10" r="2.6" fill="#f3d98b"/>
<rect x="-25" y="10" width="50" height="5.5" rx="2.75" fill="url(#gGold)"/>
</g>
</svg>"""

# ─────────────────────── ضربان قلب (ECG دوطرفه + قلب تپنده) ───────────────────────
HEARTBEAT_HTML = """<div class="hb-wrap" aria-hidden="true">
<div class="hb-bpm"><span>BPM</span><b id="hbBpm">75</b></div>
<div class="hb-row">
<svg class="ecg" viewBox="0 0 220 64" preserveAspectRatio="none">
<defs><linearGradient id="hbeA" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#a8741f"/><stop offset="1" stop-color="#f3d98b"/></linearGradient></defs>
<path d="M0 38 H110 L122 24 L132 50 L142 8 L152 58 L162 32 L172 42 L182 38 H220" stroke="url(#hbeA)"/>
</svg>
<svg class="hb-heart" viewBox="0 0 24 24">
<defs><linearGradient id="hbeH" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fdf3c8"/><stop offset=".5" stop-color="#f3d98b"/><stop offset="1" stop-color="#c9962f"/></linearGradient></defs>
<path fill="url(#hbeH)" d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
</svg>
<svg class="ecg" viewBox="0 0 220 64" preserveAspectRatio="none">
<defs><linearGradient id="hbeB" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#f3d98b"/><stop offset="1" stop-color="#a8741f"/></linearGradient></defs>
<path d="M0 38 H38 L48 42 L58 32 L68 58 L78 8 L88 50 L98 24 L110 38 H220" stroke="url(#hbeB)"/>
</svg>
</div>
<div class="hb-cap">OMID</div>
</div>
<script>(function(){var b=document.getElementById('hbBpm');if(!b)return;setInterval(function(){b.textContent=68+Math.floor(Math.random()*21)},2600)})();</script>"""

# ─────────────────────── CSS مشترک لوگو + قلب (طلایی) ───────────────────────
_GOLD_CSS = """
.omid-logo{display:block;filter:drop-shadow(0 0 14px rgba(217,168,63,.35)) drop-shadow(0 4px 12px rgba(0,0,0,.45))}
.omid-logo .ring{transform-box:fill-box;transform-origin:center}
.omid-logo .r1{animation:omCW 16s linear infinite}
.omid-logo .r2{animation:omCCW 10s linear infinite}
@keyframes omCW{to{transform:rotate(360deg)}}
@keyframes omCCW{to{transform:rotate(-360deg)}}
.omid-logo .o-glow{animation:omGlow 2.6s ease-in-out infinite}
@keyframes omGlow{0%,100%{opacity:.35}50%{opacity:.9}}
.hb-wrap{display:flex;flex-direction:column;align-items:center;gap:2px;pointer-events:none;user-select:none}
.hb-bpm{font-size:11px;letter-spacing:.22em;color:#C9B98F;font-weight:600;direction:ltr;display:inline-flex;align-items:baseline;gap:9px}
.hb-bpm b{font-size:17px;color:#fdf3c8;font-family:ui-monospace,monospace;letter-spacing:0;text-shadow:0 0 12px rgba(243,217,139,.55)}
.hb-row{display:flex;align-items:center;gap:5px;width:100%;justify-content:center}
.hb-row svg.ecg{flex:1;height:46px;min-width:0;max-width:300px}
.hb-row .ecg path{fill:none;stroke-width:2.2;vector-effect:non-scaling-stroke;stroke-linecap:round;stroke-linejoin:round;filter:drop-shadow(0 0 6px rgba(217,168,63,.75))}
.hb-heart{width:52px;height:52px;flex-shrink:0;filter:drop-shadow(0 0 15px rgba(217,168,63,.85));animation:hbBeat 1s ease-in-out infinite}
@keyframes hbBeat{0%,100%{transform:scale(1)}14%{transform:scale(1.28)}28%{transform:scale(1)}42%{transform:scale(1.14)}56%{transform:scale(1)}}
.hb-cap{font-family:'Cinzel',serif;font-size:9px;letter-spacing:.62em;text-indent:.62em;color:rgba(217,168,63,.55)}
"""

# ═══════════════════════════ صفحه ورود (LOGIN) — طلایی-مشکی VIP ═══════════════════════════
_LOGIN_TPL = r"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="theme-color" content="#050505">
<title>ورود · OMID GOLD</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800;900&family=Cinzel:wght@600;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{
 --gold1:#fdf3c8;--gold2:#f3d98b;--gold3:#d9a83f;--gold4:#a8741f;
 --bord:rgba(217,168,63,.24);--bordH:rgba(240,205,110,.5);
 --t1:#F4EEDC;--t2:#C9B98F;--t3:#8D8368;
}
html,body{min-height:100%}
body{font-family:'Vazirmatn',sans-serif;background:#050505;color:var(--t1);display:flex;align-items:center;justify-content:center;padding:24px 14px;overflow-x:hidden}
.bg-glow{position:fixed;inset:0;z-index:0;pointer-events:none;
 background:radial-gradient(760px 480px at 50% -6%,rgba(217,168,63,.13),transparent 62%),
 radial-gradient(560px 420px at 88% 108%,rgba(168,116,31,.1),transparent 60%),
 radial-gradient(420px 320px at 8% 82%,rgba(217,168,63,.06),transparent 60%)}
.bg-grid{position:fixed;inset:0;z-index:0;pointer-events:none;
 background-image:linear-gradient(rgba(217,168,63,.045) 1px,transparent 1px),linear-gradient(90deg,rgba(217,168,63,.045) 1px,transparent 1px);
 background-size:46px 46px;
 -webkit-mask-image:radial-gradient(ellipse 72% 62% at 50% 42%,#000 25%,transparent 74%);
 mask-image:radial-gradient(ellipse 72% 62% at 50% 42%,#000 25%,transparent 74%)}
.dust{position:fixed;border-radius:50%;background:var(--gold2);filter:blur(1px);z-index:1;pointer-events:none;opacity:0;animation:twk 7s ease-in-out infinite}
@keyframes twk{0%,100%{opacity:0;transform:translateY(6px)}50%{opacity:.8;transform:none}}
.card{position:relative;z-index:5;width:100%;max-width:436px;
 background:linear-gradient(168deg,rgba(30,25,12,.82),rgba(9,8,5,.96) 55%);
 border:1px solid var(--bord);border-radius:32px;
 padding:34px 26px 24px;
 box-shadow:0 40px 110px rgba(0,0,0,.75),0 0 60px rgba(217,168,63,.09),inset 0 1px 0 rgba(243,217,139,.16);
 backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px)}
.card::before{content:'';position:absolute;top:0;left:50%;transform:translateX(-50%);width:64%;height:1.5px;
 background:linear-gradient(90deg,transparent,rgba(243,217,139,.85),transparent);border-radius:2px}
.card::after{content:'';position:absolute;inset:9px;border:1px dashed rgba(217,168,63,.14);border-radius:24px;pointer-events:none}
.brand{text-align:center;margin-bottom:20px;animation:up .7s ease both}
.logo{width:152px;height:152px;margin:0 auto 4px;position:relative;filter:drop-shadow(0 0 26px rgba(217,168,63,.32)) drop-shadow(0 8px 20px rgba(0,0,0,.5))}
.logo .orb1{transform-box:fill-box;transform-origin:center;animation:spin 18s linear infinite}
.logo .orb2{transform-box:fill-box;transform-origin:center;animation:spinR 12s linear infinite}
.logo .sat{transform-box:fill-box;transform-origin:76px 76px;animation:spin 8s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
@keyframes spinR{to{transform:rotate(-360deg)}}
.logo .o-core{animation:coreGlow 2.8s ease-in-out infinite}
@keyframes coreGlow{0%,100%{opacity:.5}50%{opacity:1}}
.brand-name{font-family:'Cinzel',serif;font-weight:900;font-size:37px;letter-spacing:.3em;text-indent:.3em;line-height:1.15;
 background:linear-gradient(100deg,#a8741f 0%,#f3d98b 25%,#fdf3c8 50%,#f3d98b 75%,#a8741f 100%);
 background-size:220% auto;-webkit-background-clip:text;background-clip:text;color:transparent;
 animation:shimmer 5.5s linear infinite;filter:drop-shadow(0 3px 14px rgba(217,168,63,.35))}
@keyframes shimmer{to{background-position:-220% center}}
.brand-sub{font-family:'Cinzel',serif;font-size:9.5px;font-weight:700;letter-spacing:.44em;text-indent:.44em;color:var(--t3);margin-top:8px}
.brand-sub b{color:var(--gold2);font-weight:700}
.datapanel{background:rgba(5,5,4,.55);border:1px solid var(--bord);border-radius:22px;padding:16px 15px 13px;margin-bottom:6px;animation:up .7s .1s ease both}
.dp-head{display:flex;align-items:center;justify-content:space-between;margin-bottom:13px}
.dp-title{display:flex;align-items:center;gap:8px;font-size:12.5px;font-weight:800;color:var(--t1)}
.dp-title i{color:var(--gold2);font-size:17px;filter:drop-shadow(0 0 7px rgba(217,168,63,.6))}
.live{display:inline-flex;align-items:center;gap:6px;font-size:9.5px;font-weight:700;color:var(--gold2);border:1px solid rgba(217,168,63,.4);background:rgba(217,168,63,.08);padding:4px 12px;border-radius:20px}
.ldot{width:6px;height:6px;border-radius:50%;background:var(--gold2);box-shadow:0 0 9px rgba(243,217,139,.9);animation:pls 1.8s infinite}
@keyframes pls{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.35;transform:scale(.8)}}
.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:9px;margin-bottom:12px}
.stat{background:rgba(20,17,9,.55);border:1px solid rgba(217,168,63,.18);border-radius:15px;padding:12px 5px 10px;text-align:center;position:relative;overflow:hidden;transition:.2s}
.stat:hover{border-color:var(--bordH);transform:translateY(-2px)}
.stat::before{content:'';position:absolute;top:0;right:18%;width:64%;height:1.5px;background:linear-gradient(90deg,transparent,var(--ac),transparent)}
.st1{--ac:rgba(243,217,139,.9)}.st2{--ac:rgba(217,168,63,.9)}.st3{--ac:rgba(253,243,200,.9)}
.s-ic{font-size:17px;color:var(--ac);margin-bottom:6px;filter:drop-shadow(0 0 7px var(--ac))}
.s-val{font-size:17.5px;font-weight:800;color:#fff;line-height:1;direction:ltr}
.s-val small{font-size:9.5px;font-weight:600;color:var(--t3)}
.s-lab{font-size:9px;color:var(--t3);font-weight:600;margin-top:5px}
#chart{width:100%;height:118px;display:block}
.sep{border:none;border-top:1px dashed rgba(217,168,63,.22);margin:16px 4px}
.hb{text-align:center;animation:up .7s .2s ease both}
.hb-bpm{display:inline-flex;align-items:baseline;gap:9px;font-size:10.5px;letter-spacing:.24em;color:var(--t2);direction:ltr}
.hb-bpm b{font-size:17px;color:var(--gold1);font-family:ui-monospace,monospace;letter-spacing:.04em;text-shadow:0 0 12px rgba(243,217,139,.55)}
.hb-bpm i{color:var(--gold2);font-size:14px}
.hb-row{display:flex;align-items:center;gap:4px;margin:2px 0 3px}
.hb-row svg.ecg{flex:1;height:44px;min-width:0}
.hb-row .ecg path{fill:none;stroke-width:2.1;vector-effect:non-scaling-stroke;stroke-linecap:round;stroke-linejoin:round;filter:drop-shadow(0 0 6px rgba(217,168,63,.75))}
.hb-heart{width:48px;height:48px;flex-shrink:0;filter:drop-shadow(0 0 16px rgba(217,168,63,.85));animation:beat 1s ease-in-out infinite}
@keyframes beat{0%,100%{transform:scale(1)}14%{transform:scale(1.3)}28%{transform:scale(1)}42%{transform:scale(1.15)}56%{transform:scale(1)}}
.hb-cap{font-family:'Cinzel',serif;font-size:9px;letter-spacing:.6em;text-indent:.6em;color:rgba(217,168,63,.55)}
.loginarea{animation:up .7s .3s ease both}
h1{font-size:17px;font-weight:800;color:var(--t1);text-align:center;margin-bottom:7px}
.sub{font-size:11.5px;color:var(--t2);text-align:center;margin-bottom:16px;line-height:1.8}
.hint{display:flex;align-items:center;gap:10px;background:rgba(217,168,63,.06);border:1px solid var(--bord);border-radius:13px;padding:9px 13px;margin-bottom:15px}
.hint-label{font-size:10.5px;color:var(--t3);flex:1}
.hint-val{font-family:ui-monospace,monospace;font-size:13px;font-weight:700;color:var(--gold2);background:rgba(217,168,63,.1);border:1px solid rgba(217,168,63,.4);padding:3px 14px;border-radius:9px;cursor:pointer;transition:.15s;letter-spacing:.14em;direction:ltr}
.hint-val:hover{background:rgba(217,168,63,.24);box-shadow:0 0 14px rgba(217,168,63,.35)}
.field label{display:block;font-size:10.5px;font-weight:700;color:var(--t3);margin-bottom:8px;letter-spacing:.1em}
.inp-wrap{position:relative;margin-bottom:15px}
.inp-wrap input{width:100%;padding:14px 46px 14px 46px;border-radius:15px;border:1px solid var(--bord);background:rgba(0,0,0,.5);color:var(--t1);font-family:inherit;font-size:14px;outline:none;transition:.2s}
.inp-wrap input::placeholder{color:var(--t3)}
.inp-wrap input:focus{border-color:rgba(243,217,139,.6);box-shadow:0 0 0 3px rgba(217,168,63,.13),0 0 22px rgba(217,168,63,.12)}
.ic-wave{position:absolute;left:15px;top:50%;transform:translateY(-50%);color:var(--t3);font-size:18px;pointer-events:none;transition:.2s}
input:focus~.ic-wave{color:var(--gold2)}
.eye{position:absolute;right:10px;top:50%;transform:translateY(-50%);background:none;border:none;color:var(--t3);font-size:18px;cursor:pointer;padding:7px;line-height:1;transition:.15s}
.eye:hover{color:var(--gold2)}
.btn{width:100%;padding:14px;cursor:pointer;border-radius:16px;position:relative;overflow:hidden;
 font-family:inherit;font-size:14px;font-weight:800;display:flex;align-items:center;justify-content:center;gap:9px;
 color:#241a05;background:linear-gradient(135deg,#f9ecc0,#eccb7a 46%,#c9962f);
 border:1px solid rgba(255,238,190,.6);
 box-shadow:0 12px 34px rgba(217,168,63,.35),inset 0 1px 0 rgba(255,255,255,.65);transition:.2s}
.btn::after{content:'';position:absolute;top:0;bottom:0;width:46%;left:-60%;
 background:linear-gradient(105deg,transparent,rgba(255,255,255,.55),transparent);transform:skewX(-18deg);transition:left .6s ease}
.btn:hover::after{left:120%}
.btn:hover{filter:brightness(1.06)}
.btn:active{transform:scale(.985)}
.btn:disabled{opacity:.6;cursor:not-allowed}
.btn i{font-size:18px}
@keyframes spin{to{transform:rotate(360deg)}}
.spin{animation:spin 1s linear infinite;display:inline-block}
.err{display:none;background:rgba(229,72,77,.08);border:1px solid rgba(229,72,77,.3);border-radius:11px;padding:10px 14px;margin-bottom:14px;font-size:12px;color:#FF9393;align-items:center;gap:8px;text-align:center;justify-content:center}
.err.show{display:flex;animation:shake .45s ease}
@keyframes shake{0%,100%{transform:none}20%{transform:translateX(-6px)}40%{transform:translateX(6px)}60%{transform:translateX(-4px)}80%{transform:translateX(4px)}}
.footer{margin-top:20px;padding-top:16px;border-top:1px dashed rgba(217,168,63,.18);display:flex;align-items:center;justify-content:center;gap:8px;font-size:11px;color:var(--t3);animation:up .7s .4s ease both}
.footer a{color:var(--gold2);font-weight:700;text-decoration:none;display:flex;align-items:center;gap:5px;transition:.15s}
.footer a:hover{text-shadow:0 0 12px rgba(243,217,139,.7)}
@keyframes up{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:none}}
@media(max-width:400px){
 .card{padding:26px 17px 20px;border-radius:26px}
 .logo{width:126px;height:126px}
 .brand-name{font-size:30px}
 .s-val{font-size:15px}
}
</style>
</head>
<body>
<div class="bg-glow"></div><div class="bg-grid"></div>

<div class="card">

  <div class="brand">
    <div class="logo">
      <svg viewBox="0 0 152 152" width="152" height="152" role="img" aria-label="OMID">
        <defs>
          <linearGradient id="lgG1" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fdf3c8"/><stop offset=".35" stop-color="#f3d98b"/><stop offset=".65" stop-color="#d9a83f"/><stop offset="1" stop-color="#a8741f"/></linearGradient>
          <radialGradient id="lgHalo"><stop offset="0" stop-color="#d9a83f" stop-opacity=".3"/><stop offset="1" stop-color="#d9a83f" stop-opacity="0"/></radialGradient>
        </defs>
        <circle cx="76" cy="76" r="74" fill="url(#lgHalo)"/>
        <g class="orb1"><circle cx="76" cy="76" r="70" fill="none" stroke="url(#lgG1)" stroke-width="1.8" stroke-dasharray="34 10 6 10" stroke-linecap="round" opacity=".9"/></g>
        <g class="orb2"><circle cx="76" cy="76" r="60" fill="none" stroke="rgba(217,168,63,.4)" stroke-width="1.1" stroke-dasharray="2.5 8" stroke-linecap="round"/></g>
        <g class="sat"><circle cx="76" cy="16" r="3.4" fill="#fdf3c8"/><circle cx="76" cy="16" r="6.5" fill="#f3d98b" opacity=".28"/></g>
        <circle cx="76" cy="76" r="49" fill="#0A0806" stroke="url(#lgG1)" stroke-width="1.4"/>
        <circle class="o-core" cx="76" cy="76" r="49" fill="none" stroke="url(#lgG1)" stroke-width="2" opacity=".6"/>
        <text x="76" y="99" text-anchor="middle" font-family="Cinzel, serif" font-weight="900" font-size="62" fill="url(#lgG1)">O</text>
        <g transform="translate(76,37)">
          <path d="M-17 7 L-11.5 -5 L-4.5 3 L0 -9 L4.5 3 L11.5 -5 L17 7 Z" fill="url(#lgG1)"/>
          <circle cx="-11.5" cy="-7.5" r="1.9" fill="#f3d98b"/><circle cx="0" cy="-11.5" r="1.9" fill="#f3d98b"/><circle cx="11.5" cy="-7.5" r="1.9" fill="#f3d98b"/>
          <rect x="-17" y="7" width="34" height="4" rx="2" fill="url(#lgG1)"/>
        </g>
      </svg>
    </div>
    <div class="brand-name">OMID</div>
    <div class="brand-sub"><b>GOLD</b> EDITION · VIP PANEL</div>
  </div>

  <div class="datapanel">
    <div class="dp-head">
      <span class="dp-title"><i class="ti ti-chart-dots-3"></i>مصرف دیتای سرور</span>
      <span class="live"><span class="ldot"></span>زنده</span>
    </div>
    <div class="stats">
      <div class="stat st1"><i class="ti ti-user s-ic"></i><div class="s-val" id="stUsers">8</div><div class="s-lab">کاربر آنلاین</div></div>
      <div class="stat st2"><i class="ti ti-database s-ic"></i><div class="s-val"><span id="stTotal">214.70</span> <small>GB</small></div><div class="s-lab">مصرف کل</div></div>
      <div class="stat st3"><i class="ti ti-gauge s-ic"></i><div class="s-val"><span id="stRate">1.43</span> <small>MB/s</small></div><div class="s-lab">لحظه‌ای</div></div>
    </div>
    <canvas id="chart"></canvas>
  </div>

  <hr class="sep">
  <div class="hb">
    <div class="hb-bpm"><span>BPM</span><b id="bpm">75</b><i class="ti ti-activity"></i></div>
    <div class="hb-row">
      <svg class="ecg" viewBox="0 0 220 64" preserveAspectRatio="none">
        <defs><linearGradient id="egA" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#a8741f"/><stop offset="1" stop-color="#f3d98b"/></linearGradient></defs>
        <path d="M0 38 H110 L122 24 L132 50 L142 8 L152 58 L162 32 L172 42 L182 38 H220" stroke="url(#egA)"/>
      </svg>
      <svg class="hb-heart" viewBox="0 0 24 24">
        <defs><linearGradient id="hgA" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fdf3c8"/><stop offset=".5" stop-color="#f3d98b"/><stop offset="1" stop-color="#c9962f"/></linearGradient></defs>
        <path fill="url(#hgA)" d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
      </svg>
      <svg class="ecg" viewBox="0 0 220 64" preserveAspectRatio="none">
        <defs><linearGradient id="egB" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#f3d98b"/><stop offset="1" stop-color="#a8741f"/></linearGradient></defs>
        <path d="M0 38 H38 L48 42 L58 32 L68 58 L78 8 L88 50 L98 24 L110 38 H220" stroke="url(#egB)"/>
      </svg>
    </div>
    <div class="hb-cap">OMID</div>
  </div>
  <hr class="sep">

  <div class="loginarea">
    <h1>ورود به پنل</h1>
    <p class="sub">برای دسترسی به داشبورد، رمز عبور را وارد کنید</p>
    <div class="err" id="err"><i class="ti ti-alert-circle"></i><span id="err-text"></span></div>
    <div class="hint">
      <span class="hint-label">رمز پیش‌فرض سیستم</span>
      <span class="hint-val" onclick="document.getElementById('pw').value='OMID';document.getElementById('pw').focus()">OMID</span>
    </div>
    <form id="f" autocomplete="off">
      <div class="field">
        <label>رمز عبور</label>
        <div class="inp-wrap">
          <input type="password" id="pw" placeholder="رمز عبور را وارد کنید">
          <button class="eye" id="eye" type="button" aria-label="نمایش رمز"><i class="ti ti-eye-off"></i></button>
          <i class="ti ti-wave-sine ic-wave"></i>
        </div>
      </div>
      <button class="btn" id="btn" type="submit"><i class="ti ti-crown"></i> ورود به داشبورد</button>
    </form>
  </div>

  <div class="footer">پشتیبانی <a href="https://t.me/omiddemon" target="_blank"><i class="ti ti-brand-telegram"></i>@omiddemon</a></div>
</div>

<script>
(function(){
  for(let i=0;i<16;i++){
    const d=document.createElement('span');d.className='dust';
    const s=2+Math.random()*3.5;
    d.style.cssText='width:'+s+'px;height:'+s+'px;top:'+(5+Math.random()*90)+'%;left:'+(3+Math.random()*94)+'%;animation-delay:'+(Math.random()*7)+'s;animation-duration:'+(5+Math.random()*5)+'s';
    document.body.appendChild(d);
  }
})();
const cv=document.getElementById('chart'),ctx=cv.getContext('2d');
let W=0,H=0;
const N=42;
let data=Array.from({length:N},()=>.3+Math.random()*.5);
function fit(){const r=window.devicePixelRatio||1;W=cv.clientWidth;H=cv.clientHeight;cv.width=W*r;cv.height=H*r;ctx.setTransform(r,0,0,r,0,0)}
function draw(){
  if(!W)fit();
  ctx.clearRect(0,0,W,H);
  ctx.strokeStyle='rgba(217,168,63,.09)';ctx.lineWidth=1;
  for(let i=1;i<4;i++){const y=H/4*i;ctx.beginPath();ctx.moveTo(0,y+.5);ctx.lineTo(W,y+.5);ctx.stroke()}
  for(let i=1;i<8;i++){const x=W/8*i;ctx.beginPath();ctx.moveTo(x+.5,0);ctx.lineTo(x+.5,H);ctx.stroke()}
  const step=W/(N-1),pad=10;
  const pts=data.map((v,i)=>({x:i*step,y:H-((v/100*.9+.05)*(H-pad*2)+pad)}));
  ctx.beginPath();ctx.moveTo(pts[0].x,pts[0].y);
  for(let i=1;i<pts.length;i++)ctx.lineTo(pts[i].x,pts[i].y);
  const lg=ctx.createLinearGradient(0,0,W,0);
  lg.addColorStop(0,'#a8741f');lg.addColorStop(.5,'#f3d98b');lg.addColorStop(1,'#fdf3c8');
  ctx.strokeStyle=lg;ctx.lineWidth=2.4;ctx.lineJoin='round';ctx.lineCap='round';
  ctx.shadowColor='rgba(243,217,139,.75)';ctx.shadowBlur=11;ctx.stroke();ctx.shadowBlur=0;
  ctx.lineTo(W,H);ctx.lineTo(0,H);ctx.closePath();
  const fg=ctx.createLinearGradient(0,0,0,H);
  fg.addColorStop(0,'rgba(217,168,63,.22)');fg.addColorStop(1,'rgba(217,168,63,0)');
  ctx.fillStyle=fg;ctx.fill();
  const hy=pts[pts.length-1].y;
  ctx.beginPath();ctx.arc(W-3,hy,7,0,Math.PI*2);ctx.fillStyle='rgba(243,217,139,.25)';ctx.fill();
  ctx.beginPath();ctx.arc(W-3,hy,3.4,0,Math.PI*2);ctx.fillStyle='#fdf3c8';ctx.shadowColor='#f3d98b';ctx.shadowBlur=13;ctx.fill();ctx.shadowBlur=0;
}
let total=214.70;
function tick(){
  let v=data[data.length-1]+(Math.random()-.48)*14;
  v=Math.max(6,Math.min(94,v));
  data.push(v);data.shift();
  const rate=v/32;
  document.getElementById('stRate').textContent=rate.toFixed(2);
  total+=rate*.0011;
  document.getElementById('stTotal').textContent=total.toFixed(2);
  draw();
}
fit();draw();
addEventListener('resize',()=>{fit();draw()});
setInterval(tick,1000);
setInterval(()=>{document.getElementById('bpm').textContent=68+Math.floor(Math.random()*21)},2600);
setInterval(()=>{document.getElementById('stUsers').textContent=4+Math.floor(Math.random()*9)},6000);
const pwIn=document.getElementById('pw'),eye=document.getElementById('eye');
eye.addEventListener('click',()=>{
  const show=pwIn.type==='password';
  pwIn.type=show?'text':'password';
  eye.innerHTML='<i class="ti '+(show?'ti-eye':'ti-eye-off')+'"></i>';
  pwIn.focus();
});
function showErr(m){const e=document.getElementById('err');document.getElementById('err-text').textContent=m;e.classList.remove('show');void e.offsetWidth;e.classList.add('show');}
document.getElementById('f').addEventListener('submit',async e=>{
  e.preventDefault();
  const btn=document.getElementById('btn'),err=document.getElementById('err');
  err.classList.remove('show');btn.disabled=true;
  btn.innerHTML='<i class="ti ti-loader-2 spin"></i> در حال ورود...';
  try{
    if(location.protocol==='file:'){
      await new Promise(r=>setTimeout(r,900));
      btn.disabled=false;btn.innerHTML='<i class="ti ti-crown"></i> ورود به داشبورد';
      return;
    }
    const r=await fetch('/api/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({password:pwIn.value})});
    if(!r.ok){const d=await r.json().catch(()=>({}));throw new Error(d.detail||'رمز عبور اشتباه است');}
    location.href='/dashboard';
  }catch(ex){
    showErr(ex.message);
    btn.disabled=false;btn.innerHTML='<i class="ti ti-crown"></i> ورود به داشبورد';
  }
});
</script>
</body></html>"""

# ═══════════════════════════ داشبورد — تم طلایی-مشکی ═══════════════════════════
_DASH_TPL = r"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>OMID · پنل مدیریت</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800&family=Cinzel:wght@700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#05070D;--bg2:#0A0E18;--bg3:#0E1420;--card:rgba(14,18,30,.72);--card2:rgba(16,22,36,.85);--bord:rgba(217,168,63,.18);--bordH:rgba(240,205,110,.45);--gd:rgba(217,168,63,.08);--gold:#f3d98b;--gold2:#d9a83f;--gold3:#fdf3c8;--t1:#F4EEDC;--t2:#C9B98F;--t3:#8D8368;--green-t:#7DDFA8;--red-t:#FF7B72;--amber-t:#FFB35C;--sb-w:250px;--rad:16px;--sh:0 10px 40px rgba(0,0,0,.55)}
[data-theme="light"]{--bg:#F2EBD8;--bg2:#EAE0C6;--bg3:#E0D5B8;--card:rgba(253,250,240,.9);--card2:#FDFAF4;--bord:rgba(140,100,20,.3);--bordH:rgba(140,100,20,.55);--gd:rgba(140,100,20,.08);--t1:#241A05;--t2:#5C4A1E;--t3:#7E6B3A;--green-t:#1E7A4F;--red-t:#A32020;--amber-t:#8A5E0F;--sh:0 8px 30px rgba(90,60,10,.14)}
html,body{height:100%}
body{font-family:'Vazirmatn',sans-serif;background:radial-gradient(900px 500px at 80% -10%,rgba(217,168,63,.07),transparent 60%),var(--bg);color:var(--t1);min-height:100vh;font-size:14px;transition:background .3s,color .3s}
::-webkit-scrollbar{width:5px;height:5px}::-webkit-scrollbar-track{background:transparent}::-webkit-scrollbar-thumb{background:rgba(217,168,63,.3);border-radius:3px}
a{color:inherit;text-decoration:none}
.bgfix{position:fixed;inset:0;pointer-events:none;background-image:linear-gradient(rgba(217,168,63,.035) 1px,transparent 1px),linear-gradient(90deg,rgba(217,168,63,.035) 1px,transparent 1px);background-size:44px 44px;z-index:0}
.sidebar{width:var(--sb-w);min-height:100vh;background:linear-gradient(180deg,var(--bg2),var(--bg));border-left:1px solid var(--bord);display:flex;flex-direction:column;flex-shrink:0;position:fixed;right:0;top:0;bottom:0;z-index:200;transition:transform .25s}
.logo{display:flex;align-items:center;gap:11px;padding:18px 16px 14px;border-bottom:1px solid var(--bord);position:relative}
.logo .omid-logo{width:42px;height:42px;flex-shrink:0}
.logo-name{font-family:'Cinzel',serif;font-size:15px;font-weight:900;letter-spacing:.2em;background:linear-gradient(180deg,#fdf6d8,#f3d98b 45%,#b07f22);-webkit-background-clip:text;background-clip:text;color:transparent}
.logo-sub{font-size:9px;color:var(--t3);letter-spacing:.2em;margin-top:2px;font-family:'Cinzel',serif}
.sb-close{display:none;position:absolute;left:12px;top:18px;background:var(--gd);border:1px solid var(--bord);color:var(--t2);width:28px;height:28px;border-radius:8px;font-size:14px;align-items:center;justify-content:center;cursor:pointer}
.nav-wrap{flex:1;overflow-y:auto;padding:6px 0 8px}
.nav-sec{padding:14px 16px 4px;font-size:9px;letter-spacing:.16em;color:var(--t3);font-weight:700}
.nav-it{display:flex;align-items:center;gap:10px;padding:10px 14px;color:var(--t3);font-size:12.5px;cursor:pointer;border-right:2px solid transparent;transition:all .15s;margin:1px 8px;border-radius:9px}
.nav-it i{font-size:16px;width:18px;text-align:center;flex-shrink:0}
.nav-it:hover{background:var(--gd);color:var(--t2)}
.nav-it.on{background:var(--gd);color:var(--gold);border-right-color:var(--gold2);font-weight:700}
.nav-it.on i{color:var(--gold3)}
.nav-badge{margin-right:auto;background:var(--gd);border:1px solid var(--bord);color:var(--gold);font-size:9px;padding:1px 7px;border-radius:20px;font-weight:700;min-width:20px;text-align:center}
.sb-foot{padding:12px 14px;border-top:1px solid var(--bord)}
.mob-top{display:none;position:fixed;top:0;right:0;left:0;height:54px;background:var(--bg2);border-bottom:1px solid var(--bord);z-index:150;align-items:center;justify-content:space-between;padding:0 14px}
.mob-top .ml{display:flex;align-items:center;gap:9px}
.mob-top .omid-logo{width:30px;height:30px}
.mob-title{font-family:'Cinzel',serif;font-size:14px;font-weight:900;letter-spacing:.2em;background:linear-gradient(180deg,#fdf6d8,#d9a83f);-webkit-background-clip:text;background-clip:text;color:transparent}
.menu-btn{background:var(--gd);border:1px solid var(--bord);color:var(--gold);width:34px;height:34px;border-radius:9px;font-size:17px;display:flex;align-items:center;justify-content:center;cursor:pointer}
.overlay{display:none;position:fixed;inset:0;background:rgba(3,5,10,.65);z-index:190;backdrop-filter:blur(3px)}
.overlay.show{display:block}
.main{margin-right:var(--sb-w);flex:1;padding:26px 26px 40px;min-width:0;position:relative;z-index:1}
.pg{display:none}.pg.on{display:block;animation:fi .2s ease}
@keyframes fi{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
.topbar{display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:20px;flex-wrap:wrap;gap:12px}
.tb-title{font-size:18px;font-weight:800;display:flex;align-items:center;gap:9px}
.tb-title i{color:var(--gold2);font-size:20px}
.tb-sub{font-size:11px;color:var(--t3);margin-top:4px}
.tb-right{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.badge{font-size:10.5px;padding:4px 12px;border-radius:20px;font-weight:700;display:inline-flex;align-items:center;gap:6px;border:1px solid var(--bord);background:var(--gd);color:var(--gold)}
.dot{width:7px;height:7px;border-radius:50%;display:inline-block;flex-shrink:0}
.dg{background:#3ECF8E}.dr{background:#E5484D}
.pulse{animation:pulse 2s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.3}}
.metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:13px;margin-bottom:16px}
.metric{background:var(--card);border:1px solid var(--bord);border-radius:var(--rad);padding:17px;transition:.2s;position:relative;overflow:hidden;backdrop-filter:blur(10px)}
.metric::before{content:'';position:absolute;top:0;right:0;width:100%;height:2px;background:linear-gradient(90deg,var(--gold2),transparent 70%);opacity:.6}
.metric:hover{border-color:var(--bordH);transform:translateY(-2px);box-shadow:var(--sh)}
.m-icon{width:36px;height:36px;border-radius:10px;background:var(--gd);display:flex;align-items:center;justify-content:center;margin-bottom:12px;color:var(--gold);font-size:17px;border:1px solid var(--bord)}
.m-icon.suc{color:var(--green-t);background:rgba(62,207,142,.08);border-color:rgba(62,207,142,.2)}
.m-icon.dan{color:var(--red-t);background:rgba(229,72,77,.08);border-color:rgba(229,72,77,.2)}
.m-icon.amb{color:var(--amber-t);background:rgba(229,168,62,.08);border-color:rgba(229,168,62,.2)}
.m-val{font-size:25px;font-weight:800;line-height:1;background:linear-gradient(135deg,#fdf6d8,#f3d98b 45%,#b07f22);-webkit-background-clip:text;background-clip:text;color:transparent;display:flex;align-items:baseline;gap:5px}
[data-theme="light"] .m-val{background:linear-gradient(135deg,#8a5e0f,#b07f22);-webkit-background-clip:text;background-clip:text}
.m-unit{font-size:11px;font-weight:500;-webkit-text-fill-color:var(--t3);color:var(--t3)}
.m-label{font-size:10.5px;color:var(--t3);margin-top:7px;font-weight:600}
.g2{display:grid;grid-template-columns:1fr 1fr;gap:13px;margin-bottom:16px}
.g3{display:grid;grid-template-columns:2fr 1fr;gap:13px;margin-bottom:16px}
.card{background:var(--card);border:1px solid var(--bord);border-radius:var(--rad);padding:18px 20px;transition:border-color .2s;backdrop-filter:blur(10px)}
.card:hover{border-color:var(--bordH)}
.card-title{font-size:12.5px;font-weight:700;margin-bottom:15px;display:flex;align-items:center;gap:8px}
.card-title i{font-size:16px;color:var(--gold2)}
.ml-auto{margin-right:auto}
.sr{display:flex;align-items:center;justify-content:space-between;padding:9px 0;border-bottom:1px solid rgba(217,168,63,.08);font-size:12px}
.sr:last-child{border-bottom:none}
.sr-k{color:var(--t2);display:flex;align-items:center;gap:7px}
.sr-k i{font-size:13px;color:var(--t3)}
.sr-v{font-weight:700;font-size:11.5px;color:var(--t1)}
.mono{font-family:ui-monospace,monospace;direction:ltr}
.ch-lg{position:relative;height:320px}
.btn{font-family:inherit;font-size:12.5px;font-weight:700;border-radius:11px;padding:10px 16px;cursor:pointer;border:none;display:inline-flex;align-items:center;justify-content:center;gap:7px;transition:.18s;white-space:nowrap}
.btn:disabled{opacity:.5;cursor:not-allowed}
.btn-p{background:linear-gradient(135deg,#f9ecc0,#eccb7a 46%,#c9962f);color:#2a1e05;box-shadow:0 6px 22px rgba(217,168,63,.32),inset 0 1px 0 rgba(255,255,255,.6)}
.btn-p:hover{filter:brightness(1.07);transform:translateY(-1px)}
.btn-o{background:transparent;border:1px solid var(--bord);color:var(--t2)}
.btn-o:hover{border-color:var(--bordH);color:var(--gold);background:var(--gd)}
.btn-d{background:rgba(229,72,77,.12);border:1px solid rgba(229,72,77,.3);color:var(--red-t)}
.btn-d:hover{background:rgba(229,72,77,.22)}
.btn.tg{background:linear-gradient(135deg,#2AABEE,#1D86C7);color:#fff}
.btn.full{width:100%}
.btn-sm{padding:6px 11px;font-size:11px;border-radius:9px}
.btn-icon{width:30px;height:30px;padding:0;border-radius:8px;background:var(--gd);color:var(--gold);border:1px solid var(--bord);display:inline-flex;align-items:center;justify-content:center;cursor:pointer;font-size:14px;transition:.15s}
.btn-icon:hover{border-color:var(--bordH);color:var(--gold3);background:rgba(217,168,63,.16)}
.btn-icon.danger{color:var(--red-t);border-color:rgba(229,72,77,.25)}
.btn-icon.danger:hover{background:rgba(229,72,77,.14)}
.traf-hero{display:grid;grid-template-columns:1.4fr 1fr 1fr 1fr;gap:13px;margin-bottom:16px}
.traf-main{background:linear-gradient(155deg,var(--bg3),var(--card) 70%);border:1px solid var(--bord);border-radius:20px;padding:22px 24px;position:relative;overflow:hidden}
.traf-main::before{content:'';position:absolute;top:-50px;left:-50px;width:200px;height:200px;background:radial-gradient(circle,var(--gd),transparent 70%);pointer-events:none}
.tml{font-size:10.5px;color:var(--t3);font-weight:700;letter-spacing:.08em;display:flex;align-items:center;gap:6px;margin-bottom:10px}
.tml i{color:var(--gold2)}
.tmv{font-size:33px;font-weight:800;background:linear-gradient(135deg,#fdf6d8,#f3d98b 45%,#b07f22);-webkit-background-clip:text;background-clip:text;color:transparent;display:flex;align-items:baseline;gap:6px}
[data-theme="light"] .tmv{background:linear-gradient(135deg,#8a5e0f,#b07f22);-webkit-background-clip:text;background-clip:text}
.tmv span{font-size:14px;font-weight:500;-webkit-text-fill-color:var(--t3);color:var(--t3)}
.trend{display:inline-flex;align-items:center;gap:4px;font-size:11px;font-weight:700;padding:4px 11px;border-radius:20px;margin-top:12px;background:rgba(62,207,142,.1);color:var(--green-t)}
.traf-mini{background:var(--card);border:1px solid var(--bord);border-radius:20px;padding:18px;display:flex;flex-direction:column;justify-content:space-between;transition:.2s}
.traf-mini:hover{border-color:var(--bordH);transform:translateY(-2px)}
.tmi-ic{width:32px;height:32px;border-radius:9px;background:var(--gd);color:var(--gold);display:flex;align-items:center;justify-content:center;font-size:15px;border:1px solid var(--bord);margin-bottom:12px}
.tmv2{font-size:21px;font-weight:800}
.tml2{font-size:9.5px;color:var(--t3);font-weight:700;letter-spacing:.06em;margin-top:4px}
.tcard{margin-bottom:0}
.traf-chart-head{display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;flex-wrap:wrap;gap:10px}
.ct-title{font-size:14px;font-weight:800;display:flex;align-items:center;gap:8px}
.ct-title i{color:var(--gold2)}
.ct-sub{font-size:10.5px;color:var(--t3);margin-top:3px}
.rtabs{display:flex;gap:4px;background:var(--gd);padding:3px;border-radius:10px;border:1px solid var(--bord)}
.rtab{padding:6px 14px;border-radius:8px;font-size:10.5px;font-weight:700;color:var(--t3);cursor:pointer;transition:.15s;border:none;background:transparent;font-family:inherit}
.rtab.on{background:linear-gradient(135deg,#f9ecc0,#c9962f);color:#2a1e05;box-shadow:0 2px 10px rgba(217,168,63,.35)}
.searchrow{display:flex;align-items:center;gap:9px;background:var(--card);border:1px solid var(--bord);border-radius:12px;padding:10px 14px;margin-bottom:14px}
.searchrow input{flex:1;background:none;border:none;outline:none;color:var(--t1);font-family:inherit;font-size:13px}
.searchrow i{color:var(--t3)}
.lclist{display:flex;flex-direction:column;gap:12px}
.lcard{background:var(--card);border:1px solid var(--bord);border-radius:var(--rad);padding:16px 18px;transition:.2s}
.lcard:hover{border-color:var(--bordH)}
.lcard.off{opacity:.55}
.lc-head{display:flex;align-items:center;gap:10px;margin-bottom:11px;flex-wrap:wrap}
.lc-name{font-weight:700;font-size:13.5px;display:flex;align-items:center;gap:8px}
.lc-actions{margin-right:auto;display:flex;gap:6px;flex-wrap:wrap}
.chip{font-size:9.5px;padding:3px 9px;border-radius:20px;background:var(--gd);border:1px solid var(--bord);color:var(--t2);display:inline-flex;align-items:center;gap:4px;font-weight:600;white-space:nowrap}
.chip-gold{color:var(--gold);border-color:rgba(217,168,63,.45)}
.chip-ok{color:var(--green-t);border-color:rgba(62,207,142,.3)}
.chip-exp{color:var(--red-t);border-color:rgba(229,72,77,.3)}
.chip-amb{color:var(--amber-t);border-color:rgba(229,168,62,.35)}
.lc-badges{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:11px}
.lc-usage{margin-bottom:8px}
.ubar{height:6px;border-radius:6px;background:rgba(0,0,0,.45);overflow:hidden;border:1px solid rgba(217,168,63,.12)}
.ubar i{display:block;height:100%;background:linear-gradient(90deg,#a8741f,#d9a83f,#f3d98b);border-radius:6px;transition:width .4s;box-shadow:0 0 8px rgba(217,168,63,.5)}
.utxt{font-size:10.5px;color:var(--t3);margin-top:6px}
.lc-note{font-size:11px;color:var(--t3);margin-top:8px;padding-top:8px;border-top:1px dashed rgba(217,168,63,.14)}
.sicon{width:34px;height:34px;border-radius:10px;background:var(--gd);border:1px solid var(--bord);color:var(--gold);display:flex;align-items:center;justify-content:center;font-size:16px;flex-shrink:0}
.urlrow{display:flex;align-items:center;gap:8px;background:rgba(0,0,0,.35);border:1px solid var(--bord);border-radius:10px;padding:8px 12px;margin-top:8px}
[data-theme="light"] .urlrow{background:rgba(140,100,20,.06)}
.urltext{flex:1;font-family:ui-monospace,monospace;font-size:10.5px;color:var(--gold);direction:ltr;text-align:left;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.tscroll{overflow-x:auto}
.tgrid{min-width:680px}
.thead,.trow{display:grid;grid-template-columns:1.1fr 1.25fr .45fr .75fr .95fr .95fr;gap:8px;align-items:center}
.thead{font-size:9.5px;font-weight:700;color:var(--t3);letter-spacing:.06em;padding:0 10px 10px;border-bottom:1px solid var(--bord)}
.trow{padding:11px 10px;border-bottom:1px solid rgba(217,168,63,.07);font-size:11.5px}
.trow:last-child{border-bottom:none}
.cip{font-family:ui-monospace,monospace;direction:ltr;text-align:right;color:var(--gold);font-weight:600}
.lgrow{display:flex;align-items:center;gap:11px;padding:11px 12px;border-bottom:1px solid rgba(217,168,63,.07);font-size:12px}
.lgrow:last-child{border-bottom:none}
.lgrow>i{width:30px;height:30px;border-radius:9px;background:var(--gd);border:1px solid var(--bord);color:var(--gold);display:flex;align-items:center;justify-content:center;font-size:14px;flex-shrink:0}
.lgrow.err>i{color:var(--red-t);border-color:rgba(229,72,77,.3);background:rgba(229,72,77,.08)}
.lgrow.ok>i{color:var(--green-t);border-color:rgba(62,207,142,.3);background:rgba(62,207,142,.08)}
.lgrow.warn>i{color:var(--amber-t);border-color:rgba(229,168,62,.3);background:rgba(229,168,62,.08)}
.lgmsg{flex:1;color:var(--t1)}
.lgtime{font-size:10px;color:var(--t3);font-family:ui-monospace,monospace;direction:ltr}
.modal{position:fixed;inset:0;background:rgba(3,5,10,.78);backdrop-filter:blur(6px);z-index:300;display:none;align-items:center;justify-content:center;padding:18px}
.modal.show{display:flex}
.modal-card{width:100%;max-width:580px;max-height:88vh;overflow-y:auto;background:linear-gradient(165deg,#13182a,#05070D);border:1px solid var(--bordH);border-radius:20px;padding:22px;box-shadow:0 30px 90px rgba(0,0,0,.8),0 0 40px rgba(217,168,63,.08)}
[data-theme="light"] .modal-card{background:linear-gradient(165deg,#FDFAF4,#EAE0C6)}
.modal-title{font-size:14px;font-weight:800;margin-bottom:16px;display:flex;align-items:center;gap:8px}
.modal-title i{color:var(--gold2)}
.modal-foot{display:flex;gap:8px;margin-top:18px;justify-content:flex-end}
.fgrid{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.fg{display:flex;flex-direction:column;gap:6px}
.fg.full{grid-column:1/-1}
.fg label{font-size:10px;color:var(--t3);font-weight:700;letter-spacing:.05em}
.fg input,.fg select{background:rgba(0,0,0,.42);border:1px solid var(--bord);border-radius:10px;padding:10px 12px;color:var(--t1);font-family:inherit;font-size:12.5px;outline:none;width:100%}
[data-theme="light"] .fg input,[data-theme="light"] .fg select{background:rgba(255,255,255,.78)}
.fg input:focus,.fg select:focus{border-color:rgba(240,205,110,.55)}
select option{background:#0E1420;color:var(--t1)}
[data-theme="light"] select option{background:#FDFAF4;color:#241A05}
.mrow{display:flex;align-items:center;gap:10px;padding:10px 12px;border:1px solid var(--bord);border-radius:10px;margin-bottom:8px;cursor:pointer;font-size:12px}
.mrow input{accent-color:#d9a83f;width:16px;height:16px}
.qrbox{display:flex;flex-direction:column;align-items:center;gap:12px;padding:10px 0}
.qrbox img{width:260px;height:260px;border-radius:14px;border:1px solid var(--bordH);background:#fff;padding:8px}
.tres{margin-top:10px;padding:10px 12px;border-radius:10px;font-size:11.5px;display:none;align-items:center;gap:10px;border:1px solid var(--bord)}
.tres.show{display:flex;flex-wrap:wrap}
.tres.ok{border-color:rgba(62,207,142,.4);color:var(--green-t);background:rgba(62,207,142,.07)}
.tres.bad{border-color:rgba(229,72,77,.4);color:var(--red-t);background:rgba(229,72,77,.07)}
.tres .eg{font-family:ui-monospace,monospace;direction:ltr;font-weight:800;font-size:13px}
#toasts{position:fixed;bottom:18px;left:18px;z-index:400;display:flex;flex-direction:column;gap:8px}
.toast{background:rgba(10,14,24,.96);border:1px solid var(--bordH);color:var(--t1);padding:10px 16px;border-radius:12px;font-size:12px;display:flex;align-items:center;gap:8px;transform:translateY(12px);opacity:0;transition:.25s;box-shadow:0 8px 30px rgba(0,0,0,.6)}
[data-theme="light"] .toast{background:#FDFAF4;border-color:var(--bordH)}
.toast.show{transform:none;opacity:1}
.toast.err{border-color:rgba(229,72,77,.5);color:var(--red-t)}
.toast i{color:var(--gold3)}
.empty{padding:34px;text-align:center;color:var(--t3);font-size:12px}
.main .hb-wrap{opacity:.55;margin:40px 0 4px}
.main .hb-row{max-width:560px;margin:0 auto}
@keyframes spin{to{transform:rotate(360deg)}}
@media(max-width:1080px){.metrics{grid-template-columns:1fr 1fr}.traf-hero{grid-template-columns:1fr 1fr}.g3{grid-template-columns:1fr}}
@media(max-width:860px){
 .sidebar{transform:translateX(100%)}.sidebar.open{transform:none;box-shadow:-20px 0 60px rgba(0,0,0,.6)}
 .sb-close{display:flex}.mob-top{display:flex}
 .main{margin-right:0;padding:70px 14px 30px}.metrics{grid-template-columns:1fr 1fr}.traf-hero{grid-template-columns:1fr}.g2{grid-template-columns:1fr}.fgrid{grid-template-columns:1fr}
}
@media(max-width:520px){.metrics{grid-template-columns:1fr}.ch-lg{height:250px}}
__GOLD_CSS__
</style>
</head>
<body>
<div class="bgfix"></div>
<aside class="sidebar" id="sb">
  <div class="logo">__LOGO_SVG__<div><div class="logo-name">OMID</div><div class="logo-sub">GOLD PANEL</div></div><button class="sb-close" id="sbClose"><i class="ti ti-x"></i></button></div>
  <nav class="nav-wrap">
    <div class="nav-sec">مدیریت</div>
    <a class="nav-it on" data-pg="dash"><i class="ti ti-layout-dashboard"></i>داشبورد</a>
    <a class="nav-it" data-pg="traffic"><i class="ti ti-chart-area-line"></i>ترافیک</a>
    <a class="nav-it" data-pg="links"><i class="ti ti-link"></i>کانفیگ‌ها<span class="nav-badge" id="nbLinks">0</span></a>
    <a class="nav-it" data-pg="subs"><i class="ti ti-users-group"></i>گروه‌های ساب<span class="nav-badge" id="nbSubs">0</span></a>
    <a class="nav-it" data-pg="proxies"><i class="ti ti-world-share"></i>پروکسی‌های خروجی<span class="nav-badge" id="nbProxies">0</span></a>
    <a class="nav-it" data-pg="conns"><i class="ti ti-access-point"></i>اتصالات زنده<span class="nav-badge" id="nbConns">0</span></a>
    <div class="nav-sec">سیستم</div>
    <a class="nav-it" data-pg="logs"><i class="ti ti-history"></i>لاگ فعالیت</a>
    <a class="nav-it" data-pg="settings"><i class="ti ti-settings"></i>تنظیمات</a>
  </nav>
  <div class="sb-foot">
    <a class="btn tg full" style="margin:0 0 8px" href="https://t.me/omiddemon" target="_blank"><i class="ti ti-brand-telegram"></i>کانال پشتیبانی</a>
    <button class="btn btn-d full" style="margin:0" id="btnLogout"><i class="ti ti-logout"></i>خروج</button>
  </div>
</aside>
<div class="overlay" id="ov"></div>
<header class="mob-top">
  <div class="ml">__LOGO_SVG__<span class="mob-title">OMID</span></div>
  <button class="menu-btn" id="sbOpen"><i class="ti ti-menu-2"></i></button>
</header>
<main class="main">

<section class="pg on" id="pg-dash">
  <div class="topbar">
    <div><div class="tb-title"><i class="ti ti-wave-sine"></i>داشبورد</div><div class="tb-sub">نمای کلی سیستم در یک نگاه</div></div>
    <div class="tb-right"><span class="badge"><i class="ti ti-clock"></i><span id="bUptime">--:--:--</span></span><span class="badge" style="color:var(--green-t);border-color:rgba(62,207,142,.3)"><span class="dot dg pulse"></span>آنلاین</span></div>
  </div>
  <div class="metrics">
    <div class="metric"><div class="m-icon"><i class="ti ti-access-point"></i></div><div class="m-val"><span id="mConns">0</span></div><div class="m-label">اتصالات زنده</div></div>
    <div class="metric"><div class="m-icon suc"><i class="ti ti-arrows-exchange"></i></div><div class="m-val"><span id="mTraffic">0</span><span class="m-unit">MB</span></div><div class="m-label">ترافیک کل</div></div>
    <div class="metric"><div class="m-icon amb"><i class="ti ti-link"></i></div><div class="m-val"><span id="mLinks">0</span></div><div class="m-label">کانفیگ فعال / کل</div></div>
    <div class="metric"><div class="m-icon"><i class="ti ti-world-share"></i></div><div class="m-val"><span id="mProxies">0</span></div><div class="m-label">پروکسی خروجی</div></div>
  </div>
  <div class="g3">
    <div class="card"><div class="card-title"><i class="ti ti-chart-bar"></i>ترافیک ساعتی<span class="ml-auto"></span><span class="tb-sub" style="margin:0">MB</span></div><div class="ch-lg"><canvas id="chHourly"></canvas></div></div>
    <div class="card"><div class="card-title"><i class="ti ti-server"></i>وضعیت سیستم</div>
      <div class="sr"><span class="sr-k"><i class="ti ti-world"></i>میزبان</span><span class="sr-v mono" id="sysHost">--</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-arrows-transfer-up"></i>کل درخواست‌ها</span><span class="sr-v" id="sysReq">0</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-alert-triangle"></i>خطاها</span><span class="sr-v" id="sysErr">0</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-versions"></i>نسخه</span><span class="sr-v">OMID v14.0 GOLD</span></div>
    </div>
  </div>
  <div class="card"><div class="card-title"><i class="ti ti-history"></i>آخرین رویدادها</div><div id="dashRecent"></div></div>
</section>

<section class="pg" id="pg-traffic">
  <div class="topbar">
    <div><div class="tb-title"><i class="ti ti-chart-area-line"></i>ترافیک</div><div class="tb-sub">آمار مصرف و پرفورمنس سیستم</div></div>
    <div class="tb-right"><span class="badge"><i class="ti ti-clock"></i><span id="tUp">--</span></span></div>
  </div>
  <div class="traf-hero">
    <div class="traf-main"><div class="tml"><i class="ti ti-arrows-exchange"></i>کل ترافیک منتقل‌شده</div><div class="tmv"><span id="thTraffic">0</span><span>MB</span></div><div class="trend"><i class="ti ti-trending-up"></i>زنده</div></div>
    <div class="traf-mini"><div class="tmi-ic"><i class="ti ti-access-point"></i></div><div class="tmv2" id="thConns">0</div><div class="tml2">اتصالات زنده</div></div>
    <div class="traf-mini"><div class="tmi-ic"><i class="ti ti-arrows-transfer-up"></i></div><div class="tmv2" id="thReq">0</div><div class="tml2">کل درخواست‌ها</div></div>
    <div class="traf-mini"><div class="tmi-ic"><i class="ti ti-alert-triangle"></i></div><div class="tmv2" id="thErr">0</div><div class="tml2">خطاها</div></div>
  </div>
  <div class="card tcard">
    <div class="traf-chart-head">
      <div><div class="ct-title"><i class="ti ti-chart-line"></i>نمودار ترافیک ساعتی</div><div class="ct-sub">بر اساس ساعت تهران</div></div>
      <div class="rtabs"><button class="rtab" data-r="12">۱۲ ساعت</button><button class="rtab on" data-r="24">۲۴ ساعت</button><button class="rtab" data-r="all">همه</button></div>
    </div>
    <div class="ch-lg"><canvas id="chTraffic"></canvas></div>
  </div>
</section>

<section class="pg" id="pg-links">
  <div class="topbar">
    <div><div class="tb-title"><i class="ti ti-link"></i>کانفیگ‌ها</div><div class="tb-sub"><span id="linksCount">0</span> کانفیگ ثبت شده</div></div>
    <div class="tb-right"><button class="btn btn-o" id="btnSubAll"><i class="ti ti-stack-2"></i>کپی همه</button><button class="btn btn-p" id="btnNewLink"><i class="ti ti-plus"></i>کانفیگ جدید</button></div>
  </div>
  <div class="searchrow"><i class="ti ti-search"></i><input id="linkSearch" placeholder="جستجو در کانفیگ‌ها..."></div>
  <div id="linksList" class="lclist"></div>
</section>

<section class="pg" id="pg-subs">
  <div class="topbar">
    <div><div class="tb-title"><i class="ti ti-users-group"></i>گروه‌های ساب</div><div class="tb-sub">لینک ساب حرفه‌ای برای مجموعه‌ای از کانفیگ‌ها</div></div>
    <div class="tb-right"><button class="btn btn-p" id="btnNewSub"><i class="ti ti-plus"></i>گروه جدید</button></div>
  </div>
  <div id="subsList" class="lclist"></div>
</section>

<section class="pg" id="pg-proxies">
  <div class="topbar">
    <div><div class="tb-title"><i class="ti ti-world-share"></i>پروکسی‌های خروجی</div><div class="tb-sub">Multi-IP: خروجی هر کانفیگ از پروکسی اختصاصی خودش (SOCKS5 / HTTP CONNECT)</div></div>
    <div class="tb-right">
      <span class="badge"><i class="ti ti-server"></i>پیش‌فرض سرور: <b id="defProxyName" style="margin-right:4px">—</b></span>
      <button class="btn btn-p" id="btnNewProxy"><i class="ti ti-plus"></i>پروکسی جدید</button>
    </div>
  </div>
  <div class="card" style="margin-bottom:14px;font-size:11.5px;color:var(--t3);line-height:1.9">
    <i class="ti ti-info-circle" style="color:var(--gold2)"></i>
    کانفیگی که پروکسی اختصاصی دارد → ترافیکش از همان پروکسی خارج می‌شود و سایت‌ها <b style="color:var(--gold)">IP پروکسی</b> را می‌بینند.
    کانفیگی که پروکسی ندارد → از «پیش‌فرض سرور» خارج می‌شود (اگر تنظیم شده باشد) وگرنه مستقیم.
    لینک اتصال همیشه روی دامنه‌ی همین پنل می‌ماند؛ فقط مسیر خروجی عوض می‌شود.
  </div>
  <div id="proxiesList" class="lclist"></div>
</section>

<section class="pg" id="pg-conns">
  <div class="topbar">
    <div><div class="tb-title"><i class="ti ti-access-point"></i>اتصالات زنده</div><div class="tb-sub">گروه‌بندی‌شده بر اساس آی‌پی · بروزرسانی خودکار</div></div>
    <div class="tb-right"><span class="badge"><i class="ti ti-world"></i>آی‌پی یکتا: <b id="cCount">0</b></span><span class="badge"><i class="ti ti-plug"></i>اتصال: <b id="cRaw">0</b></span></div>
  </div>
  <div class="card"><div class="tscroll"><div class="tgrid">
    <div class="thead"><div>آی‌پی</div><div>کانفیگ</div><div>سشن</div><div>ترافیک</div><div>خروجی</div><div>آخرین فعالیت</div></div>
    <div id="connsBody"></div>
  </div></div></div>
</section>

<section class="pg" id="pg-logs">
  <div class="topbar">
    <div><div class="tb-title"><i class="ti ti-history"></i>لاگ فعالیت</div><div class="tb-sub">رویدادهای سیستم، ورودها و تغییرات کانفیگ‌ها</div></div>
  </div>
  <div class="card"><div id="logsList"></div></div>
</section>

<section class="pg" id="pg-settings">
  <div class="topbar">
    <div><div class="tb-title"><i class="ti ti-settings"></i>تنظیمات</div><div class="tb-sub">امنیت، پوسته و پشتیبانی</div></div>
  </div>
  <div class="g2">
    <div class="card">
      <div class="card-title"><i class="ti ti-key"></i>تغییر رمز عبور</div>
      <div class="fg" style="margin-bottom:12px"><label>رمز فعلی</label><input type="password" id="pwCur"></div>
      <div class="fg" style="margin-bottom:12px"><label>رمز جدید</label><input type="password" id="pwNew"></div>
      <div class="fg"><label>تکرار رمز جدید</label><input type="password" id="pwNew2"></div>
      <button class="btn btn-p full" id="btnPw" style="margin-top:12px"><i class="ti ti-device-floppy"></i>ذخیره رمز جدید</button>
    </div>
    <div class="card">
      <div class="card-title"><i class="ti ti-palette"></i>پوسته و پشتیبانی</div>
      <button class="btn btn-o full" style="margin:0 0 10px" id="btnTheme"><i class="ti ti-moon"></i>تغییر پوسته (تیره / روشن طلایی)</button>
      <a class="btn tg full" style="margin:0 0 10px" href="https://t.me/omiddemon" target="_blank"><i class="ti ti-brand-telegram"></i>کانال پشتیبانی @omiddemon</a>
      <button class="btn btn-d full" style="margin:0" id="btnLogout2"><i class="ti ti-logout"></i>خروج از حساب</button>
      <div class="sr" style="margin-top:14px"><span class="sr-k"><i class="ti ti-versions"></i>نسخه</span><span class="sr-v">OMID v14.0 — GOLD Edition</span></div>
    </div>
  </div>
</section>

__HEARTBEAT__
</main>

<div class="modal" id="mLink"><div class="modal-card">
  <div class="modal-title"><i class="ti ti-link"></i><span id="mlTitle">کانفیگ جدید</span></div>
  <div class="fgrid">
    <div class="fg full"><label>نام / برچسب</label><input id="fLabel" placeholder="مثلاً کانفیگ طلایی"></div>
    <div class="fg"><label>پروتکل / ترابرد</label><select id="fProto"><option value="vless-ws">VLESS + WebSocket</option><option value="xhttp-packet-up">XHTTP (packet-up)</option><option value="xhttp-stream-up">XHTTP (stream-up)</option></select></div>
    <div class="fg"><label>Fingerprint (uTLS)</label><select id="fFp"><option>chrome</option><option>firefox</option><option>safari</option><option>ios</option><option>android</option><option>edge</option><option>360</option><option>qq</option><option>random</option><option>randomized</option></select></div>
    <div class="fg"><label>ALPN</label><input id="fAlpn" placeholder="پیش‌فرض پروتکل" dir="ltr"></div>
    <div class="fg"><label>پورت</label><input id="fPort" type="number" value="443" dir="ltr"></div>
    <div class="fg"><label>محدودیت حجم</label><div style="display:flex;gap:6px"><input id="fLimit" type="number" placeholder="∞"><select id="fLimitU" style="width:84px"><option>GB</option><option>MB</option><option>KB</option></select></div></div>
    <div class="fg"><label>محدودیت سرعت (Mbps)</label><input id="fSpeed" type="number" placeholder="∞" dir="ltr"></div>
    <div class="fg"><label>محدودیت آی‌پی هم‌زمان</label><input id="fIps" type="number" placeholder="∞" dir="ltr"></div>
    <div class="fg"><label>انقضا (روز)</label><input id="fDays" type="number" placeholder="بدون انقضا" dir="ltr"></div>
    <div class="fg full"><label>پروکسی خروجی (Multi-IP)</label><select id="fProxy"><option value="">خروجی سرور (پیش‌فرض / مستقیم)</option></select></div>
    <div class="fg full"><label>گروه ساب</label><select id="fSub"></select></div>
    <div class="fg full"><label>یادداشت</label><input id="fNote" placeholder="اختیاری"></div>
  </div>
  <div class="modal-foot"><button class="btn btn-o" onclick="closeM('mLink')">انصراف</button><button class="btn btn-p" id="btnSaveLink"><i class="ti ti-device-floppy"></i>ذخیره</button></div>
</div></div>

<div class="modal" id="mSub"><div class="modal-card" style="max-width:480px">
  <div class="modal-title"><i class="ti ti-users-group"></i><span id="msTitle">گروه ساب جدید</span></div>
  <div class="fg" style="margin-bottom:12px"><label>نام گروه</label><input id="sName" placeholder="مثلاً VIP"></div>
  <div class="fg" style="margin-bottom:12px"><label>توضیحات</label><input id="sDesc" placeholder="اختیاری"></div>
  <div class="fg"><label>رمز عبور گروه (اختیاری)</label><input id="sPw" type="password" placeholder="بدون رمز"></div>
  <div class="modal-foot"><button class="btn btn-o" onclick="closeM('mSub')">انصراف</button><button class="btn btn-p" id="btnSaveSub"><i class="ti ti-device-floppy"></i>ذخیره</button></div>
</div></div>

<div class="modal" id="mProxy"><div class="modal-card" style="max-width:500px">
  <div class="modal-title"><i class="ti ti-world-share"></i><span id="mpTitle">پروکسی خروجی جدید</span></div>
  <div class="fgrid">
    <div class="fg"><label>نوع پروکسی</label><select id="pType"><option value="socks5">SOCKS5</option><option value="http">HTTP CONNECT</option></select></div>
    <div class="fg"><label>برچسب</label><input id="pLabel" placeholder="مثلاً فرانسه ۱"></div>
    <div class="fg"><label>هاست / آی‌پی</label><input id="pHost" dir="ltr" placeholder="109.123.249.138"></div>
    <div class="fg"><label>پورت</label><input id="pPort" type="number" dir="ltr" placeholder="10808"></div>
    <div class="fg"><label>یوزرنیم (اختیاری)</label><input id="pUser" dir="ltr" autocomplete="off"></div>
    <div class="fg"><label>رمز عبور (اختیاری)</label><input id="pPass" type="password" dir="ltr" autocomplete="new-password"></div>
  </div>
  <div style="margin-top:12px;font-size:11px;color:var(--t3);line-height:1.8;border:1px dashed var(--bord);border-radius:10px;padding:10px 12px">
    <i class="ti ti-info-circle" style="color:var(--gold)"></i>
    بعد از ذخیره، با دکمه‌ی <b style="color:var(--gold)">تست</b>، IP خروجی واقعی پروکسی را بررسی کنید.
  </div>
  <div class="modal-foot"><button class="btn btn-o" onclick="closeM('mProxy')">انصراف</button><button class="btn btn-p" id="btnSaveProxy"><i class="ti ti-device-floppy"></i>ذخیره</button></div>
</div></div>

<div class="modal" id="mManage"><div class="modal-card">
  <div class="modal-title"><i class="ti ti-adjustments"></i>مدیریت کانفیگ‌های گروه</div>
  <div id="manageList"></div>
  <div class="modal-foot"><button class="btn btn-o" onclick="closeM('mManage')">انصراف</button><button class="btn btn-p" id="btnSaveManage"><i class="ti ti-device-floppy"></i>ذخیره گروه</button></div>
</div></div>

<div class="modal" id="mQr"><div class="modal-card" style="max-width:380px">
  <div class="modal-title"><i class="ti ti-qrcode"></i><span id="qrTitle">QR</span></div>
  <div class="qrbox"><img id="qrImg" alt="QR"><div class="urlrow" style="width:100%"><span class="urltext" id="qrText"></span><button class="btn-icon" onclick="copyEl('qrText')"><i class="ti ti-copy"></i></button></div></div>
  <div class="modal-foot"><button class="btn btn-o" onclick="closeM('mQr')">بستن</button></div>
</div></div>

<div id="toasts"></div>

<script>
const $=s=>document.querySelector(s), $$=s=>document.querySelectorAll(s);
const esc=s=>(s??'').toString().replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function toast(msg,isErr){
  const t=document.createElement('div');t.className='toast'+(isErr?' err':'');
  t.innerHTML=`<i class="ti ${isErr?'ti-alert-circle':'ti-circle-check'}"></i>${esc(msg)}`;
  $('#toasts').appendChild(t);requestAnimationFrame(()=>t.classList.add('show'));
  setTimeout(()=>{t.classList.remove('show');setTimeout(()=>t.remove(),300)},3200);
}
async function jfetch(url,opts){
  const r=await fetch(url,opts);
  if(r.status===401){location.href='/login';throw new Error('unauthorized');}
  const d=await r.json().catch(()=>({}));
  if(!r.ok)throw new Error(d.detail||('خطا '+r.status));
  return d;
}
const jget=u=>jfetch(u);
const jpost=(u,b)=>jfetch(u,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(b||{})});
const jpatch=(u,b)=>jfetch(u,{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify(b||{})});
const jdel=u=>jfetch(u,{method:'DELETE'});
async function copyText(t){
  try{await navigator.clipboard.writeText(t);toast('کپی شد');}
  catch(e){const ta=document.createElement('textarea');ta.value=t;ta.style.position='fixed';ta.style.opacity='0';document.body.appendChild(ta);ta.select();document.execCommand('copy');ta.remove();toast('کپی شد');}
}
function copyEl(id){copyText(document.getElementById(id).textContent);}
function openM(id){document.getElementById(id).classList.add('show');}
function closeM(id){document.getElementById(id).classList.remove('show');}
function fmtTime(iso){if(!iso)return'—';try{const d=new Date(iso);return d.toLocaleTimeString('fa-IR')}catch(e){return'—'}}
function fmtDate(iso){if(!iso)return'—';try{const d=new Date(iso);return d.toLocaleDateString('fa-IR')}catch(e){return'—'}}
let LINKS=[],SUBS=[],PROXIES=[],SETTINGS={},ACTIVITY=[];
let editingLink=null,editingSub=null,editingProxy=null,manageSubId=null;
let hourlyMap=JSON.parse(localStorage.getItem('omid_hourly')||'{}');
let trafficRange='24',trafficChart=null,dashChart=null;
function closeSidebar(){$('#sb').classList.remove('open');$('#ov').classList.remove('show');}
 $('#sbOpen').addEventListener('click',()=>{$('#sb').classList.add('open');$('#ov').classList.add('show');});
 $('#sbClose').addEventListener('click',closeSidebar);
 $('#ov').addEventListener('click',closeSidebar);
 $$('.nav-it').forEach(n=>n.addEventListener('click',()=>{
  const p=n.dataset.pg;
  $$('.nav-it').forEach(x=>x.classList.toggle('on',x===n));
  $$('.pg').forEach(s=>s.classList.toggle('on',s.id==='pg-'+p));
  closeSidebar();refreshPage(p);
}));
function refreshPage(p){
  if(p==='links')loadLinks();
  else if(p==='subs')loadSubs();
  else if(p==='proxies')loadProxies();
  else if(p==='conns')loadConns();
  else if(p==='logs')loadActivity();
}
async function loadStats(){
  try{
    const s=await jget('/stats');
    $('#mConns').textContent=s.active_connections;
    $('#mTraffic').textContent=s.total_traffic_mb;
    $('#mLinks').textContent=s.active_links+' / '+s.links_count;
    $('#mProxies').textContent=s.proxies_count||0;
    $('#bUptime').textContent=s.uptime;$('#tUp').textContent=s.uptime;
    $('#sysReq').textContent=s.total_requests;$('#sysErr').textContent=s.total_errors;
    $('#thTraffic').textContent=s.total_traffic_mb;$('#thConns').textContent=s.active_connections;
    $('#thReq').textContent=s.total_requests;$('#thErr').textContent=s.total_errors;
    $('#sysHost').textContent=location.hostname||'--';
    for(const k in (s.hourly||{}))hourlyMap[k]=Math.max(hourlyMap[k]||0,s.hourly[k]);
    const keys=Object.keys(hourlyMap).sort();
    if(keys.length>96){keys.slice(0,keys.length-96).forEach(k=>delete hourlyMap[k]);}
    localStorage.setItem('omid_hourly',JSON.stringify(hourlyMap));
    renderTrafficChart();renderDashChart();
  }catch(e){}
}
function chartData(n){
  let keys=Object.keys(hourlyMap).sort();
  if(n!=='all')keys=keys.slice(-parseInt(n));
  return{labels:keys.map(k=>k),values:keys.map(k=>Math.round(hourlyMap[k]/1048576*100)/100)};
}
function baseChart(ctx,label){
  return new Chart(ctx,{type:'line',data:{labels:[],datasets:[{label,label,data:[],borderColor:'#f3d98b',backgroundColor:'rgba(217,168,63,.14)',fill:true,tension:.35,pointRadius:0,borderWidth:2.2}]},
    options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{x:{ticks:{color:'#8D8368',font:{size:9},maxTicksLimit:12},grid:{color:'rgba(217,168,63,.07)'}},y:{beginAtZero:true,ticks:{color:'#8D8368',font:{size:9}},grid:{color:'rgba(217,168,63,.07)'}}}}});
}
function renderTrafficChart(){
  const cv=document.getElementById('chTraffic');if(!cv)return;
  if(!trafficChart)trafficChart=baseChart(cv.getContext('2d'),'MB');
  const d=chartData(trafficRange);
  trafficChart.data.labels=d.labels;trafficChart.data.datasets[0].data=d.values;trafficChart.update('none');
}
function renderDashChart(){
  const cv=document.getElementById('chHourly');if(!cv)return;
  if(!dashChart)dashChart=baseChart(cv.getContext('2d'),'MB');
  const d=chartData('24');
  dashChart.data.labels=d.labels;dashChart.data.datasets[0].data=d.values;dashChart.update('none');
}
 $$('.rtab').forEach(b=>b.addEventListener('click',()=>{
  $$('.rtab').forEach(x=>x.classList.toggle('on',x===b));
  trafficRange=b.dataset.r;renderTrafficChart();
}));
async function loadLinks(){
  try{
    const d=await jget('/api/links');LINKS=d.links||[];
    $('#nbLinks').textContent=LINKS.length;
    $('#linksCount').textContent=LINKS.length;
    renderLinks();fillSubSelects();
  }catch(e){}
}
function protoName(p){return{'vless-ws':'WS','xhttp-packet-up':'XHTTP·PU','xhttp-stream-up':'XHTTP·SU','xhttp-stream-one':'XHTTP·SO'}[p]||p;}
function renderLinks(){
  const q=(($('#linkSearch').value||'').toLowerCase());
  const list=LINKS.filter(l=>!q||(l.label||'').toLowerCase().includes(q)||(l.note||'').toLowerCase().includes(q));
  const box=$('#linksList');
  if(!list.length){box.innerHTML='<div class="empty">کانفیگی ثبت نشده — دکمه «کانفیگ جدید» را بزنید</div>';return;}
  box.innerHTML=list.map(l=>{
    const pct=l.limit_bytes>0?Math.min(100,(l.used_bytes/l.limit_bytes*100)):0;
    const off=!l.active||l.expired;
    const proxyChip=PROXIES.length?`<span class="chip chip-gold"><i class="ti ti-world-share"></i>${esc(l.proxy_label||'خروجی سرور')}</span>`:'';
    return`<div class="lcard ${off?'off':''}">
      <div class="lc-head">
        <div class="sicon"><i class="ti ti-link"></i></div>
        <div class="lc-name">${esc(l.label)}${l.is_default?' <span class="chip chip-gold">پیش‌فرض</span>':''}</div>
        <div class="lc-actions">
          <button class="btn-icon" title="QR" onclick="qrLink('${l.uuid}')"><i class="ti ti-qrcode"></i></button>
          <button class="btn-icon" title="کپی لینک اتصال" onclick="copyVless('${l.uuid}')"><i class="ti ti-copy"></i></button>
          <button class="btn-icon" title="کپی لینک ساب" onclick="copySub('${l.uuid}')"><i class="ti ti-cloud-download"></i></button>
          <button class="btn-icon" title="ویرایش" onclick="editLink('${l.uuid}')"><i class="ti ti-pencil"></i></button>
          <button class="btn-icon" title="${l.active?'غیرفعال':'فعال'}" onclick="toggleLink('${l.uuid}')"><i class="ti ${l.active?'ti-player-pause':'ti-player-play'}"></i></button>
          <button class="btn-icon" title="ریست مصرف" onclick="resetLink('${l.uuid}')"><i class="ti ti-rotate"></i></button>
          <button class="btn-icon danger" title="حذف" onclick="delLink('${l.uuid}')"><i class="ti ti-trash"></i></button>
        </div>
      </div>
      <div class="lc-badges">
        <span class="chip ${l.active?'chip-ok':'chip-exp'}"><i class="ti ${l.active?'ti-circle-check':'ti-circle-x'}"></i>${l.active?'فعال':'غیرفعال'}</span>
        ${l.expired?'<span class="chip chip-exp"><i class="ti ti-calendar-x"></i>منقضی</span>':''}
        <span class="chip"><i class="ti ti-topology-star"></i>${esc(protoName(l.protocol))}</span>
        <span class="chip"><i class="ti ti-plug"></i>${esc(l.port)}</span>
        ${l.ip_limit>0?`<span class="chip chip-amb"><i class="ti ti-users"></i>${l.ip_limit} IP</span>`:''}
        ${l.speed_limit_bytes>0?`<span class="chip chip-amb"><i class="ti ti-gauge"></i>${Math.round(l.speed_limit_bytes*8/1048576)}Mbps</span>`:''}
        ${l.sub_id?`<span class="chip"><i class="ti ti-users-group"></i>${esc(subName(l.sub_id))}</span>`:''}
        ${proxyChip}
        <span class="chip"><i class="ti ti-access-point"></i>${l.connected_ips||0} آی‌پی متصل</span>
      </div>
      <div class="lc-usage"><div class="ubar"><i style="width:${pct}%"></i></div>
      <div class="utxt">${esc(l.used_fmt||fmtB(l.used_bytes))} از ${l.limit_bytes>0?esc(l.limit_fmt||fmtB(l.limit_bytes)):'∞'}${l.expires_at?' · انقضا: '+fmtDate(l.expires_at):''}</div></div>
      ${l.note?`<div class="lc-note">${esc(l.note)}</div>`:''}
    </div>`;
  }).join('');
}
function fmtB(b){if(b<1024)return b+' B';if(b<1048576)return(b/1024).toFixed(1)+' KB';if(b<1073741824)return(b/1048576).toFixed(2)+' MB';return(b/1073741824).toFixed(2)+' GB';}
function subName(id){const s=SUBS.find(x=>x.sub_id===id);return s?s.name:'—';}
 $('#linkSearch').addEventListener('input',renderLinks);
function fillSubSelects(){
  const sel=$('#fSub');const cur=sel.value;
  sel.innerHTML='<option value="">— بدون گروه —</option>'+SUBS.map(s=>`<option value="${s.sub_id}">${esc(s.name)}</option>`).join('');
  sel.value=cur;
  const psel=$('#fProxy');const pcur=psel.value;
  psel.innerHTML='<option value="">خروجی سرور (پیش‌فرض / مستقیم)</option>'+PROXIES.filter(p=>p.active).map(p=>`<option value="${p.proxy_id}">${esc(p.label)} (${p.type.toUpperCase()})</option>`).join('');
  psel.value=pcur;
}
window.qrLink=id=>{const l=LINKS.find(x=>x.uuid===id);if(!l)return;showQr(l.vless_link,l.label);};
window.copyVless=id=>{const l=LINKS.find(x=>x.uuid===id);if(l)copyText(l.vless_link);};
window.copySub=id=>{const l=LINKS.find(x=>x.uuid===id);if(l)copyText(l.sub_url);};
function showQr(text,title){
  $('#qrTitle').textContent=title||'QR';
  $('#qrImg').src='https://api.qrserver.com/v1/create-qr-code/?size=300x300&data='+encodeURIComponent(text);
  $('#qrText').textContent=text;openM('mQr');
}
 $('#btnNewLink').addEventListener('click',()=>{
  editingLink=null;$('#mlTitle').textContent='کانفیگ جدید';
  ['fLabel','fAlpn','fNote'].forEach(i=>$('#'+i).value='');
  $('#fProto').value='vless-ws';$('#fFp').value='chrome';$('#fPort').value=443;
  $('#fLimit').value='';$('#fLimitU').value='GB';$('#fSpeed').value='';$('#fIps').value='';$('#fDays').value='';
  fillSubSelects();$('#fProxy').value='';openM('mLink');
});
window.editLink=id=>{
  const l=LINKS.find(x=>x.uuid===id);if(!l)return;
  editingLink=id;$('#mlTitle').textContent='ویرایش کانفیگ';
  $('#fLabel').value=l.label||'';$('#fProto').value=l.protocol||'vless-ws';
  $('#fFp').value=l.fingerprint||'chrome';$('#fAlpn').value=l.alpn||'';$('#fPort').value=l.port||443;
  $('#fSpeed').value=l.speed_limit_bytes?Math.round(l.speed_limit_bytes*8/1048576):'';
  $('#fIps').value=l.ip_limit||'';$('#fNote').value=l.note||'';
  if(l.limit_bytes>0){
    if(l.limit_bytes>=1073741824){$('#fLimit').value=+(l.limit_bytes/1073741824).toFixed(2);$('#fLimitU').value='GB';}
    else if(l.limit_bytes>=1048576){$('#fLimit').value=+(l.limit_bytes/1048576).toFixed(2);$('#fLimitU').value='MB';}
    else{$('#fLimit').value=Math.round(l.limit_bytes/1024);$('#fLimitU').value='KB';}
  }else{$('#fLimit').value='';$('#fLimitU').value='GB';}
  $('#fDays').value='';
  fillSubSelects();$('#fSub').value=l.sub_id||'';$('#fProxy').value=l.proxy_id||'';
  openM('mLink');
};
 $('#btnSaveLink').addEventListener('click',async()=>{
  const body={
    label:$('#fLabel').value.trim()||'لینک جدید',
    protocol:$('#fProto').value,fingerprint:$('#fFp').value,
    alpn:$('#fAlpn').value.trim(),port:parseInt($('#fPort').value)||443,
    limit_value:parseFloat($('#fLimit').value)||0,limit_unit:$('#fLimitU').value,
    speed_limit_value:parseFloat($('#fSpeed').value)||0,speed_limit_unit:'MBIT',
    ip_limit:parseInt($('#fIps').value)||0,
    expires_days:parseInt($('#fDays').value)||0,
    note:$('#fNote').value.trim(),
    sub_id:$('#fSub').value||null,
    proxy_id:$('#fProxy').value||null,
  };
  try{
    if(editingLink)await jpatch('/api/links/'+editingLink,body);
    else await jpost('/api/links',body);
    closeM('mLink');toast('ذخیره شد');loadLinks();
  }catch(e){toast(e.message,true);}
});
window.toggleLink=async id=>{
  const l=LINKS.find(x=>x.uuid===id);if(!l)return;
  try{await jpatch('/api/links/'+id,{active:!l.active});loadLinks();}catch(e){toast(e.message,true);}
};
window.resetLink=async id=>{
  try{await jpatch('/api/links/'+id,{reset_usage:true});toast('مصرف ریست شد');loadLinks();}catch(e){toast(e.message,true);}
};
window.delLink=async id=>{
  const l=LINKS.find(x=>x.uuid===id);if(!l)return;
  if(!confirm(`حذف کانفیگ «${l.label}»؟`))return;
  try{await jdel('/api/links/'+id);toast('حذف شد');loadLinks();}catch(e){toast(e.message,true);}
};
 $('#btnSubAll').addEventListener('click',()=>{
  const txt=LINKS.filter(l=>l.active&&!l.expired).map(l=>l.vless_link).join('\n');
  if(!txt){toast('کانفیگ فعالی نیست',true);return;}
  copyText(txt);
});
async function loadSubs(){
  try{
    const d=await jget('/api/subs');SUBS=d.subs||[];
    $('#nbSubs').textContent=SUBS.length;
    renderSubs();fillSubSelects();
  }catch(e){}
}
function renderSubs(){
  const box=$('#subsList');
  if(!SUBS.length){box.innerHTML='<div class="empty">گروهی ساخته نشده</div>';return;}
  box.innerHTML=SUBS.map(s=>`<div class="lcard">
    <div class="lc-head">
      <div class="sicon"><i class="ti ti-users-group"></i></div>
      <div class="lc-name">${esc(s.name)}</div>
      <div class="lc-actions">
        <a class="btn-icon" title="صفحه عمومی" href="${s.public_url}" target="_blank"><i class="ti ti-external-link"></i></a>
        <button class="btn-icon" title="کپی لینک ساب" onclick="copyText('${s.sub_url}')"><i class="ti ti-copy"></i></button>
        <button class="btn-icon" title="QR ساب" onclick="qrSub('${s.sub_id}')"><i class="ti ti-qrcode"></i></button>
        <button class="btn-icon" title="مدیریت کانفیگ‌ها" onclick="openManage('${s.sub_id}')"><i class="ti ti-adjustments"></i></button>
        <button class="btn-icon" title="ویرایش" onclick="editSub('${s.sub_id}')"><i class="ti ti-pencil"></i></button>
        <button class="btn-icon danger" title="حذف" onclick="delSub('${s.sub_id}')"><i class="ti ti-trash"></i></button>
      </div>
    </div>
    <div class="lc-badges">
      ${s.has_password?'<span class="chip chip-amb"><i class="ti ti-lock"></i>رمزدار</span>':''}
      <span class="chip"><i class="ti ti-link"></i>${s.links_count} کانفیگ</span>
      <span class="chip chip-ok"><i class="ti ti-circle-check"></i>${s.active_count} فعال</span>
      <span class="chip"><i class="ti ti-arrows-exchange"></i>${esc(s.total_used_fmt)}</span>
    </div>
    ${s.desc?`<div class="lc-note">${esc(s.desc)}</div>`:''}
  </div>`).join('');
}
window.qrSub=id=>{const s=SUBS.find(x=>x.sub_id===id);if(s)showQr(s.sub_url,'ساب '+s.name);};
 $('#btnNewSub').addEventListener('click',()=>{
  editingSub=null;$('#msTitle').textContent='گروه ساب جدید';
  $('#sName').value='';$('#sDesc').value='';$('#sPw').value='';openM('mSub');
});
window.editSub=id=>{
  const s=SUBS.find(x=>x.sub_id===id);if(!s)return;
  editingSub=id;$('#msTitle').textContent='ویرایش گروه';
  $('#sName').value=s.name;$('#sDesc').value=s.desc||'';$('#sPw').value='';
  openM('mSub');
};
 $('#btnSaveSub').addEventListener('click',async()=>{
  const body={name:$('#sName').value.trim()||'گروه جدید',desc:$('#sDesc').value.trim()};
  const pw=$('#sPw').value;
  if(pw||!editingSub)body.password=pw;
  try{
    if(editingSub)await jpatch('/api/subs/'+editingSub,body);
    else await jpost('/api/subs',body);
    closeM('mSub');toast('ذخیره شد');loadSubs();
  }catch(e){toast(e.message,true);}
});
window.delSub=async id=>{
  const s=SUBS.find(x=>x.sub_id===id);if(!s)return;
  if(!confirm(`حذف گروه «${s.name}»؟`))return;
  try{await jdel('/api/subs/'+id);toast('حذف شد');loadSubs();}catch(e){toast(e.message,true);}
};
window.openManage=async id=>{
  manageSubId=id;const s=SUBS.find(x=>x.sub_id===id);if(!s)return;
  const box=$('#manageList');
  box.innerHTML=LINKS.map(l=>`<label class="mrow"><input type="checkbox" data-lid="${l.uuid}" ${s.link_ids.includes(l.uuid)?'checked':''}><span>${esc(l.label)}</span></label>`).join('')||'<div class="empty">کانفیگی نیست</div>';
  openM('mManage');
};
 $('#btnSaveManage').addEventListener('click',async()=>{
  const s=SUBS.find(x=>x.sub_id===manageSubId);if(!s)return;
  try{
    const wanted=[...$$('#manageList input:checked')].map(i=>i.dataset.lid);
    for(const lid of wanted)if(!s.link_ids.includes(lid))await jpost(`/api/subs/${manageSubId}/links`,{link_id:lid,action:'add'});
    for(const lid of s.link_ids)if(!wanted.includes(lid))await jpost(`/api/subs/${manageSubId}/links`,{link_id:lid,action:'remove'});
    closeM('mManage');toast('گروه بروزرسانی شد');loadSubs();
  }catch(e){toast(e.message,true);}
});
async function loadProxies(){
  try{
    const [pd,sd]=await Promise.all([jget('/api/proxies'),jget('/api/settings')]);
    PROXIES=pd.proxies||[];SETTINGS=sd||{};
    $('#nbProxies').textContent=PROXIES.length;
    $('#defProxyName').textContent=SETTINGS.default_proxy_label||'—';
    renderProxies();fillSubSelects();
  }catch(e){}
}
function renderProxies(){
  const box=$('#proxiesList');
  if(!PROXIES.length){box.innerHTML='<div class="empty">پروکسی‌ای ثبت نشده — دکمه «پروکسی جدید» را بزنید</div>';return;}
  box.innerHTML=PROXIES.map(p=>`<div class="lcard ${p.active?'':'off'}">
    <div class="lc-head">
      <div class="sicon"><i class="ti ${p.type==='http'?'ti-world':'ti-topology-star-3'}"></i></div>
      <div class="lc-name">${esc(p.label)}</div>
      <div class="lc-actions">
        <button class="btn-icon" title="تست IP خروجی" onclick="testProxy('${p.proxy_id}')" id="tb-${p.proxy_id}"><i class="ti ti-bolt"></i></button>
        <button class="btn-icon" title="${p.is_default?'حذف پیش‌فرض':'تنظیم به‌عنوان پیش‌فرض سرور'}" onclick="defProxy('${p.proxy_id}')"><i class="ti ${p.is_default?'ti-star-filled':'ti-star'}"></i></button>
        <button class="btn-icon" title="ویرایش" onclick="editProxy('${p.proxy_id}')"><i class="ti ti-pencil"></i></button>
        <button class="btn-icon" title="${p.active?'غیرفعال':'فعال'}" onclick="toggleProxy('${p.proxy_id}')"><i class="ti ${p.active?'ti-player-pause':'ti-player-play'}"></i></button>
        <button class="btn-icon danger" title="حذف" onclick="delProxy('${p.proxy_id}')"><i class="ti ti-trash"></i></button>
      </div>
    </div>
    <div class="lc-badges">
      <span class="chip chip-gold"><i class="ti ti-topology-star"></i>${esc(p.type.toUpperCase())}</span>
      <span class="chip mono"><i class="ti ti-plug"></i>${esc(p.host)}:${esc(p.port)}</span>
      ${p.username?'<span class="chip chip-ok"><i class="ti ti-key"></i>احراز هویت</span>':'<span class="chip"><i class="ti ti-lock-open"></i>بدون رمز</span>'}
      <span class="chip"><i class="ti ti-link"></i>${p.used_by||0} کانفیگ</span>
      ${p.is_default?'<span class="chip chip-ok"><i class="ti ti-star-filled"></i>پیش‌فرض سرور</span>':''}
      ${p.active?'':'<span class="chip chip-exp">غیرفعال</span>'}
    </div>
    <div class="urlrow"><span class="urltext">${esc(p.type)}://${esc(p.host)}:${esc(p.port)}</span>
      <button class="btn-icon" onclick="copyText('${esc(p.host)}:${esc(p.port)}')"><i class="ti ti-copy"></i></button></div>
    <div class="tres" id="tres-${p.proxy_id}"></div>
  </div>`).join('');
}
 $('#btnNewProxy').addEventListener('click',()=>{
  editingProxy=null;$('#mpTitle').textContent='پروکسی خروجی جدید';
  $('#pType').value='socks5';$('#pLabel').value='';$('#pHost').value='';$('#pPort').value='';$('#pUser').value='';$('#pPass').value='';
  openM('mProxy');setTimeout(()=>$('#pHost').focus(),80);
});
window.editProxy=id=>{
  const p=PROXIES.find(x=>x.proxy_id===id);if(!p)return;
  editingProxy=id;$('#mpTitle').textContent='ویرایش پروکسی';
  $('#pType').value=p.type;$('#pLabel').value=p.label;$('#pHost').value=p.host;$('#pPort').value=p.port;
  $('#pUser').value=p.username||'';$('#pPass').value=p.password||'';
  openM('mProxy');
};
 $('#btnSaveProxy').addEventListener('click',async()=>{
  const body={
    type:$('#pType').value,label:$('#pLabel').value.trim(),
    host:$('#pHost').value.trim(),port:parseInt($('#pPort').value)||0,
    username:$('#pUser').value.trim(),password:$('#pPass').value,
  };
  if(!body.host||!(body.port>=1&&body.port<=65535)){toast('هاست و پورت معتبر وارد کنید',true);return;}
  try{
    if(editingProxy)await jpatch('/api/proxies/'+editingProxy,body);
    else await jpost('/api/proxies',body);
    closeM('mProxy');toast('ذخیره شد');loadProxies();
  }catch(e){toast(e.message,true);}
});
window.testProxy=async id=>{
  const btn=document.getElementById('tb-'+id);const res=document.getElementById('tres-'+id);
  if(btn){btn.disabled=true;btn.innerHTML='<i class="ti ti-loader-2" style="animation:spin 1s linear infinite"></i>';}
  if(res){res.className='tres show';res.innerHTML='<i class="ti ti-loader-2" style="animation:spin 1s linear infinite"></i> در حال تست از داخل تونل پروکسی...';}
  try{
    const r=await jpost(`/api/proxies/${id}/test`);
    if(res){
      if(r.ok){res.className='tres show ok';res.innerHTML=`<i class="ti ti-circle-check"></i> خروجی واقعی: <span class="eg">${esc(r.egress_ip)}</span> <span class="chip chip-ok">${r.latency_ms} ms</span>`;}
      else{res.className='tres show bad';res.innerHTML=`<i class="ti ti-alert-triangle"></i> ناموفق: ${esc(r.error)} <span class="chip">${r.latency_ms} ms</span>`;}
    }
  }catch(e){if(res){res.className='tres show bad';res.innerHTML='<i class="ti ti-alert-triangle"></i> '+esc(e.message);}}
  if(btn){btn.disabled=false;btn.innerHTML='<i class="ti ti-bolt"></i>';}
};
window.defProxy=async id=>{
  try{
    const p=PROXIES.find(x=>x.proxy_id===id);
    const nv=(p&&p.is_default)?null:id;
    await jpatch('/api/settings',{default_proxy_id:nv});
    toast(nv?'پیش‌فرض سرور تنظیم شد':'پیش‌فرض سرور حذف شد');loadProxies();
  }catch(e){toast(e.message,true);}
};
window.toggleProxy=async id=>{
  const p=PROXIES.find(x=>x.proxy_id===id);if(!p)return;
  try{await jpatch('/api/proxies/'+id,{active:!p.active});loadProxies();}catch(e){toast(e.message,true);}
};
window.delProxy=async id=>{
  const p=PROXIES.find(x=>x.proxy_id===id);if(!p)return;
  if(!confirm(`حذف پروکسی «${p.label}»؟ کانفیگ‌های متصل به حالت خروجی سرور برمی‌گردند.`))return;
  try{await jdel('/api/proxies/'+id);toast('حذف شد');loadProxies();loadLinks();}catch(e){toast(e.message,true);}
};
async function loadConns(){
  try{
    const d=await jget('/api/connections');
    $('#nbConns').textContent=d.count;
    $('#cCount').textContent=d.count;$('#cRaw').textContent=d.raw_count;
    const box=$('#connsBody');
    if(!(d.connections||[]).length){box.innerHTML='<div class="empty" style="grid-column:1/-1">اتصال فعالی وجود ندارد</div>';return;}
    box.innerHTML=d.connections.map(c=>`<div class="trow">
      <div class="cip">${esc(c.ip)}</div>
      <div>${esc(c.label)}</div>
      <div>${c.sessions}</div>
      <div class="mono">${esc(c.bytes_fmt)}</div>
      <div style="font-size:10.5px;color:var(--gold)">${esc((c.proxies||['مستقیم']).join(' · '))}</div>
      <div class="mono" style="font-size:10px;color:var(--t3)">${fmtTime(c.last_connected_at)}</div>
    </div>`).join('');
  }catch(e){}
}
function logRow(l){
  const ic={'ok':'ti-circle-check','err':'ti-alert-triangle','warn':'ti-alert-circle','info':'ti-info-circle','connection':'ti-access-point','link':'ti-link','sub':'ti-users-group','auth':'ti-key','proxy':'ti-world-share','system':'ti-server'}[l.kind]||'ti-point';
  return`<div class="lgrow ${l.level==='err'?'err':l.level==='ok'?'ok':l.level==='warn'?'warn':''}"><i class="ti ${ic}"></i><span class="lgmsg">${esc(l.message)}</span><span class="lgtime">${fmtTime(l.time)}</span></div>`;
}
async function loadActivity(){
  try{
    const d=await jget('/api/activity');ACTIVITY=d.logs||[];
    $('#logsList').innerHTML=ACTIVITY.slice().reverse().map(logRow).join('')||'<div class="empty">لاگی ثبت نشده</div>';
    $('#dashRecent').innerHTML=ACTIVITY.slice(-8).reverse().map(logRow).join('')||'<div class="empty">—</div>';
  }catch(e){}
}
 $('#btnPw').addEventListener('click',async()=>{
  const a=$('#pwCur').value,b=$('#pwNew').value,c=$('#pwNew2').value;
  if(!a||!b){toast('همه فیلدها را پر کنید',true);return;}
  if(b!==c){toast('تکرار رمز مطابقت ندارد',true);return;}
  try{await jpost('/api/change-password',{current_password:a,new_password:b});toast('رمز تغییر کرد');$('#pwCur').value=$('#pwNew').value=$('#pwNew2').value='';}
  catch(e){toast(e.message,true);}
});
 $('#btnTheme').addEventListener('click',()=>{
  const cur=document.documentElement.getAttribute('data-theme')==='light'?'dark':'light';
  document.documentElement.setAttribute('data-theme',cur);
  localStorage.setItem('omid_theme',cur);
});
if(localStorage.getItem('omid_theme')==='light')document.documentElement.setAttribute('data-theme','light');
async function doLogout(){try{await jpost('/api/logout');}catch(e){}location.href='/login';}
 $('#btnLogout').addEventListener('click',doLogout);
 $('#btnLogout2').addEventListener('click',doLogout);
loadLinks();loadSubs();loadProxies();loadActivity();loadStats();loadConns();
setInterval(loadStats,4000);
setInterval(loadConns,5000);
setInterval(loadActivity,15000);
setInterval(()=>{if(!$('#pg-links').classList.contains('on'))loadLinks();},12000);
</script>
</body></html>"""

# ═══════════════════════════ صفحه عمومی گروه ساب — طلایی ═══════════════════════════
_PUBLIC_TPL = r"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ساب · OMID</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800&family=Cinzel:wght@700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#05070D;--gold:#f3d98b;--gold2:#d9a83f;--gold3:#fdf3c8;--bord:rgba(217,168,63,.18);--bordH:rgba(240,205,110,.45);--gd:rgba(217,168,63,.08);--t1:#F4EEDC;--t2:#C9B98F;--t3:#8D8368;--green-t:#7DDFA8;--red-t:#FF7B72;--amber-t:#FFB35C}
html,body{min-height:100%}
body{font-family:'Vazirmatn',sans-serif;background:radial-gradient(900px 500px at 50% -10%,rgba(217,168,63,.08),transparent 60%),var(--bg);color:var(--t1);padding:20px 14px 40px}
.grid{position:fixed;inset:0;background-image:linear-gradient(rgba(217,168,63,.04) 1px,transparent 1px),linear-gradient(90deg,rgba(217,168,63,.04) 1px,transparent 1px);background-size:44px 44px;-webkit-mask-image:radial-gradient(ellipse 70% 60% at 50% 30%,#000 30%,transparent 75%);mask-image:radial-gradient(ellipse 70% 60% at 50% 30%,#000 30%,transparent 75%);z-index:0;pointer-events:none}
.wrap{position:relative;z-index:2;max-width:680px;margin:0 auto}
.head{text-align:center;margin:18px 0 22px}
.head .omid-logo{width:86px;height:86px;margin:0 auto 8px}
.brand-name{font-family:'Cinzel',serif;font-size:19px;font-weight:900;letter-spacing:.3em;text-indent:.3em;background:linear-gradient(180deg,#fdf6d8,#f3d98b 45%,#b07f22);-webkit-background-clip:text;background-clip:text;color:transparent}
.gname{font-size:19px;font-weight:800;margin-top:12px}
.gdesc{font-size:12px;color:var(--t2);margin-top:5px}
.statrow{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin:16px 0 6px}
.sbadge{font-size:11px;padding:6px 14px;border-radius:20px;border:1px solid var(--bord);background:var(--gd);color:var(--gold);font-weight:700;display:inline-flex;align-items:center;gap:6px}
.subbtns{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin:14px 0 22px}
.btn{font-family:inherit;font-size:12.5px;font-weight:700;border-radius:11px;padding:10px 18px;cursor:pointer;border:none;display:inline-flex;align-items:center;gap:7px;transition:.18s;text-decoration:none}
.btn-p{background:linear-gradient(135deg,#f9ecc0,#eccb7a 46%,#c9962f);color:#2a1e05;box-shadow:0 6px 22px rgba(217,168,63,.32)}
.btn-o{background:transparent;border:1px solid var(--bord);color:var(--t2)}
.btn-o:hover{border-color:var(--bordH);color:var(--gold)}
.lcard{background:rgba(14,18,30,.72);border:1px solid var(--bord);border-radius:16px;padding:15px 17px;margin-bottom:12px;backdrop-filter:blur(10px);transition:.2s}
.lcard:hover{border-color:var(--bordH)}
.lcard.off{opacity:.55}
.lc-head{display:flex;align-items:center;gap:9px;margin-bottom:9px;flex-wrap:wrap}
.lc-name{font-weight:700;font-size:13.5px}
.lc-actions{margin-right:auto;display:flex;gap:6px}
.chip{font-size:9.5px;padding:3px 9px;border-radius:20px;background:var(--gd);border:1px solid var(--bord);color:var(--t2);display:inline-flex;align-items:center;gap:4px;font-weight:600;white-space:nowrap}
.chip-ok{color:var(--green-t);border-color:rgba(62,207,142,.3)}
.chip-exp{color:var(--red-t);border-color:rgba(229,72,77,.3)}
.chip-amb{color:var(--amber-t);border-color:rgba(229,168,62,.35)}
.chip-gold{color:var(--gold);border-color:rgba(217,168,63,.45)}
.ubar{height:6px;border-radius:6px;background:rgba(0,0,0,.45);overflow:hidden;border:1px solid rgba(217,168,63,.12)}
.ubar i{display:block;height:100%;background:linear-gradient(90deg,#a8741f,#d9a83f,#f3d98b);border-radius:6px;transition:width .4s}
.utxt{font-size:10.5px;color:var(--t3);margin-top:6px}
.qr{display:none;margin-top:12px;text-align:center}
.qr.show{display:block}
.qr img{width:230px;height:230px;border-radius:12px;border:1px solid var(--bordH);background:#fff;padding:7px}
.bicon{width:32px;height:32px;padding:0;border-radius:9px;background:var(--gd);color:var(--gold);border:1px solid var(--bord);display:inline-flex;align-items:center;justify-content:center;cursor:pointer;font-size:14px}
.bicon:hover{border-color:var(--bordH)}
.gate{max-width:360px;margin:60px auto;background:rgba(14,18,30,.8);border:1px solid var(--bord);border-radius:18px;padding:26px;text-align:center;backdrop-filter:blur(10px)}
.gate i{font-size:34px;color:var(--gold2)}
.gate h2{font-size:15px;margin:10px 0 16px}
.gate input{width:100%;padding:12px;border-radius:11px;border:1px solid var(--bord);background:rgba(0,0,0,.45);color:var(--t1);font-family:inherit;text-align:center;outline:none;margin-bottom:12px}
.gate input:focus{border-color:rgba(240,205,110,.55)}
.gate .btn{width:100%;justify-content:center}
.gerr{color:var(--red-t);font-size:11.5px;margin-top:9px;display:none}
.foot{text-align:center;font-size:10.5px;color:var(--t3);margin-top:26px}
.foot a{color:var(--gold);font-weight:700;text-decoration:none}
.empty{text-align:center;color:var(--t3);padding:30px;font-size:12.5px}
#toasts{position:fixed;bottom:16px;left:16px;z-index:99;display:flex;flex-direction:column;gap:8px}
.toast{background:rgba(10,14,24,.96);border:1px solid var(--bordH);color:var(--t1);padding:9px 15px;border-radius:11px;font-size:12px;opacity:0;transform:translateY(10px);transition:.25s}
.toast.show{opacity:1;transform:none}
.toast.err{border-color:rgba(229,72,77,.5);color:var(--red-t)}
</style>
</head>
<body>
<div class="grid"></div>
<div class="wrap">
  <div class="head">
    __LOGO_SVG__
    <div class="brand-name">OMID</div>
    <div class="gname" id="gname">—</div>
    <div class="gdesc" id="gdesc"></div>
    <div class="statrow" id="statrow"></div>
  </div>
  <div class="subbtns" id="subbtns" style="display:none">
    <a class="btn btn-p" id="dlSub" target="_blank"><i class="ti ti-cloud-download"></i>دریافت ساب</a>
    <button class="btn btn-o" id="cpSub"><i class="ti ti-copy"></i>کپی لینک ساب</button>
  </div>
  <div id="links"></div>
</div>
<div class="gate" id="gate" style="display:none">
  <i class="ti ti-lock"></i>
  <h2>این گروه رمزدار است</h2>
  <input type="password" id="gpw" placeholder="رمز عبور گروه">
  <button class="btn btn-p" id="gobtn"><i class="ti ti-unlock"></i>نمایش کانفیگ‌ها</button>
  <div class="gerr" id="gerr">رمز اشتباه است</div>
</div>
<div class="foot">پشتیبانی <a href="https://t.me/omiddemon" target="_blank">@omiddemon</a> · OMID GOLD</div>
<div id="toasts"></div>
<script>
const KEY='__SUBKEY__';
let PW=new URLSearchParams(location.search).get('pw')||'';
let DATA=null;
function toast(m,e){const t=document.createElement('div');t.className='toast'+(e?' err':'');t.textContent=m;document.getElementById('toasts').appendChild(t);requestAnimationFrame(()=>t.classList.add('show'));setTimeout(()=>{t.classList.remove('show');setTimeout(()=>t.remove(),300)},2800);}
async function copyText(t){try{await navigator.clipboard.writeText(t);toast('کپی شد')}catch(e){const a=document.createElement('textarea');a.value=t;document.body.appendChild(a);a.select();document.execCommand('copy');a.remove();toast('کپی شد')}}
function esc(s){return(s??'').toString().replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
function fmtB(b){if(b<1024)return b+' B';if(b<1048576)return(b/1024).toFixed(1)+' KB';if(b<1073741824)return(b/1048576).toFixed(2)+' MB';return(b/1073741824).toFixed(2)+' GB'}
async function load(){
  try{
    const r=await fetch(`/api/public/sub/${KEY}?pw=${encodeURIComponent(PW)}`);
    const d=await r.json();
    if(d.locked){document.getElementById('gate').style.display='block';return;}
    DATA=d;render();
  }catch(e){document.getElementById('links').innerHTML='<div class="empty">خطا در دریافت اطلاعات</div>';}
}
function render(){
  document.getElementById('gate').style.display='none';
  document.getElementById('gname').textContent=DATA.name||'';
  document.getElementById('gdesc').textContent=DATA.desc||'';
  document.getElementById('subbtns').style.display='flex';
  const dl=document.getElementById('dlSub');dl.href=DATA.sub_url;
  document.getElementById('cpSub').onclick=()=>copyText(DATA.sub_url);
  document.getElementById('statrow').innerHTML=`
    <span class="sbadge"><i class="ti ti-arrows-exchange"></i>${esc(DATA.total_used_fmt||'0 B')}</span>
    <span class="sbadge"><i class="ti ti-access-point"></i>${DATA.active_connections||0} اتصال</span>
    <span class="sbadge"><i class="ti ti-link"></i>${(DATA.links||[]).length} کانفیگ</span>`;
  const box=document.getElementById('links');
  if(!(DATA.links||[]).length){box.innerHTML='<div class="empty">هنوز کانفیگی در این گروه نیست</div>';return;}
  box.innerHTML=DATA.links.map((l,i)=>{
    const pct=l.limit_bytes>0?Math.min(100,(l.used_bytes/l.limit_bytes*100)):0;
    return`<div class="lcard ${l.active?'':'off'}">
      <div class="lc-head">
        <div class="lc-name">${esc(l.label)}</div>
        <div class="lc-actions">
          <button class="bicon" onclick="copyL(${i})"><i class="ti ti-copy"></i></button>
          <button class="bicon" onclick="qrL(${i})"><i class="ti ti-qrcode"></i></button>
        </div>
      </div>
      <div style="display:flex;gap:6px;flex-wrap:wrap;margin-bottom:9px">
        <span class="chip ${l.active?'chip-ok':'chip-exp'}">${l.active?'فعال':'غیرفعال'}</span>
        <span class="chip chip-gold"><i class="ti ti-topology-star"></i>${esc((l.protocol||'').replace('vless-','').replace('xhttp-','XHTTP·'))}</span>
        ${l.proxy_label?`<span class="chip chip-gold"><i class="ti ti-world-share"></i>${esc(l.proxy_label)}</span>`:''}
        ${l.ip_limit>0?`<span class="chip chip-amb"><i class="ti ti-users"></i>${l.ip_limit} IP</span>`:''}
        ${l.connections?`<span class="chip"><i class="ti ti-access-point"></i>${l.connections}</span>`:''}
      </div>
      <div class="ubar"><i style="width:${pct}%"></i></div>
      <div class="utxt">${esc(l.used_fmt)} از ${esc(l.limit_fmt)}${l.expires_at?' · انقضا: '+new Date(l.expires_at).toLocaleDateString('fa-IR'):''}</div>
      <div class="qr" id="qr${i}"><img src="https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=${encodeURIComponent(l.vless_link)}" alt="qr"></div>
    </div>`;
  }).join('');
}
function copyL(i){copyText(DATA.links[i].vless_link);}
function qrL(i){document.getElementById('qr'+i).classList.toggle('show');}
document.getElementById('gobtn').addEventListener('click',async()=>{
  PW=document.getElementById('gpw').value;
  document.getElementById('gerr').style.display='none';
  const r=await fetch(`/api/public/sub/${KEY}?pw=${encodeURIComponent(PW)}`);
  const d=await r.json();
  if(d.locked){document.getElementById('gerr').style.display='block';return;}
  DATA=d;render();
});
document.getElementById('gpw').addEventListener('keydown',e=>{if(e.key==='Enter')document.getElementById('gobtn').click();});
load();
</script>
</body></html>"""

# ═══════════════════════════ خروجی‌های ماژول ═══════════════════════════
LOGIN_HTML = _LOGIN_TPL.replace("__LOGO_SVG__", LOGO_SVG).replace("__HEARTBEAT__", HEARTBEAT_HTML).replace("__GOLD_CSS__", _GOLD_CSS)
DASHBOARD_HTML = _DASH_TPL.replace("__LOGO_SVG__", LOGO_SVG).replace("__HEARTBEAT__", HEARTBEAT_HTML).replace("__GOLD_CSS__", _GOLD_CSS)

def get_public_page_html(uuid_key: str) -> str:
    """صفحه‌ی عمومی گروه ساب با کلید یکتا."""
    return (_PUBLIC_TPL
            .replace("__SUBKEY__", uuid_key)
            .replace("__LOGO_SVG__", LOGO_SVG)
            .replace("__GOLD_CSS__", _GOLD_CSS))
