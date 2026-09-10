from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)   # 1. Browser: avvia Chrome
    context = browser.new_context()                # 2. Context: profilo isolato
    page = context.new_page()                       # 3. Page: una scheda dentro il context

    page.goto("https://example.com")                # naviga con quella scheda
    print(page.title())                              # legge il titolo della pagina

    browser.close()  
