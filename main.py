from fastapi import FastAPI
from datetime import datetime

class Client(SQLModel, table=true):
    id: str = Field(primary_key=True)
    name: str = Field(default="Novo Cliente", index=True)
    passwd: str | None = Field(default=None)
    crated_at: datetime | None = Field(default_factory=datetime.nown index=True)
    last_session: datetime | None = Field(index=True)

@app.get("/clients")
def get_clients():
    return clients

@app.get("/clients/{client_id}")
def get_client(client_id):
    return client

