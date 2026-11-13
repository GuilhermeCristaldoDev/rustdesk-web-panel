from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from datetime import datetime
from sqlmodel import Field, Session, SQLModel, create_engine, select

class ClientBase(SQLModel):
    id: str = Field(primary_key=True)
    name: str = Field(default="Novo Cliente", index=True)

class Client(ClientBase, table=True):
    passwd: str | None = Field(default=None)
    created_at: datetime | None = Field(default_factory=datetime.now, index=True)
    last_session: datetime | None = Field(index=True)

class ClientPublic(ClientBase):
    created_at: datetime | None = None
    last_session: datetime | None = None 

class ClientCreate(ClientBase):
    passwd: str | None = None 

class ClientUpdate(ClientBase):
    id: str | None = None
    name: str | None = None
    passwd: str | None = None

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

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/clients/", response_model=list[ClientPublic])
def read_clients(session: SessionDep):
    clients = session.exec(select(Client)).all()
    return clients

@app.get("/clients/{client_id}", response_model=ClientPublic)
def read_client(client_id: str, session: SessionDep):
    client = session.get(Client, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return client

@app.post("/client/", response_model=ClientPublic)
def create_client(client: ClientCreate, session: SessionDep):
    db_client = Client.model_validate(client)
    session.add(db_client)
    session.commit()
    session.refresh(db_client)
    return db_client

@app.delete("/client/{client_id}")
def delete_client(client_id: str, session: SessionDep):
    client = session.get(Client, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não foi encontrado")
    session.delete(client)
    session.commit()
    return {"ok": True}

@app.patch("/client/{client_id}", response_model=ClientPublic)
def update_client(client_id: str, client: ClientUpdate,session: SessionDep):
    client_db = session.get(Client, client_id)
    if not client_db:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    client_data = client.model_dump(exclude_unset=True)
    client_db.sqlmodel_update(client_data)
    session.add(client_db)
    session.commit()
    session.refresh(client_db)
    return hero_db    


