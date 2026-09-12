import asyncio
import json
from playwright.async_api import async_playwright

async def get_documento_base64(id_bando: str, codice_hash: str):
    async with async_playwright() as p:
        # Avvia Chromium in modalità headless
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        # 1. Carica la scheda del bando per inizializzare sessione, cookie OAM e XSRF-TOKEN dinamico
        url_bando = f"https://www.acquistinretepa.it/opencms/opencms/scheda_altri_bandi.html?idBando={id_bando}"
        print(f"Caricamento pagina bando: {url_bando}")
        
        # Attende che il network sia idle (Angular ha completato l'inizializzazione)
        await page.goto(url_bando, wait_until="networkidle")

        # 2. Esegue la chiamata POST a getDocumento direttamente nel contesto JS del browser
        # Il browser inietta AUTOMATICAMENTE tutti i cookie e l'header X-XSRF-TOKEN corretto
        script_js = """
        async (hash) => {
            const response = await fetch('https://www.acquistinretepa.it/eproc2/documentaleservices/getDocumento', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json;charset=UTF-8',
                    'Accept': 'application/json, text/plain, */*'
                },
                body: JSON.stringify({ id: hash })
            });
            return await response.json();
        }
        """
        
        print("Invio richiesta getDocumento dal browser...")
        result_json = await page.evaluate(script_js, codice_hash)

        await browser.close()
        return result_json

# --- ESEMPIO DI ESECUZIONE ---
if __name__ == "__main__":
    # Sostituisci con i dati reali per testare
    ID_BANDO_TEST = "dbf7b862315835bf"
    CODICE_HASH_TEST = "INSERISCI_QUI_IL_CODICE_HASH"

    response = asyncio.run(get_documento_base64(ID_BANDO_TEST, CODICE_HASH_TEST))
    
    print("\nRisposta ricevuta con successo!")
    print(json.dumps(response, indent=2)[:300] + "...") # Stampa i primi 300 caratteri
