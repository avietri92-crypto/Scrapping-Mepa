from fastapi import FastAPI, HTTPException
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel
from playwright.sync_api import sync_playwright
import traceback
import time

app = FastAPI()

class RequestData(BaseModel):
    idBando: str
    codiceHash: str

def _execute_playwright_download(id_bando: str, codice_hash: str):
    with sync_playwright() as p:
        # Avvia Chromium in modalità Headless
        browser = p.chromium.launch(headless=True)
        
        # Maschera il browser da client reale
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            locale="it-IT"
        )
        page = context.new_page()

        url_bando = f"https://www.acquistinretepa.it/opencms/opencms/scheda_altri_bandi.html?idBando={id_bando}"
        print(f"[LOG] Caricamento URL: {url_bando}")

        # 'commit' sblocca subito la pagina non appena riceve la risposta iniziale
        page.goto(url_bando, wait_until="commit", timeout=30000)
        
        # Attesa di 4 secondi per lasciare spazio all'esecuzione dei cookie/JS di sessione
        time.sleep(4)

        script_js = """
        async (hash) => {
            const res = await fetch('https://www.acquistinretepa.it/eproc2/documentaleservices/getDocumento', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json;charset=UTF-8',
                    'Accept': 'application/json, text/plain, */*'
                },
                body: JSON.stringify({ id: hash })
            });
            return await res.json();
        }
        """

        print("[LOG] Esecuzione fetch getDocumento nel browser...")
        result_json = page.evaluate(script_js, codice_hash)
        browser.close()
        return result_json

@app.post("/get-pdf")
async def download_pdf(data: RequestData):
    try:
        # Esegue la funzione Playwright in un thread separato gestito da FastAPI
        result = await run_in_threadpool(
            _execute_playwright_download, 
            data.idBando, 
            data.codiceHash
        )
        return result
    except Exception as e:
        print("[ERROR] Errore durante il processo:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
