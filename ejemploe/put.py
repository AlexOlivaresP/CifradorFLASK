import requests
import json



url = "https://historia-arte.com/_/eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpbSI6WyJcL2FydHdvcmtcL2ltYWdlRmlsZVwvaGFyaW5nLWJlc3QtYnVkZGllcy5qcGciLCJyZXNpemUsODAwIl19.fZIiM_8TQrinlGAM4U6ysCpH9qqdMhSCN4rUiy7atlk.jpg"

#response porque queremos jalar un archivo
#stream porque queremos que se guarde en memoria
response = requests.get(url,stream=True) #realiza la peticion sin descargar el archivo
with open("imagen.jpg","wb") as file: #abrimos el archivo en modo escritura binaria
    for chunk in response.iter_content(): #iteramos sobre el contenido de la respuesta
        file.write(chunk) #escribimos el contenido en el archivo


response.close() #cerramos la conexion

