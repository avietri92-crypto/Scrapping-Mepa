from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)   # 1. Browser: avvia Chrome
    context = browser.new_context()                # 2. Context: profilo isolato
    page = context.new_page()                       # 3. Page: una scheda dentro il context

    page.goto("https://mepa.it/home/garemepa")                # naviga con quella scheda
    titoli=page.locator(".m-t-10").wait_for() 
    pulsante_altri = page.locator("text=Mostra altri risultati")  # adatta al testo/selettore reale

    while pulsante_altri.is_visible():
    pulsante_altri.click()
    page.wait_for_timeout(1000)
    contatore= titoli.count()
    
    for i in range(contatore):
        print(titoli.nth(i).text_content())
        
    browser.close()  
