#!/usr/bin/env python3
"""Confere os precos de docs/items.json, grava o historico e avisa no celular (ntfy) quando cai."""
import json, os, re, time, urllib.request
from pathlib import Path

D = Path(__file__).parent / "docs"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36",
      "Accept-Language": "pt-BR,pt;q=0.9"}


def money(x):
    return "R$ " + f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def parse_price(html):
    # shortcut: o primeiro padrao que casar vence; se uma loja mudar o layout, ajuste os padroes
    m = re.search(r'a-offscreen">\s*R\$\s*([\d.]+,\d{2})', html)  # Amazon
    if m:
        return float(m.group(1).replace(".", "").replace(",", "."))
    for pat in (r'"(?:price|lowPrice)"\s*:\s*"?(\d+(?:\.\d+)?)"?',  # JSON-LD (KaBuM, Pichau...)
                r'product:price:amount"\s+content="(\d+(?:\.\d+)?)"'):
        m = re.search(pat, html)
        if m and float(m.group(1)) > 0:
            return float(m.group(1))
    m = re.search(r'R\$\s*([\d.]+,\d{2})', html)
    return float(m.group(1).replace(".", "").replace(",", ".")) if m else None


def alert(hist, price, target):
    last = hist[-1][1] if hist else None
    if target and price <= target and (last is None or last > target):
        return f"{money(price)}, bateu sua meta de {money(target)}"
    if last and price < last * 0.99:
        return f"caiu de {money(last)} para {money(price)}"


def notify(text, url):
    topic = os.environ.get("NTFY_TOPIC")
    if not topic:
        print("ALERTA:", text)
        return
    req = urllib.request.Request(f"https://ntfy.sh/{topic}", data=text.encode(),
                                 headers={"Title": "Preco caiu", "Click": url})
    urllib.request.urlopen(req, timeout=20)


def fetch(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=20).read().decode("utf-8", "replace")


def main():
    items = json.loads((D / "items.json").read_text())
    path = D / "prices.json"
    hist = json.loads(path.read_text()) if path.exists() else {}
    now = int(time.time())
    for it in items:
        try:
            price = parse_price(fetch(it["url"]))
        except Exception as e:  # loja bloqueou ou caiu: segue com os outros itens
            print("erro", it["name"], e)
            continue
        if price is None:
            print("sem preco", it["name"])
            continue
        h = hist.setdefault(it["url"], [])
        msg = alert(h, price, it.get("target"))
        h.append([now, price])
        del h[:-300]
        print(it["name"], money(price))
        if msg:
            notify(f"{it['name']}: {msg}", it["url"])
    path.write_text(json.dumps(hist))


if __name__ == "__main__":
    main()
