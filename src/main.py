import os
from fastapi import FastAPI, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, Session, declarative_base


DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:@localhost:3306/tienda_fastapi")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ItemDB(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    price = Column(Float)

Base.metadata.create_all(bind=engine)

class ItemSchema(BaseModel):
    name: str
    price: float

class ItemResponse(ItemSchema):
    id: int
    class Config:
        from_attributes = True

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get("/web", response_class=HTMLResponse)
def read_web(request: Request, db: Session = Depends(get_db)):
    items = db.query(ItemDB).all()
    return templates.TemplateResponse("inicio.html", {"request": request, "items": items})

@app.post("/add")
def add_item_web(name: str = Form(...), price: float = Form(...), db: Session = Depends(get_db)):
    new_item = ItemDB(name=name, price=price)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return RedirectResponse(url="/web", status_code=303)



@app.get("/productos", response_model=list[ItemResponse])
def lista_productos(db: Session = Depends(get_db)):
    return db.query(ItemDB).all()

@app.post("/productos", response_model=ItemResponse, status_code=201)
def crear_producto(item: ItemSchema, db: Session = Depends(get_db)):
    new_item = ItemDB(name=item.name, price=item.price)
    db.add(new_item)
    db.commit()
    db.refresh(new_item) 
    return new_item

@app.put("/productos/{producto_id}", response_model=ItemResponse)
def actualizar_producto(producto_id: int, item_actualizado: ItemSchema, db: Session = Depends(get_db)):
    item_db = db.query(ItemDB).filter(ItemDB.id == producto_id).first()
    
    if item_db is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    item_db.name = item_actualizado.name
    item_db.price = item_actualizado.price
    
    db.commit()
    db.refresh(item_db)
    return item_db

@app.delete("/productos/{producto_id}", status_code=204)
def eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    item_db = db.query(ItemDB).filter(ItemDB.id == producto_id).first()
    
    if item_db is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    db.delete(item_db)
    db.commit()
    return None

#comandos
#python -m venv .venv
#.\.venv\Scripts\Activate.ps1
#python -m pip install --upgrade pip
#pip install -r .\requirements.txt
#uvicorn src.main:app --port 3000