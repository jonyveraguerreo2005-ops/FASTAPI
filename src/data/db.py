from src.models.producto import Producto
from datetime import date 

productos: list[Producto] = [
    Producto(id=1, nombre="Portatil ASUS", fecha_registro="2022-01-15", disponible=True),
    Producto(id=2, nombre="Monitor 4K Lenovo", fecha_registro="2020-03-01", disponible=True),
    Producto(id=3, nombre="Teclado Mecánico Corsair", fecha_registro="2021-11-20", disponible=False)
]