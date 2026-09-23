# proxy_outbound.py — v2
# ══════════════════════════════════════════════════════════════════════════════
# موتور خروجی از پروکسی — نسخه مقاوم با تشخیص خودکار پروتکل و fallback کامل
#  ─ کلاینت SOCKS5 (RFC 1928 + احراز هویت RFC 1929) با asyncio خالص — بدون وابستگی جدید
#  ─ کلاینت HTTP CONNECT با fallback: HTTP/1.1 → HTTP/1.0 → پروکسی-TLS (پروکسی https)
#  ─ پروکسیِ «HTTP» که در واقع SOCKS5 است، خودکار شناسایی و استفاده می‌شود
#  ─ پروتکل برنده برای هر پروکسی کش می‌شود → دفعات بعد بدون سربار
#  ─ رفع باگ: بایت‌های بعد از هدر CONNECT دیگر گم نمی‌شوند (خواندن خط‌به‌خط با readline)
#  ─ diagnose_proxy(): تشخیص مرحله‌به‌مرحله برای دکمه «تست» پنل
#  ─ DNS دامنه‌ها داخل خودِ پروکسی resolve می‌شود (بدون نشت DNS)
#  ─ open_connection_via(): جایگزین drop-in برای asyncio.open_connection در رله‌ها
#    → اگر پروکسی داده شود، کل اتصال TCP از داخل تونل پروکسی باز می‌شود؛ یعنی
#      IP خروجی‌ای که مقصد (سایت‌ها) می‌بیند، دقیقاً IP خودِ پروکسی است.
# ══════════════════════════════════════════════════════════════════════════════

import asyncio
import base64
import ipaddress
import socket
import ssl
import time

PROXY_HANDSHAKE_TIMEOUT = 12.0
PROXY_TEST_TIMEOUT = 15.0

# کش پروتکل برنده: key → "http" | "socks5"
_detected: dict = {}


class ProxyError(Exception):
    """خطای اتصال/هندشیک پروکسی خروجی. code = کد HTTP (در صورت وجود)."""
    def __init__(self, message: str, code: int | None = None):
        super().__init__(message)
        self.code = code


def describe_proxy(proxy: dict | None) -> str:
    """توضیح متنی پروکسی برای لاگ‌ها (رمز ماسک می‌شود)."""
    if not proxy:
        return "direct"
    user = proxy.get("username")
    cred = f"{user}:***@" if user else ""
    return f"{proxy.get('type', 'socks5')}://{cred}{proxy.get('host')}:{proxy.get('port')}"


def _proxy_key(proxy: dict) -> str:
    return f"{proxy.get('type','')}|{proxy.get('host')}|{proxy.get('port')}|{proxy.get('username') or ''}"


def _validate(proxy: dict) -> tuple[str, int]:
    phost = str(proxy.get("host") or "").strip()
    try:
        pport = int(proxy.get("port") or 0)
    except (TypeError, ValueError):
        pport = 0
    if not phost or not (1 <= pport <= 65535):
        raise ProxyError("پروکسی خروجی معتبر نیست (host/port نامعتبر)")
    return phost, pport


def _tune_socket(writer: asyncio.StreamWriter):
    """TCP_NODELAY برای کاهش لتنسی هندشیک و اولین بایت‌های رله."""
    try:
        sock = writer.transport.get_extra_info("socket")
        if sock:
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    except Exception:
        pass


def _is_ip_literal(host: str) -> bool:
    try:
        ipaddress.ip_address(host)
        return True
    except ValueError:
        return False


def _scheme_order(proxy: dict) -> list:
    """ترتیب امتحان پروتکل‌ها — پروتکل برنده‌ی قبلی اول."""
    t = str(proxy.get("type") or "").strip().lower()
    if t == "socks5":
        order = ["socks5", "http"]
    else:  # http یا هر چیز دیگر
        order = ["http", "socks5"]
    cached = _detected.get(_proxy_key(proxy))
    if cached in order:
        order = [cached] + [s for s in order if s != cached]
    return order


