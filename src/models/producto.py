from datetime import date
from pydantic import BaseModel

class Producto(BaseModel):
    id: int | None = None          
    nombre: str | None = None      
    fecha_registro: date | None = None 
    disponible: bool | None = None 