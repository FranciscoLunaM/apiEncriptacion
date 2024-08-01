from fastapi import FastAPI,HTTPException,status
from models.datos import Datos,DatosEncriptados
from cryptography.fernet import Fernet
from fastapi.encoders import jsonable_encoder
import json
from dotenv import load_dotenv
import os
import consul

load_dotenv()
keygen=os.getenv("KEY")
consul_ip=os.getenv("CONSUL_IP")
consul_port=os.getenv("CONSUL_PORT")
ip=os.getenv("SERVER_IP")
port=os.getenv("PORT")

#consul
"""
c=consul.Consul(host=consul_ip,port=consul_port)
c.agent.service.register('servicio-encriptacion',
                        service_id='servicio-encriptacion',
                        port=port,
                        address=ip,
                        tags=['servicio-encriptacion'])"""

#endConsul

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
    
#uvicorn main:app --host 0.0.0.0 --port 9001  <-- asi se levanta el sistema