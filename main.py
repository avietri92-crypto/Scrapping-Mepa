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
        browser = p.chromium.launch(headless=True)
        
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            locale="it-IT",
            viewport={"width": 1280, "height": 800}
        )
        page = context.new_page()

        url_bando = f"https://www.acquistinretepa.it/opencms/opencms/scheda_altri_bandi.html?idBando={id_bando}"
        print(f"[LOG] Caricamento URL: {url_bando}")

        # Carica la pagina del bando fino al DOM
        page.goto(url_bando, wait_until="domcontentloaded", timeout=45000)
        
        # Pausa di 6 secondi per consentire l'esecuzione degli script di bootstrap Angular
        time.sleep(6)

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

            const text = await res.text();
            try {
                return { success: true, data: JSON.parse(text) };
            } catch (e) {
                return { success: false, status: res.status, html_snippet: text.substring(0, 500) };
            }
        }
        """

        print("[LOG] Esecuzione fetch getDocumento nel browser...")
        result = page.evaluate(script_js, codice_hash)
        browser.close()

        if not result["success"]:
            raise Exception(f"Il server MePA ha restituito HTML anziché JSON (Status {result['status']}): {result['html_snippet']}")

        return result["data"]

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
