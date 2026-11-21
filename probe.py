import json
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(user_agent="Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 Chrome/124 Mobile Safari/537.36",
                        viewport={"width": 390, "height": 844}, locale="pt-BR")
    pg = ctx.new_page()
    def req(r):
        if "zoom.com.br" in r.url and ("api" in r.url or "search" in r.url):
            print("REQ", r.method, r.url[:200], (r.post_data or "")[:300])
    def resp(r):
        if "api-v1.zoom.com.br" in r.url and "suggestions" not in r.url:
            try: print("RESP", r.status, r.url[:120], r.headers.get("content-type"), r.headers.get("access-control-allow-origin"), len(r.text()))
            except Exception as e: print("RESP", r.status, r.url[:120], "ERR", e)
    pg.on("request", req); pg.on("response", resp)
    pg.goto("https://www.zoom.com.br/search?q=processador%20ryzen", wait_until="networkidle", timeout=60000)
    pg.wait_for_timeout(3000)
    cards = pg.query_selector_all("[data-testid='product-card']")
    print("CARDS", len(cards))
    for c in cards[:3]:
        print("TESTIDS", c.eval_on_selector_all("[data-testid]", "els => els.map(e => e.dataset.testid + '=' + e.innerText.slice(0,60).replace(/\\n/g,' | '))"))
        print("HREF", c.eval_on_selector("a", "a => a.getAttribute('href')"))
    ft = pg.eval_on_selector_all("[data-testid*='filter'], [data-testid*='refinement'], [data-testid*='facet']", "els => [...new Set(els.map(e => e.dataset.testid))]")
    print("FILTER TESTIDS", ft[:40])
    b.close()
