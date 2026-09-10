from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)   # 1. Browser: avvia Chrome
    context = browser.new_context()                # 2. Context: profilo isolato
    page = context.new_page()                       # 3. Page: una scheda dentro il context
    page.goto("https://mepa.it/home/garemepa")
    page.locator("h4").wait_for()


    pulsante_altri = page.locator("text=mostra altri risultati")  # adatta al testo/selettore reale

    while pulsante_altri.is_visible():
        pulsante_altri.click()
        page.wait_for_timeout(1000)  # piccola pausa per far caricare i nuovi elementi

    titoli = page.locator("h4")
    contatore = titoli.count()

    for i in range(contatore):
       print(titoli.nth(i).text_content())
