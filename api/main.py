from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from cryptography.fernet import Fernet
from fastapi.encoders import jsonable_encoder
import json

app=FastAPI()

class Datos(BaseModel):
    linea_captura:str
    client_id:str
    token:str

class DatosEncriptados(BaseModel):
    datos_encriptados: str
    

@app.post("/encriptador/encriptar")
async def encriptarData(datos: Datos):
    try:
        key="tNZzKi8vcbn2aE+Yy8vD4BluYr2QJv9lUY7m3ts1Dt4="
        encriptador=Fernet(key)
        dataEncriptada=encriptador.encrypt(str(jsonable_encoder(datos)).encode())
        
        
        response={"status_code":200,"datos_encriptados":dataEncriptada}

        return response

    except Exception as e:
        print(e)
        return {"status_code":400,"error":str(e)}
    
@app.post("/encriptador/desencriptar")
async def desencriptarData(data:DatosEncriptados):
    try:
        key="tNZzKi8vcbn2aE+Yy8vD4BluYr2QJv9lUY7m3ts1Dt4="
        encriptador=Fernet(key)
        datosDesencriptados=encriptador.decrypt(data.datos_encriptados.encode())
        conversion=datosDesencriptados.decode('utf8').replace("'", '"')
        conversionjson=json.loads(conversion)
        
        
        return conversionjson
        
    except Exception as e:
        return e