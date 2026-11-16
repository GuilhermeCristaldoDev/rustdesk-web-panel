from sqlmodel import SQLModel, Field
from datetime import datetime, timezone


//atributos comuns entre os pymodels
class ClientBase(SQLModel):
    id: str = Field(primary_key=True, min_length=9, max_length=9, regex=r"^[0-9]+$")
    name: str = Field(default="Novo Cliente",max_length=50, index=True)
    device: str | None = Field(default=None, max_length=50)

//tabela clientes
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