# ══════════════════════════════════════════════════════════════════════════════
# اتصال به خودِ پروکسی (TCP و در صورت نیاز TLS روی پورت پروکسی)
# ══════════════════════════════════════════════════════════════════════════════

async def _connect_proxy_socket(proxy: dict, connect_timeout: float, use_tls: bool):
    phost, pport = _validate(proxy)
    reader, writer = await asyncio.wait_for(
        asyncio.open_connection(phost, pport), timeout=connect_timeout
    )
    _tune_socket(writer)

    if use_tls:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        loop = asyncio.get_running_loop()
        transport = writer.transport
        protocol = transport.get_protocol()
        try:
            new_transport = await asyncio.wait_for(
                loop.start_tls(transport, protocol, ctx,
                               server_hostname=None if _is_ip_literal(phost) else phost),
                timeout=connect_timeout,
            )
        except Exception:
            try:
                writer.close()
            except Exception:
                pass
            raise ProxyError("اتصال TLS به سرور پروکسی برقرار نشد (این پروکسی احتمالاً https نیست)")
        writer = asyncio.StreamWriter(new_transport, protocol, reader, loop)
    return reader, writer


# ══════════════════════════════════════════════════════════════════════════════
# SOCKS5 — RFC 1928 (CONNECT) + RFC 1929 (username/password)
# ══════════════════════════════════════════════════════════════════════════════

async def _socks5_handshake(reader: asyncio.StreamReader,
                            writer: asyncio.StreamWriter,
                            dst_host: str,
                            dst_port: int,
                            username: str,
                            password: str,
                            timeout: float):
    # ۱) سلام + مذاکره متد احراز هویت
    #    اگر یوزرنیم داریم، هم no-auth هم user/pass پیشنهاد می‌کنیم تا حداکثر سازگاری
    if username:
        writer.write(b"\x05\x02\x00\x02")
    else:
        writer.write(b"\x05\x01\x00")
    await writer.drain()

    try:
        resp = await asyncio.wait_for(reader.readexactly(2), timeout)
    except asyncio.IncompleteReadError:
        raise ProxyError("SOCKS5: سرور وسط سلام اتصال را بست (احتمالاً SOCKS نیست)")
    ver, method = resp[0], resp[1]
    if ver != 0x05:
        raise ProxyError(f"این سرور SOCKS5 نیست (ver={ver})")
    if method == 0xFF:
        raise ProxyError("SOCKS5: هیچ متد احراز هویتی پذیرفته نشد (یوزر/پسورد را چک کن)")

    if method == 0x02:
        # زیرمذاکره‌ی احراز هویت RFC 1929
        if not username:
            raise ProxyError("SOCKS5: این سرور یوزرنیم/پسورد می‌خواهد", code=401)
        ub = username.encode("utf-8")[:255]
        pb = password.encode("utf-8")[:255]
        writer.write(b"\x01" + bytes([len(ub)]) + ub + bytes([len(pb)]) + pb)
        await writer.drain()
        try:
            auth = await asyncio.wait_for(reader.readexactly(2), timeout)
        except asyncio.IncompleteReadError:
            raise ProxyError("SOCKS5: سرور وسط احراز هویت اتصال را بست")
        if auth[1] != 0x00:
            raise ProxyError("SOCKS5: احراز هویت رد شد (یوزرنیم/پسورد غلط)", code=401)
    elif method != 0x00:
        raise ProxyError(f"SOCKS5: متد احراز هویت پشتیبانی نمی‌شود 0x{method:02x}")

    # ۲) CONNECT — دامنه‌ها ATYP=3 تا DNS داخل خود پروکسی انجام شود (بدون نشت DNS)
    try:
        ip = ipaddress.ip_address(dst_host)
        if ip.version == 4:
            atyp, addr = 0x01, ip.packed
        else:
            atyp, addr = 0x04, ip.packed
    except ValueError:
        host_b = (dst_host.encode("idna")
                  if any(ord(ch) > 127 for ch in dst_host)
                  else dst_host.encode("utf-8"))
        if len(host_b) > 255:
            raise ProxyError("نام دامنه مقصد بیش از حد طولانی است")
        atyp, addr = 0x03, bytes([len(host_b)]) + host_b

    writer.write(b"\x05\x01\x00" + bytes([atyp]) + addr + int(dst_port).to_bytes(2, "big"))
    await writer.drain()

    try:
        head = await asyncio.wait_for(reader.readexactly(4), timeout)
    except asyncio.IncompleteReadError:
        raise ProxyError("SOCKS5: سرور وسط CONNECT اتصال را بست")
    if head[1] != 0x00:
        _codes = {
            0x01: "خطای عمومی",
            0x02: "مجاز نیست (ruleset سرور پروکسی)",
            0x03: "شبکه مقصد در دسترس نیست",
            0x04: "مقصد پیدا نشد",
            0x05: "اتصال مقصد رد شد",
            0x06: "TTL منقضی شد",
            0x07: "این سرور CONNECT ساپورت نمی‌کند",
            0x08: "نوع آدرس ساپورت نمی‌شود",
        }
        raise ProxyError(f"SOCKS5 CONNECT رد شد: {_codes.get(head[1], f'code={head[1]}')}", code=403)

    # ۳) خواندن BND.ADDR + BND.PORT از پاسخ (بعد از این، تونل شفاف است)
    atyp_r = head[3]
    try:
        if atyp_r == 0x01:
            await asyncio.wait_for(reader.readexactly(4), timeout)
        elif atyp_r == 0x03:
            ln = (await asyncio.wait_for(reader.readexactly(1), timeout))[0]
            await asyncio.wait_for(reader.readexactly(ln), timeout)
        elif atyp_r == 0x04:
            await asyncio.wait_for(reader.readexactly(16), timeout)
        else:
            raise ProxyError(f"SOCKS5: ATYP پاسخ نامعتبر {atyp_r}")
        await asyncio.wait_for(reader.readexactly(2), timeout)  # BND.PORT
    except asyncio.IncompleteReadError:
        raise ProxyError("SOCKS5: سرور وسط پاسخ اتصال را بست")

    return reader, writer


