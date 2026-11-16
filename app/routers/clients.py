from typing import Annotated
from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select

from ..database import SessionDep
from ..models import Client, ClientCreate, ClientUpdate, ClientPublic

router = APIRouter(prefix="/clients", tags=["clients"])

@router.get("/", response_model=list[ClientPublic])
def read_clients(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=20)] = 20
    ):
    clients = session.exec(select(Client).offset(offset).limit(limit)).all()
    return clients

@router.get("/{client_id}", response_model=ClientPublic)
def read_client(client_id: str, session: SessionDep):
    client = session.get(Client, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return client

@router.post("/", response_model=ClientPublic)
def create_client(client: ClientCreate, session: SessionDep):
    client_exists = session.get(Client, client.id)
    if client_exists:
        raise HTTPException(status_code=409, detail="Esse cliente já existe")
    db_client = Client.model_validate(client)
    session.add(db_client)
    session.commit()
    session.refresh(db_client)
    return db_client

@router.delete("/{client_id}")
def delete_client(client_id: str, session: SessionDep):
    client = session.get(Client, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não foi encontrado")
    session.delete(client)
    session.commit()
    return {"ok": True}

@router.patch("/{client_id}", response_model=ClientPublic)
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
