import requests

url = "https://mepa.it/Mepa/SearchRdo"

def scarica_pagina(skip, take=10):
    payload = {
        "Descrizione": "",
        "FromDate": "",
        "ToDate": "",
        "Bookmarks": "false",
        "Comments": "false",
        "SortBy": "",
        "SearchType": "",
        "LoadOptions[skip]": skip,
        "LoadOptions[take]": take,
        "LoadOptions[searchOperation]": "contains",
    }
    response = requests.post(url, data=payload)
    response.raise_for_status()  # solleva errore se la richiesta fallisce
    return response.json()

tutti_i_dati = []
skip = 0
take = 10

while True:
    risultato = scarica_pagina(skip, take)
    tutti_i_dati.extend(risultato["data"])
