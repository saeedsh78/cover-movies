import requests

TIMEOUT = 25
NO_PROXY = {"http": None, "https": None}

# latched after the system proxy proves unreachable; requests go direct
_bypass_proxy = False


def _system_proxy():
    """Read the Windows system proxy the way the browser does (WinINET)."""
    try:
        import winreg
    except ImportError:
        return None
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Internet Settings")
        try:
            enabled, _ = winreg.QueryValueEx(key, "ProxyEnable")
            server, _ = winreg.QueryValueEx(key, "ProxyServer")
        finally:
            winreg.CloseKey(key)
    except OSError:
        return None
    if not enabled or not server:
        return None

    if "=" in server:
        proxies = {}
        for part in server.split(";"):
            if "=" not in part:
                continue
            proto, addr = part.split("=", 1)
            addr = addr.strip()
            if not addr:
                continue
            if proto == "socks":
                addr = "socks5://" + addr
            elif "://" not in addr:
                addr = "http://" + addr
            proxies[proto] = addr
        if proxies.get("http") and proxies.get("https"):
            return {"http": proxies["http"], "https": proxies["https"]}
        if proxies.get("socks"):
            return {"http": proxies["socks"], "https": proxies["socks"]}
        return None

    url = server if "://" in server else "http://" + server
    return {"http": url, "https": url}


def get(url, timeout=TIMEOUT, **kwargs):
    global _bypass_proxy
    if _bypass_proxy:
        return requests.get(url, timeout=timeout, proxies=dict(NO_PROXY), **kwargs)
    px = _system_proxy()
    if not px:
        return requests.get(url, timeout=timeout, **kwargs)
    try:
        return requests.get(url, timeout=timeout, proxies=px, **kwargs)
    except (requests.exceptions.ProxyError, requests.exceptions.SSLError,
            requests.exceptions.InvalidSchema):
        _bypass_proxy = True
        return requests.get(url, timeout=timeout, proxies=dict(NO_PROXY), **kwargs)
