from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, Session, declarative_base

DATABASE_URL = "mysql+pymysql://root:root@db_mysql:3306/tienda_fastapi"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class ItemDB(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    price = Column(Float)

Base.metadata.create_all(bind=engine)

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
def add_item(name: str = Form(...), price: float = Form(...), db: Session = Depends(get_db)):
    new_item = ItemDB(name=name, price=price)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return RedirectResponse(url="/web", status_code=303)

class ItemSchema(BaseModel):
    name: str
    price: float

@app.post("/items/")
def create_item(item: ItemSchema, db: Session = Depends(get_db)):
    db_item = ItemDB(name=item.name, price=item.price)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

#comandos
#python -m venv .venv
#.\.venv\Scripts\Activate.ps1
#python -m pip install --upgrade pip
#pip install -r .\requirements.txt
#uvicorn src.main:app --port 3000