import json
from playwright.sync_api import sync_playwright
hits = []
with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(user_agent="Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 Chrome/124 Mobile Safari/537.36",
                        viewport={"width": 390, "height": 844}, locale="pt-BR")
    pg = ctx.new_page()
    def on(r):
        try:
            ct = r.headers.get("content-type", "")
            if "json" in ct and r.request.resource_type in ("fetch", "xhr"):
                body = r.text()
                hits.append((r.request.method, r.url, len(body), body, r.request.post_data))
        except Exception as e:
            pass
    pg.on("response", on)
    pg.goto("https://www.zoom.com.br/search?q=processador%20ryzen", wait_until="networkidle", timeout=60000)
    pg.wait_for_timeout(4000)
    for m, u, n, body, post in hits:
        flag = "PRICE" if ("price" in body.lower() or "hits" in body) else ""
        print(m, u[:160], n, flag)
        if flag:
            print("   POST:", (post or "")[:400])
            print("   BODY:", body[:900].replace("\n", " "))
    tids = pg.eval_on_selector_all("[data-testid]", "els => [...new Set(els.map(e => e.dataset.testid))]")
    print("TESTIDS", tids[:80])
    html = pg.eval_on_selector("[data-testid*='product']", "e => e.outerHTML") if pg.query_selector("[data-testid*='product']") else "none"
    print("CARD", html[:1500])
    b.close()