async def _socks5_full(proxy: dict, dst_host: str, dst_port: int, connect_timeout: float):
    """اتصال کامل SOCKS5: سوکت + هندشیک. در خطا سوکت پروکسی کامل بسته می‌شود."""
    reader, writer = await _connect_proxy_socket(proxy, connect_timeout, False)
    try:
        return await _socks5_handshake(
            reader, writer, dst_host, int(dst_port),
            str(proxy.get("username") or "").strip(),
            str(proxy.get("password") or ""),
            connect_timeout,
        )
    except Exception:
        try:
            writer.close()
        except Exception:
            pass
        raise


# ══════════════════════════════════════════════════════════════════════════════
# HTTP CONNECT — با fallback کامل (1.1 → 1.0 → TLS-پروکسی)
# ══════════════════════════════════════════════════════════════════════════════

async def _http_connect_handshake(reader: asyncio.StreamReader,
                                  writer: asyncio.StreamWriter,
                                  dst_host: str,
                                  dst_port: int,
                                  username: str,
                                  password: str,
                                  version: str):
    if ":" in dst_host and not dst_host.startswith("["):
        dst = f"[{dst_host}]:{dst_port}"   # IPv6 literal
    else:
        dst = f"{dst_host}:{dst_port}"

    req = (f"CONNECT {dst} {version}\r\n"
           f"Host: {dst}\r\n"
           f"User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36\r\n"
           f"Proxy-Connection: keep-alive\r\n")
    if username:
        cred = base64.b64encode(f"{username}:{password}".encode("utf-8")).decode("ascii")
        req += f"Proxy-Authorization: Basic {cred}\r\n"
    req += "\r\n"

    writer.write(req.encode("utf-8"))
    await writer.drain()

    # خط وضعیت (خط‌های خالی ابتدایی نادیده گرفته می‌شوند)
    status_line = b""
    for _ in range(8):
        raw = await asyncio.wait_for(reader.readline(), timeout=10.0)
        if not raw:
            raise ProxyError("HTTP proxy وسط CONNECT اتصال را بست")
        stripped = raw.strip()
        if stripped:
            status_line = stripped
            break
    if not status_line:
        raise ProxyError("HTTP proxy پاسخ خالی داد")

    parts = status_line.decode("utf-8", errors="ignore").split(" ", 2)
    if len(parts) < 2 or not parts[0].upper().startswith("HTTP") or not parts[1].isdigit():
        raise ProxyError(f"HTTP proxy خط وضعیت نامعتبر: {status_line[:80]!r}")
    code = int(parts[1])
    reason = parts[2] if len(parts) > 2 else ""

    # خواندن هدرها تا خط خالی؛ بایت‌های اضافه در بافر reader می‌مانند و تونل سالم می‌ماند
    for _ in range(256):
        line = await asyncio.wait_for(reader.readline(), timeout=10.0)
        if line in (b"\r\n", b"\n", b""):
            break

    if 200 <= code < 300:
        return
    raise ProxyError(f"HTTP CONNECT failed: HTTP {code} {reason}".strip(), code=code)


