"""
@authors: Enaitz Otazua y Victor del Barrio
@desc: Este programa lee datos de temperatura y humedad
de sensores acoplados a la Raspbery y los sube a Thinspeak utilizando el protocolo HTTP
"""

# importamos las librerias que queremos usar
import httplib
import urllib
import json
import time
import Adafruit_DHT

# definimos la API_KEY necesaria de nuestra cuenta
# y el servidor al que subimos los datos
USER_API_KEY ='4YT93L5Q42UD9W5S'
server = 'api.thingspeak.com'

# establecemos conexion con el servidor
connTCP = httplib.HTTPSConnection(server)
print ("Estableciendo conexion TCP...")
connTCP.connect()
print("Conexion TCP establecida")


###################################################################################################
# Creacion del PRIMER canal para el almacenamiento de datos
print("Creando canal 1...")
method = "POST"
relative_uri = "/channels.json"
headers ={'Host': server,
          'Content-Type':'application/x-www-form-urlencoded'}
payload ={'api_key':USER_API_KEY,
          'name':'Parametros atmosfericos. CANAL 1',
          'field1':'TEMPERATURA',
          'field2':'HUMEDAD'}
payload_encoded = urllib.urlencode(payload)
headers['Content-Length'] = len(payload_encoded)
print ("\t Enviando peticion de creacion de canal 1...")
connTCP.request(method,relative_uri,headers=headers,body=payload_encoded)

print("\tRecibinedo respuesta")
respuesta = connTCP.getresponse()
status = respuesta.status
print("\tStatus: " + str(status))
contenido = respuesta.read()
contenido_json = json.loads(contenido)
CHANNEL_1_ID = contenido_json['id']
WRITE_API_KEY_1 = contenido_json['api_keys'][0]['api_key']

####################################################################################################
# Creacion del SEGUNDO canal para el almacenamiento de datos
print("Creando canal 2...")
method = "POST"
relative_uri = "/channels.json"
headers ={'Host': server,
          'Content-Type':'application/x-www-form-urlencoded'}
payload ={'api_key':USER_API_KEY,
          'name':'Parametros atmosfericos. CANAL 2',
          'field1':'TEMPERATURA',
          'field2':'HUMEDAD'}
payload_encoded = urllib.urlencode(payload)
headers['Content-Length'] = len(payload_encoded)
print ("\t Enviando peticion de creacion de canal 2...")
connTCP.request(method,relative_uri,headers=headers,body=payload_encoded)

print("\tRecibinedo respuesta")
respuesta = connTCP.getresponse()
status = respuesta.status
print("\tStatus: " + str(status))
contenido = respuesta.read()
contenido_json = json.loads(contenido)
CHANNEL_2_ID = contenido_json['id']
WRITE_API_KEY_2 = contenido_json['api_keys'][0]['api_key']

################################################################################################
# Captura de datos mediante la estacion meteorologica
try:
    # Utilizamos un flag para determinar el canal en el que debemos guardar
    # los datos en funcion del instante en el que se ha tomado la medida
    sensor = Adafruit_DHT.AM2302
    pin = '4'
    flag = True
    while (True):
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin, delay_seconds=0.00)
        print('Temperatura:{0:0.1f}\tHumedad:{1:0.1f}'.format(temperature, humidity))
		
        if flag == True:
            WRITE_API_KEY = WRITE_API_KEY_1
        else:
            WRITE_API_KEY = WRITE_API_KEY_2
        # creamos la peticion http
        # que sube datos a mi canal de thingspeak
        # https://es.mathworks.com/help/thingspeak/writedata.html
        method = "POST"
        relative_uri = "/update.json"
        headers = {'Host': server,
                   'Content-Type': 'application/x-www-form-urlencoded'}
        payload = {'api_key': WRITE_API_KEY,
                   'field1': temperature,
                   'field2': humidity}
        # codificamos los datos a enviar
        payload_encoded = urllib.urlencode(payload)
        headers['Content-Length'] = len(payload_encoded)

        print("Enviando peticion HTTP ...")
        connTCP.request(method, relative_uri, body=payload_encoded, headers=headers)
        print("Peticion enviada")

        print("Esperando respuesta HTTP...")
        respuesta = connTCP.getresponse()
        status = respuesta.status
        print(str(status))
        flag = not flag
		time.sleep(10)
		
except KeyboardInterrupt:
    connTCP.close()
    print("Se ha pulsado Crtl+C. Saliendo del programa...")

