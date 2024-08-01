from pydantic import BaseModel

class Datos(BaseModel):
    linea_captura:str
    client_id:str
    token:str


class DatosEncriptados(BaseModel):
    datos_encriptados: str
    