# ترتیب تلاش‌های HTTP: (TLS روی پورت پروکسی؟، نسخه پروتکل)
_HTTP_ATTEMPTS = ((False, "HTTP/1.1"), (False, "HTTP/1.0"), (True, "HTTP/1.1"), (True, "HTTP/1.0"))


async def _http_connect_full(proxy: dict, dst_host: str, dst_port: int, connect_timeout: float):
    """HTTP CONNECT با fallback کامل — هر ۴ حالت را امتحان می‌کند."""
    username = str(proxy.get("username") or "").strip()
    password = str(proxy.get("password") or "")
    last_err: Exception | None = None
    handshake_err: ProxyError | None = None

    for use_tls, version in _HTTP_ATTEMPTS:
        try:
            reader, writer = await _connect_proxy_socket(proxy, connect_timeout, use_tls)
        except ProxyError as e:
            last_err = last_err or e
            continue   # مثلاً TLS روی پروکسی non-https → حالت بعدی
        except Exception as e:
            last_err = last_err or e
            continue   # TCP اصلاً وصل نشد → حالت بعدی

        try:
            await _http_connect_handshake(reader, writer, dst_host, int(dst_port),
                                          username, password, version)
            return reader, writer
        except ProxyError as e:
            try:
                writer.close()
            except Exception:
                pass
            if e.code in (401, 407):
                raise ProxyError("پروکسی احراز هویت می‌خواهد — یوزرنیم/پسورد پروکسی را در پنل وارد کن",
                                 code=e.code)
            handshake_err = handshake_err or e
            continue   # 400/403/405/... → نسخه/TLS بعدی
        except Exception as e:
            try:
                writer.close()
            except Exception:
                pass
            last_err = last_err or e
            continue

    if handshake_err:
        raise handshake_err
    if isinstance(last_err, ProxyError):
        raise last_err
    raise ProxyError(f"HTTP CONNECT failed: {last_err}")


# ══════════════════════════════════════════════════════════════════════════════
# نقطه‌ی ورود اصلی برای رله‌ها (همان امضای قبلی — drop-in)
# ══════════════════════════════════════════════════════════════════════════════

