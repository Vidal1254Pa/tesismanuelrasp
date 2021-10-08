import requests
from time import sleep
#import serial
from datetime import datetime
import pyrebase as pybase
import uuid
import json
import os
import os.path as path
import webbrowser as wb

import random

diccionario_aleatorio = {
    "S" : {
    1 : {"val" : 97, "porc": 10},
    2 : {"val" : 98, "porc": 80},
    3 : {"val" : 99, "porc": 10},
    },
    "T" : {
    1 : {"val" : 36.3, "porc": 5},
    2 : {"val" : 36.4, "porc": 20},
    3 : {"val" : 36.5, "porc": 50},
    4 : {"val" : 36.6, "porc": 20},
    5 : {"val" : 36.7, "porc": 5},
    },
    "B" : {
        "A":{
            "F":{
            1 : {"val" : 74, "porc": 8},
            2 : {"val" : 75, "porc": 12},
            3 : {"val" : 76, "porc": 15},
            4 : {"val" : 77, "porc": 30},
            5 : {"val" : 78, "porc": 15},
            6 : {"val" : 79, "porc": 12},
            7 : {"val" : 80, "porc": 8}
            },
            "M":{
            1 : {"val" : 74, "porc": 8},
            2 : {"val" : 75, "porc": 12},
            3 : {"val" : 76, "porc": 15},
            4 : {"val" : 77, "porc": 30},
            5 : {"val" : 78, "porc": 15},
            6 : {"val" : 79, "porc": 12},
            7 : {"val" : 80, "porc": 8}
            }
        },
        "B":{
            "F":{
            1 : {"val" : 76, "porc": 15},
            2 : {"val" : 77, "porc": 20},
            3 : {"val" : 78, "porc": 30},
            4 : {"val" : 79, "porc": 20},
            5 : {"val" : 80, "porc": 15}
            },
            "M":{
            1 : {"val" : 78, "porc": 15},
            2 : {"val" : 79, "porc": 20},
            3 : {"val" : 80, "porc": 30},
            4 : {"val" : 81, "porc": 20},
            5 : {"val" : 82, "porc": 15}
            }
        },
        "C":{
            "F":{
            1 : {"val" : 68, "porc": 15},
            2 : {"val" : 69, "porc": 20},
            3 : {"val" : 70, "porc": 30},
            4 : {"val" : 71, "porc": 20},
            5 : {"val" : 72, "porc": 15}
            },
            "M":{
            1 : {"val" : 68, "porc": 15},
            2 : {"val" : 69, "porc": 20},
            3 : {"val" : 70, "porc": 30},
            4 : {"val" : 71, "porc": 20},
            5 : {"val" : 72, "porc": 15}
            }
        },
        "D":{
            "F":{
            1 : {"val" : 75, "porc": 15},
            2 : {"val" : 76, "porc": 20},
            3 : {"val" : 77, "porc": 30},
            4 : {"val" : 78, "porc": 20},
            5 : {"val" : 79, "porc": 15},
            6 : {"val" : 80, "porc": 15},
            7 : {"val" : 81, "porc": 15}
            },
            "M":{
            1 : {"val" : 75, "porc": 15},
            2 : {"val" : 76, "porc": 20},
            3 : {"val" : 77, "porc": 30},
            4 : {"val" : 78, "porc": 20},
            5 : {"val" : 79, "porc": 15},
            6 : {"val" : 80, "porc": 15},
            7 : {"val" : 81, "porc": 15}
            }
        }
    },
}

dic_val = {
    "val_antiguo_B" : -1,
    "porc_antiguo_B" : -1,
    "val_antiguo_S" : -1,
    "porc_antiguo_S" : -1,
    "val_antiguo_T" : -1,
    "porc_antiguo_T" : -1,
}

def aleatorio(tipo, edad, sexo):
    num_aleatorio = random.randrange(0, 100, 1)
    result = 0
    porc_result = 0
    acum = 0
    if tipo != "B":
        for key in diccionario_aleatorio[tipo]:
            data = diccionario_aleatorio[tipo][key]
            if acum <= num_aleatorio < acum + data['porc']:
                result = data["val"]

            acum += data['porc']
    else:
        for key in diccionario_aleatorio[tipo][edad][sexo]:
            data = diccionario_aleatorio[tipo][edad][sexo][key]
            if acum <= num_aleatorio < acum + data['porc']:
                result = data["val"]

            acum += data['porc']


    if dic_val['porc_antiguo_'+tipo] == -1:
        dic_val['val_antiguo_'+tipo] = result
        dic_val['porc_antiguo_'+tipo] = num_aleatorio
    else:
        if(abs(num_aleatorio - dic_val['porc_antiguo_'+tipo]) > 25):
            result = dic_val['val_antiguo_'+tipo]
    return result
    

definerIdentifierEquipe='E-001'
myUUID = uuid.uuid4()
ContadorTemp=0
ContadorPulso=0
dataTemp={}
dataPulso={}
dataBreackandSave=True
from threading import Thread

firebaseConfig = {
    "apiKey": "AIzaSyDrAe52D9Bu8iwvmQWtQetakT5LNtJxQkU",
    "authDomain": "tesispruebas-a6896.firebaseapp.com",
    "databaseURL": "https://tesispruebas-a6896-default-rtdb.firebaseio.com",
    "projectId": "tesispruebas-a6896",
    "storageBucket": "tesispruebas-a6896.appspot.com",
    "messagingSenderId": "199497932992",
    "appId": "1:199497932992:web:9006841cc32307e9584d25"
  };
