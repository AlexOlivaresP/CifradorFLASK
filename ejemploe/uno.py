import requests



url = "https://httpbin.org/get"

args = {
    "nombre":"Juan",
    "curso":"python",
    "nivel":"intermedio"
    }

response = requests.get(url,params=args)

print(response.url)

if response.status_code == 200:
    print(response.content)