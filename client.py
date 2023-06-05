import requests
import json
import logging
import time

# Configurar el registro
logging.basicConfig(filename='bitacora.log', level=logging.DEBUG, filemode='w',
                    format='%(asctime)s | %(levelname)s:%(message)s | %(threadName)s | %(funcName)s | %(lineno)d|')

# Crear logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Crear manejador para la consola
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# Formatear mensaje de log
formatter = logging.Formatter('%(levelname)s || %(message)s')
ch.setFormatter(formatter)

# Agregar manejador al logger
logger.addHandler(ch)


def cifrado(texto, desplazamiento):
    texto = texto.upper()
    alfabeto = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
    cifrado = ""
    for letra in texto:
        if letra in alfabeto:
            posicion = alfabeto.find(letra)
            nueva_posicion = (posicion + desplazamiento) % 27
            cifrado += alfabeto[nueva_posicion]
        else:
            cifrado += letra
    return cifrado


def decifrado(cifrado, corrimientos):
    cifrado = cifrado.upper()
    alfabeto = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
    decifrado = ""
    for letra in cifrado:
        if letra in alfabeto:
            posicion = alfabeto.find(letra)
            nueva_posicion = (posicion - corrimientos) % 27
            decifrado += alfabeto[nueva_posicion]
        else:
            decifrado += letra
    return decifrado


def serverStat():
    logging.debug(f"TESTEANDO LOS SERVIDORES ...")
    url = "http://localhost:5000/libres"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        libres = data['libres']
        print(f"Servidores libres: {libres}")
        return libres
    else:
        print("Error al obtener la información de los servidores")


def solicitud(texto, desplazamiento):
    logging.debug(f"Solicitando servidor al gsc desde el cliente ...")
    url = "http://localhost:5000/solicitud"
    #payload es la información que se envía al servidor
    payload = {
        "texto": texto,
        "desplazamiento": desplazamiento
    }
    #define que el formato de la información que se envía es json
    headers = {
        "Content-Type": "application/json"
    }
    #envía la información al servidor
    #response es la respuesta del servidor
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    #si la respuesta es 200, se obtiene el resultado
    if response.status_code == 200:
        #data es la información que se obtiene del servidor
        #response.json() convierte la información en un diccionario
        #data contiene el diccionario con los valores de la respuesta del servidor, son 2 valores: resultado y servidor
        data = response.json()
        resultado = data['resultado']
        return resultado
    else:
        print("Error al solicitar el servidor")
        return None


logging.debug("Iniciando programa")
logging.debug("Leyendo archivo")
try:
    with open("texto.txt", "r") as archivo:
        Frase = archivo.read()
except (FileNotFoundError, IOError) as e:
    logging.error(f"Error al abrir el archivo: {e}")

#serverStat()

if serverStat() == 0:
    logging.debug("No hay servidores disponibles")
    print("No hay servidores disponibles")
    time.sleep(10)
    exit()

Desplazamiento = int(input("Ingrese el desplazamiento: "))
print("\n\n")

logging.debug("Dividiendo texto en 2")
mitad = len(Frase) // 2
texto1 = Frase[:mitad]
texto2 = Frase[mitad:]

# logging.debug("Cifrando texto 1")
# cifrado1 = cifrado(texto1, Desplazamiento)

# logging.debug("Cifrando texto 2")
# cifrado2 = cifrado(texto2, Desplazamiento)

logging.debug("Solicitando servidor para texto 1")
resultado1 = solicitud(texto1, Desplazamiento)

logging.debug("Solicitando servidor para texto 2")
resultado2 = solicitud(texto2, Desplazamiento)

if resultado1 is not None and resultado2 is not None:
    logging.debug("Decifrando resultado 1")
    decifrado1 = decifrado(resultado1, Desplazamiento)

    logging.debug("Decifrando resultado 2")
    decifrado2 = decifrado(resultado2, Desplazamiento)

    logging.debug("Uniendo resultados")
    resultado_final = decifrado1 + decifrado2

    #print(f"Resultado final: {resultado_final}")
else:
    logging.debug("Error en la solicitud de los servidores")

logging.debug("Programa finalizado")

with open("resultado.txt", "w") as archivo:
    archivo.write(resultado1+"\n"+resultado2+"\n")