async def open_connection_via(proxy: dict | None,
                              host: str,
                              port: int,
                              connect_timeout: float = PROXY_HANDSHAKE_TIMEOUT):
    """دقیقاً مثل asyncio.open_connection(host, port) یک (reader, writer) برمی‌گرداند،
    اما اگر proxy داده شود، اتصال از داخل تونل پروکسی باز می‌شود →
    IP خروجی‌ای که مقصد می‌بیند دقیقاً IP خود پروکسی است.
      proxy=None → اتصال مستقیم (رفتار کاملاً یکسان با asyncio.open_connection)
      proxy={'type':'socks5'|'http', 'host', 'port', 'username', 'password'}"""
    if not proxy:
        reader, writer = await asyncio.open_connection(host, int(port))
        _tune_socket(writer)
        return reader, writer

    _validate(proxy)
    key = _proxy_key(proxy)
    last_err: Exception | None = None

    for scheme in _scheme_order(proxy):
        try:
            if scheme == "socks5":
                reader, writer = await _socks5_full(proxy, host, int(port), connect_timeout)
            else:
                reader, writer = await _http_connect_full(proxy, host, int(port), connect_timeout)
            _detected[key] = scheme   # پروتکل برنده کش شد → دفعات بعد مستقیم همین
            return reader, writer
        except ProxyError as e:
            last_err = e
            if e.code in (401, 407):
                break   # احراز هویت — تغییر پروتکل فایده ندارد
        except Exception as e:
            last_err = e

    if isinstance(last_err, ProxyError):
        raise last_err
    raise ProxyError(f"اتصال از طریق پروکسی ({describe_proxy(proxy)}) ناموفق بود: {last_err}")


# ══════════════════════════════════════════════════════════════════════════════
# تست IP خروجی + تشخیص مرحله‌به‌مرحله
# ══════════════════════════════════════════════════════════════════════════════

async def _fetch_exit_ip(reader: asyncio.StreamReader, writer: asyncio.StreamWriter,
                         host: str, use_tls: bool, timeout: float) -> str:
    """از داخل تونلِ باز‌شده، IP خروجی را می‌گیرد (HTTP ساده یا با TLS-upgrade برای پورت 443)."""
    if use_tls:
        # بالا کشیدن TLS داخل تونل (برای مقاصد 443)
        ctx = ssl.create_default_context()
        loop = asyncio.get_running_loop()
        transport = writer.transport
        protocol = transport.get_protocol()
        new_transport = await asyncio.wait_for(
            loop.start_tls(transport, protocol, ctx, server_hostname=host), timeout)
        writer = asyncio.StreamWriter(new_transport, protocol, reader, loop)

    writer.write((f"GET / HTTP/1.1\r\nHost: {host}\r\nUser-Agent: curl/8.5.0\r\n"
                  f"Accept: */*\r\nConnection: close\r\n\r\n").encode("utf-8"))
    await writer.drain()

    chunks = []
    total = 0
    while total < 65536:
        try:
            chunk = await asyncio.wait_for(reader.read(8192), timeout=5.0)
        except asyncio.TimeoutError:
            break
        if not chunk:
            break
        chunks.append(chunk)
        total += len(chunk)

    raw = b"".join(chunks).decode("utf-8", errors="ignore")
    body = raw.split("\r\n\r\n", 1)[-1].strip() if "\r\n\r\n" in raw else raw.strip()
    candidate = (body.split()[0] if body else "").strip().strip('"')
    ipaddress.ip_address(candidate)   # اگر IP معتبر نباشد ValueError می‌دهد
    return candidate


# مقصدهای تست: (دامنه، پورت، TLS-upgrade بعد از تونل؟) — چند مقصد برای دور زدن پورت‌بلاک
_EGRESS_TARGETS = (
    ("api.ipify.org", 80, False),
    ("icanhazip.com", 80, False),
    ("ifconfig.me", 80, False),
    ("api.ipify.org", 443, True),
    ("icanhazip.com", 443, True),
)

_DIAG_TARGETS = (
    ("api.ipify.org", 80, False),
    ("icanhazip.com", 80, False),
    ("api.ipify.org", 443, True),
)


async def test_proxy_egress(proxy: dict | None, timeout: float = PROXY_TEST_TIMEOUT) -> str:
    """IP خروجی واقعی را از داخل تونل پروکسی برمی‌گرداند (چند پروتکل/مقصد امتحان می‌شود).
    proxy=None → IP مستقیم خود سرور (برای مقایسه در پنل)."""
    if not proxy:
        reader, writer = await asyncio.wait_for(asyncio.open_connection("api.ipify.org", 80), timeout)
        try:
            return await _fetch_exit_ip(reader, writer, "api.ipify.org", False, timeout)
        finally:
            try:
                writer.close()
            except Exception:
                pass

    last_err: Exception | None = None
    for host, port, tls in _EGRESS_TARGETS:
        try:
            reader, writer = await open_connection_via(proxy, host, port, connect_timeout=timeout)
        except Exception as e:
            last_err = e
            continue
        try:
            return await _fetch_exit_ip(reader, writer, host, tls, timeout)
        except Exception as e:
            last_err = e
        finally:
            try:
                writer.close()
            except Exception:
                pass
    raise ProxyError(f"تست پروکسی ناموفق بود: {last_err}")


