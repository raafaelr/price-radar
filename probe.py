import re, urllib.request, json
UA = {"User-Agent": "Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 Chrome/124 Mobile Safari/537.36",
      "Accept-Language": "pt-BR,pt;q=0.9", "Accept": "application/json,text/html,*/*"}
Q = "ryzen%207%207800x3d"
URLS = [
 "https://servicespub.prod.api.kabum.com.br/catalog/v2/products?query=%s&page_number=1&page_size=5&facet_filters=&sort=most_searched" % Q,
 "https://api.mercadolibre.com/sites/MLB/search?q=%s&limit=5" % Q,
 "https://www.zoom.com.br/search?q=%s" % Q,
 "https://www.buscape.com.br/search?q=%s" % Q,
 "https://www.pichau.com.br/search?q=%s" % Q,
 "https://www.amazon.com.br/s?k=%s" % Q,
 "https://lista.mercadolivre.com.br/ryzen-7-7800x3d",
]
for u in URLS:
    print("=====", u[:90])
    try:
        r = urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=25)
        b = r.read().decode("utf-8", "replace")
        print("status", r.status, "len", len(b), r.headers.get("content-type"), "ACAO", r.headers.get("access-control-allow-origin"))
        print("next_data", "__NEXT_DATA__" in b, "ldjson", "application/ld+json" in b, "R$ count", b.count("R$"))
        print(b[:700].replace("\n", " "))
    except Exception as e:
        print("ERR", e)
