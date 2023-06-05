from flask import Flask, jsonify, request
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

app = Flask(__name__)

libres = 2

@app.route('/libres', methods=['GET'])
def get_libres():
    return jsonify({'libres': libres})

@app.route('/solicitud', methods=['POST'])
def solicitud():
    global libres
    data = request.get_json()
    texto = data['texto']
    desplazamiento = data['desplazamiento']
    
    if libres > 0:
        libres -= 1
        #logging.debug(f"Solicitud recibida - Texto: {texto} | Desplazamiento: {desplazamiento}")
        cifrado_texto = cifrado(texto, desplazamiento)
        #logging.debug(f"Solicitud procesada - Texto cifrado: {cifrado_texto}")
        libres += 1
        return jsonify({'resultado': cifrado_texto})
    else:
        logging.debug(f"Error: No hay servidores disponibles")
        return jsonify({'resultado': None})

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

if __name__ == '__main__':
    app.run(debug=True)
