import re, json, urllib.request
UA = {"User-Agent": "Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 Chrome/124 Mobile Safari/537.36", "Accept-Language": "pt-BR,pt;q=0.9"}
def get(u):
    return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=25).read().decode("utf-8", "replace")
for u in ["https://www.zoom.com.br/search?q=processador%20ryzen", "https://www.buscape.com.br/search?q=processador%20ryzen"]:
    b = get(u)
    print("#####", u, len(b))
    lds = re.findall(r'<script type="application/ld\+json">(.*?)</script>', b, re.S)
    for i, l in enumerate(lds):
        t = re.findall(r'"@type":"([A-Za-z]+)"', l)[:6]
        print("LD", i, len(l), t)
        if "ItemList" in l or "Product" in l: print("   ", l[:1200])
    for m in list(re.finditer(r'R\$', b))[:3]:
        print("CTX", b[max(0, m.start()-300):m.start()+120].replace("\n", " "))
