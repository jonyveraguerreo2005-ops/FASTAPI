from fastapi import FastAPI, HTTPException
from src.data.db import productos 
from src.models.producto import Producto 

app = FastAPI()

@app.get("/productos", response_model=list[Producto])
async def lista_productos():
    return productos

def siguiente_id() -> int:
    if len(productos) == 0:
        return 1
    else:
        return max(producto.id for producto in productos if producto.id is not None) + 1

@app.post("/productos", response_model=Producto, status_code=201)
async def crear_producto(producto: Producto):
    producto.id = siguiente_id()
    productos.append(producto)
    return producto

def buscar_producto(producto_id: int):
    for producto in productos:
        if producto.id == producto_id:
            return producto
    return None

@app.put("/productos/{producto_id}", response_model=Producto)
async def actualizar_producto(producto_id: int, producto_actualizado: Producto):
    producto = buscar_producto(producto_id)
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")  
    if producto_actualizado.nombre is not None:
        producto.nombre = producto_actualizado.nombre
    if producto_actualizado.fecha_registro is not None:
        producto.fecha_registro = producto_actualizado.fecha_registro
    return producto

@app.delete("/productos/{producto_id}", status_code=204)
async def eliminar_producto(producto_id: int):
    producto = buscar_producto(producto_id)
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    productos.remove(producto)
    return None

#comandos
#python -m venv .venv
#.\.venv\Scripts\Activate.ps1
#python -m pip install --upgrade pip
#pip install -r .\requirements.txt
#uvicorn src.main:app --port 3000