import re, json, urllib.request
UA = {"User-Agent": "Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 Chrome/124 Mobile Safari/537.36", "Accept-Language": "pt-BR,pt;q=0.9"}
def get(u):
    return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=25).read().decode("utf-8", "replace")
s1 = get("https://www.zoom.com.br/search?q=processador%20ryzen")
s2 = get("https://www.zoom.com.br/search?q=processador%20ryzen&page=2")
n = lambda s: re.findall(r'data-testid="product-card::name"[^>]*>([^<]+)<', s)
print("P1", len(n(s1)), n(s1)[:3]); print("P2", len(n(s2)), n(s2)[:3])
print("VIA", re.findall(r'Via(?:&nbsp;|\s)*([^<]{2,30})<', s1)[:8])
m = re.search(r'href="(/processador/[^"?]+)', s1); print("LINK", m.group(1))
pp = get("https://www.zoom.com.br" + m.group(1))
print("PRODUCT PAGE len", len(pp), "R$ count", pp.count("R$"))
for i, l in enumerate(re.findall(r'<script type="application/ld\+json">(.*?)</script>', pp, re.S)):
    print("LD", i, re.findall(r'"@type":"([A-Za-z]+)"', l)[:5], l[:600])
for mm in list(re.finditer(r'data-testid="[^"]*(?:price|offer)[^"]*"', pp))[:6]:
    print("T", pp[mm.start():mm.start()+200].replace("\n"," "))
