from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)   # 1. Browser: avvia Chrome
    context = browser.new_context()                # 2. Context: profilo isolato
    page = context.new_page()                       # 3. Page: una scheda dentro il context
    page.goto("https://mepa.it/home/garemepa")

    titoli = page.locator("#simpleList h4")
    pulsante_altri = page.locator("text=mostra altri risultati")  # adatta al selettore reale

    click_numero = 0
    while pulsante_altri.is_visible():
        prima = titoli.count()
        pulsante_altri.click()
        page.wait_for_timeout(1500)
        dopo = titoli.count()
        click_numero += 1
        print(f"Click {click_numero}: prima={prima}, dopo={dopo}")

        if dopo == prima:
            print("ATTENZIONE: il conteggio non è cresciuto, il click potrebbe non funzionare")
            break  # evita loop infinito se il problema si ripete sempre
