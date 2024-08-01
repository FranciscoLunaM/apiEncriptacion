from fastapi import FastAPI,HTTPException,status
from models.datos import Datos,DatosEncriptados
from cryptography.fernet import Fernet
from fastapi.encoders import jsonable_encoder
import json
from dotenv import load_dotenv
import os
load_dotenv()

keygen=os.getenv("KEY")

app=FastAPI()

@app.post("/encriptador/encriptar",response_model=DatosEncriptados)
async def encriptarData(datos: Datos):
    try:
        key=keygen
        encriptador=Fernet(key)
        dataEncriptada=encriptador.encrypt(str(jsonable_encoder(datos)).encode())
        response=DatosEncriptados(**{"datos_encriptados":dataEncriptada.decode()})

        return response

    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=status.HTTP_417_EXPECTATION_FAILED,detail=str(e))
    
@app.post("/encriptador/desencriptar",response_model=Datos)
async def desencriptarData(data:DatosEncriptados):
    try:
        key=keygen
        
        encriptador=Fernet(key)
        datosDesencriptados=encriptador.decrypt(data.datos_encriptados.encode())
        conversion=datosDesencriptados.decode('utf8').replace("'", '"')
        conversionjson=json.loads(conversion)
  
        return Datos(**conversionjson)
        
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=status.HTTP_417_EXPECTATION_FAILED,detail=str(e))