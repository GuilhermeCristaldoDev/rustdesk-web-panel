from typing import Annotated
from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from datetime import datetime, timezone
from sqlmodel import Field, Session, SQLModel, create_engine, select

class ClientBase(SQLModel):
    id: str = Field(primary_key=True, min_length=9, max_length=9, regex=r"^[0-9]+$")
    name: str = Field(default="Novo Cliente",max_length=50, index=True)
    device: str | None = Field(default=None, max_length=50)

class Client(ClientBase, table=True):
    passwd: str | None = Field(default=None, max_length=6)
    created_at: datetime | None = Field(default_factory=lambda: datetime.now(timezone.utc), index=True)
    last_session: datetime | None = Field(default=None, index=True)

class ClientPublic(ClientBase):
    created_at: datetime | None = None
    last_session: datetime | None = None 

class ClientCreate(ClientBase):
    passwd: str | None = Field(default=None, max_length=6)

class ClientUpdate(SQLModel):
    name: str | None = Field(default=None, max_length=50) 
    device: str | None = Field(default=None, max_length=50)
    passwd: str | None = Field(default=None, max_length=6)
   
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)    

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def ler_pagina():
    return FileResponse("static/index.html")

@app.get("/clients/", response_model=list[ClientPublic])
def read_clients(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=20)] = 20
    ):
    clients = session.exec(select(Client).offset(offset).limit(limit)).all()
    return clients

@app.get("/clients/{client_id}", response_model=ClientPublic)
def read_client(client_id: str, session: SessionDep):
    client = session.get(Client, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return client

@app.post("/clients/", response_model=ClientPublic)
def create_client(client: ClientCreate, session: SessionDep):
    client_exists = session.get(Client, client.id)
    if client_exists:
        raise HTTPException(status_code=409, detail="Esse cliente já existe")
    db_client = Client.model_validate(client)
    session.add(db_client)
    session.commit()
    session.refresh(db_client)
    return db_client

@app.delete("/clients/{client_id}")
def delete_client(client_id: str, session: SessionDep):
    client = session.get(Client, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não foi encontrado")
    session.delete(client)
    session.commit()
    return {"ok": True}

@app.patch("/clients/{client_id}", response_model=ClientPublic)
def update_client(client_id: str, client: ClientUpdate,session: SessionDep):
    client_db = session.get(Client, client_id)
    if not client_db:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    client_data = client.model_dump(exclude_unset=True)
    client_db.sqlmodel_update(client_data)
    session.add(client_db)
    session.commit()
    session.refresh(client_db)
    return client_db    


