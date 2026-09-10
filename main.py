import requests
proxies = {
  "https": "scraperapi:45157fd2ab79ca980e39f985c9868c66@proxy-server.scraperapi.com:8001"
}
r = requests.get('https://mepa.it/home/garemepa', proxies=proxies, verify=False)
print(r.text)

