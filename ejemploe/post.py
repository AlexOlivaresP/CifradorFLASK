import requests



url = "https://httpbin.org/post"

payload = {
    "nombre":"Juan",
    "curso":"python",
    "nivel":"intermedio"
    }
headers = { "Content-Type":"application/json", "access-token":"123456789"}

#para enviar por json
response = requests.post(url,json=payload,headers=headers)
# #para enviar por form
# response = requests.post(url,json=payload)
# #para enviar por data
# response = requests.post(url,data=payload)

#json post se encarga de serializar el diccionario
#data post se encarga de enviarlo como form


print(response.content)