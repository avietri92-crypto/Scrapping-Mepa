import requests

url = "https://mepa.it/Mepa/SearchRdo"
tutti_i_dati = []

skip = 0
batch_size = 10  # da confermare col Payload

while True:
    payload = {"skip": skip, "take": batch_size}  # da adattare ai nomi veri
    response = requests.post(url, json=payload)
    risultato = response.json()

    tutti_i_dati.extend(risultato["data"])
    print(f"Scaricati finora: {len(tutti_i_dati)} / {risultato['totalCount']}")

    if len(tutti_i_dati) >= risultato["totalCount"]:
        break
    skip += batch_size
