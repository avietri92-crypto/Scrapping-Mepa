from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    # stampa ogni richiesta di rete che parte dopo il caricamento iniziale
    page.on("response", lambda response: print(f"  → risposta: {response.status} {response.url}"))

    page.goto("https://mepa.it/home/garemepa")
    page.locator("#simpleList h4").wait_for()

    titoli = page.locator("#simpleList h4")
    pulsante_altri = page.locator("text=mostra altri risultati")

    click_numero = 0
    while pulsante_altri.is_visible():
        prima = titoli.count()
        print(f"--- Click {click_numero + 1} ---")
        pulsante_altri.click(force=True)   # force=True bypassa controlli di "clickabilità" che potrebbero bloccare silenziosamente
        page.wait_for_timeout(2000)
        dopo = titoli.count()
        click_numero += 1
        print(f"prima={prima}, dopo={dopo}")

        if dopo == prima and click_numero > 1:
            print("ATTENZIONE: nessuna nuova richiesta/nuovo conteggio, il click non sta avanzando")
            break
        if click_numero > 30:  # sicurezza anti-loop-infinito
            break
