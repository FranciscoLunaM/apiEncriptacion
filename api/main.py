import logging
from fastapi import FastAPI,HTTPException, Request,status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from models.datos import Datos,DatosEncriptados
from cryptography.fernet import Fernet
from fastapi.encoders import jsonable_encoder
import json
from dotenv import load_dotenv
import os
import consul
import socket

load_dotenv()
keygen=os.getenv("KEY")
consul_ip=os.getenv("CONSUL_IP")
consul_port=os.getenv("CONSUL_PORT")
ip=os.getenv("SERVER_IP")
port=os.getenv("PORT")

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip_address =s.getsockname()[0]

#consul

c=consul.Consul(host=consul_ip,port=consul_port)
c.agent.service.register('servicio-encriptacion',
                        service_id='servicio-encriptacion',
                        port=int(port),
                        address=ip_address,
                        tags=['servicio-encriptacion'])

#endConsul

app=FastAPI()

@app.post("/encriptador/encriptar",response_model=DatosEncriptados)
async def encriptarData(datos: Datos):
    try:
        key:str=keygen
        encriptador:str=Fernet(key)
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
    
    
    
#uvicorn main:app --host 0.0.0.0 --port 9001  <-- asi se levanta el sistema