async def diagnose_proxy(proxy: dict, timeout: float = 8.0) -> dict:
    """تشخیص مرحله‌به‌مرحله برای دکمه تست پنل:
    مرحله ۱: اتصال TCP به خود پروکسی → مرحله ۲: هندشیک پروتکل → مرحله ۳: IP خروجی واقعی"""
    stages: list = []
    try:
        phost, pport = _validate(proxy)
    except ProxyError as e:
        return {"ok": False, "detail": str(e), "stages": [f"✗ {e}"], "hint": str(e)}

    # ── مرحله ۱: اتصال TCP به خود پروکسی ──
    t0 = time.monotonic()
    try:
        r, w = await asyncio.wait_for(asyncio.open_connection(phost, pport), timeout)
        w.close()
        stages.append(f"✓ اتصال TCP به {phost}:{pport} ({(time.monotonic()-t0)*1000:.0f}ms)")
    except Exception as e:
        stages.append(f"✗ اتصال TCP به {phost}:{pport} ناموفق: {e}")
        return {"ok": False, "detail": "اتصال اولیه به سرور پروکسی برقرار نشد",
                "stages": stages,
                "hint": "آی‌پی/پورت پروکسی اشتباه است یا فایروال جلوی آن را گرفته"}

    # ── مرحله ۲ و ۳: پروتکل + IP خروجی واقعی ──
    auth_hint = None
    for scheme in _scheme_order(proxy):
        for host, port, tls in _DIAG_TARGETS:
            target = f"{host}:{port}" + (" (TLS)" if tls else "")
            try:
                t0 = time.monotonic()
                if scheme == "socks5":
                    reader, writer = await _socks5_full(proxy, host, port, timeout)
                else:
                    reader, writer = await _http_connect_full(proxy, host, port, timeout)
                stages.append(f"✓ تونل {scheme} → {target} ({(time.monotonic()-t0)*1000:.0f}ms)")
            except ProxyError as e:
                stages.append(f"… {scheme} → {target}: {e}")
                if e.code in (401, 407):
                    auth_hint = "یوزرنیم/پسورد پروکسی لازم است — آن را در پنل وارد کن"
                    break
                if e.code == 405:
                    break   # این سرور اصلاً CONNECT ندارد؛ تغییر مقصد فایده ندارد
                continue
            except Exception as e:
                stages.append(f"… {scheme} → {target}: {e}")
                continue

            try:
                ip = await _fetch_exit_ip(reader, writer, host, tls, timeout + 4)
                stages.append(f"✓ IP خروجی واقعی: {ip} (پروتکل: {scheme})")
                _detected[_proxy_key(proxy)] = scheme
                return {"ok": True, "exit_ip": ip, "protocol": scheme,
                        "detail": f"خروجی واقعی: {ip} · پروتکل: {scheme}",
                        "stages": stages}
            except Exception as e:
                stages.append(f"… دریافت IP از {target} ناموفق: {e}")
            finally:
                try:
                    writer.close()
                except Exception:
                    pass
        if auth_hint:
            break

    if auth_hint:
        hint = auth_hint
    else:
        hint = ("هیچ پروتکلی (HTTP CONNECT / SOCKS5) با این سرور جواب نداد — "
                "احتمالاً این پروکسی از متد CONNECT پشتیبانی نمی‌کند (web proxy است) "
                "و برای VPN قابل استفاده نیست")
    stages.append("✗ تست ناموفق")
    return {"ok": False, "detail": hint, "stages": stages, "hint": hint}