from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from datetime import datetime
from sqlmodel import Field, Session, SQLModel, create_engine, select

class Client(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: str = Field(default="Novo Cliente", index=True)
    passwd: str | None = Field(default=None)
    crated_at: datetime | None = Field(default_factory=datetime.now, index=True)
    last_session: datetime | None = Field(index=True)

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

@app.get("/clients/")
def read_clients(session: SessionDep) -> list[Client]:
    clients = session.exec(select(Client)).all()
    return clients

@app.get("/clients/{client_id}")
def read_client(client_id: str, session: SessionDep) -> Client:
    client = session.get(Client, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return client

@app.post("/client/")
def create_client(client: Client, session: SessionDep) -> Client:
    session.add(client)
    session.commit()
    session.refresh(client)
    return client

@app.delete("client")
def delete_client(client_id: str, session: SessionDep):
    client = session.get(Client, client_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Cliente não foi encontrado")
    session.delete(client)
    session.commit()
    return {"ok": True}

