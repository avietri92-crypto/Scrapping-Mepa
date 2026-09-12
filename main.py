from fastapi import FastAPI
from pydantic import BaseModel
import asyncio
from playwright.async_api import async_playwright
import os
import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
    
app = FastAPI()

class RequestData(BaseModel):
    idBando: str
    codiceHash: str

@app.post("/get-pdf")
async def download_pdf(data: RequestData):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        url_bando = f"https://www.acquistinretepa.it/opencms/opencms/scheda_altri_bandi.html?idBando={data.idBando}"
        await page.goto(url_bando, wait_until="networkidle")

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
        result_json = await page.evaluate(script_js, data.codiceHash)
        await browser.close()
        return result_json

# Per avviarlo: uvicorn main:app --reload --port 8000
