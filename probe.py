import re, json, urllib.request
UA = {"User-Agent": "Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 Chrome/124 Mobile Safari/537.36", "Accept-Language": "pt-BR,pt;q=0.9"}
def get(u):
    return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=25).read().decode("utf-8", "replace")
def walk(o, path="", depth=0, out=None):
    if depth > 6: return
    if isinstance(o, dict):
        for k, v in o.items():
            p = path + "." + k
            if isinstance(v, (dict, list)):
                print(p, type(v).__name__, len(v)); walk(v, p, depth + 1)
            else:
                print(p, "=", str(v)[:70])
    elif isinstance(o, list) and o:
        print(path + "[0]"); walk(o[0], path + "[0]", depth + 1)
for u in ["https://www.zoom.com.br/search?q=processador%20ryzen"]:
    b = get(u)
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', b, re.S)
    d = json.loads(m.group(1))
    print("TOP", list(d["props"].keys()), d.get("page"), d.get("query"))
    walk(d["props"], "props")
    for i, l in enumerate(re.findall(r'<script type="application/ld\+json">(.*?)</script>', b, re.S)[:3]):
        print("LD", i, l[:500])