credencialesStreamer=pybase.initialize_app(firebaseConfig)
escuchar=credencialesStreamer.database()

def Temp():
    while True:
        global DatoPulso
        global ContadorPulso
        ContadorPulso=ContadorPulso+1
        DatoPulso=aleatorio("B","A","F")
        DatoOxig=aleatorio("S","A","F")
        escuchar.child(f"{definerIdentifierEquipe}/Data").update({'Pulso':"{0:.2f}bpm / SPO2:{1:.2f}%".format(DatoPulso,DatoOxig)})
        dataPulso[f"{ContadorPulso}"]={"Data":DatoPulso,"Fech":datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        
        
def Pulso():
    while True:
        global DatoTemp
        global ContadorTemp
        ContadorTemp=ContadorTemp+1
        DatoTemp=aleatorio("T","A","F")
        escuchar.child(f"{definerIdentifierEquipe}/Data").update({'Temp':"{0:.2f}°C".format(DatoTemp)})
        dataTemp[f"{ContadorTemp}"]={"Data":DatoTemp,"Fech":datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        
        
HiloPulso = Thread(target=Pulso);
HiloTemp = Thread(target=Temp);
dic = {'-': '_',
                   ':': '_',
                   ' ': '_'}
def onchangeConfircloseDataCharge(value):
    global dataBreackandSave
    if value['data']==1:
        dataBreackandSave=True
        print(dataBreackandSave)
    else:
        print("holis")
        dataBreackandSave=False

fileName = "/home/pi/Desktop/ActivateEquipo.json"
"""if os.path.exists(fileName):
	f = open ('/home/pi/Desktop/ActivateEquipo.json','r')
	mensaje = f.read()
	dataConvert = json.loads(mensaje)
	wb.open(f"http://192.168.43.211/MonitorSensor/{definerIdentifierEquipe}?token={dataConvert['TOCKEN']}", new=2, autoraise=True)
else:
	URL = f"http://192.168.43.211/api/SetDataTocken/{definerIdentifierEquipe}"
	PARAMS = {"TOCKEN":myUUID}
	r = requests.post(url = URL, params = PARAMS)
	data = r.json()
	print(PARAMS)
	if int(data['mensaje']['type'])==1:	
		with open('/home/pi/Desktop/ActivateEquipo.json', 'w') as file:
			json.dump({"TOCKEN":str(myUUID)}, file, indent=4)"""
print(definerIdentifierEquipe)
escuchar.child(f"{definerIdentifierEquipe}/estate").stream(onchangeConfircloseDataCharge,stream_id="1")
HiloPulso.start();
HiloTemp.start();
"""while True:
    dataBreackandSave=True
    Adjun={}
    while dataBreackandSave==True:
        print('wey')
    controleRegistro=datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    with open(f"/home/pi/Desktop/DataSave/{controleRegistro}dataTemp.json", 'w') as file:
        json.dump(dataTemp, file, indent=4)
    with open(f"/home/pi/Desktop/DataSave/{controleRegistro}dataPulso.json", 'w') as file:
        json.dump(dataPulso, file, indent=4)
    dataTempjson = open (f"/home/pi/Desktop/DataSave/{controleRegistro.translate(str.maketrans(dic))}dataTemp.json",'r')
    Adjun['Temp'] = json.loads(dataTempjson.read())
    dataPulsojson = open (f"/home/pi/Desktop/DataSave/{controleRegistro.translate(str.maketrans(dic))}dataPulso.json",'r')
    Adjun['Pulso'] = json.loads(dataPulsojson.read())
    validate=''
    try:
        URL = f"http://192.168.43.211/api/ControlTemandPulso/{definerIdentifierEquipe}?jsondata={json.dumps(Adjun)}&fechRegister={controleRegistro}"
        r = requests.post(url = URL)
        data = r.json()
        print(data)
        sleep(10)
        validate=True
    except Exception as exc:
        print(exc)
        validate=False
    if validate: 
        try:  
            if data['mensaje']['type']==True:
                cadena={}
                fileNameDataReceived = "/home/pi/Desktop/dataReceivedConfirm.json"
                if os.path.exists(fileNameDataReceived):
                    cadena[f"{controleRegistro}"]='Acepted'
                    with open(f"/home/pi/Desktop/dataReceivedConfirm.json", 'w') as file:
                        json.dump(cadena, file, indent=4)
                else:
                    f = open ('/home/pi/Desktop/dataReceivedConfirm.json','r')
                    mensaje = f.read()
                    cadena=json.loads(mensaje)
                    cadena[f"{controleRegistro}"]='Acepted'
                    with open(f"/home/pi/Desktop/dataReceivedConfirm.json", 'w') as file:
                        json.dump(cadena, file, indent=4)
        except Exception as ex:
            print(ex)
    else:
        if os.path.exists(fileNameDataReceived):
            cadena[f"{controleRegistro}"]='Acepted'
            with open(f"/home/pi/Desktop/dataReceivedConfirm.json", 'w') as file:
                json.dump(cadena, file, indent=4)
        else:
            f = open ('/home/pi/Desktop/dataReceivedConfirm.json','r')
            mensaje = f.read()
            cadena=json.loads(mensaje)
            cadena[f"{controleRegistro}"]='Acepted'
            with open(f"/home/pi/Desktop/dataReceivedConfirm.json", 'w') as file:
                json.dump(cadena, file, indent=4)"""