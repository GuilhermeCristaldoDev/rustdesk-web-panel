import getpass
from sqlmodel import Session, select

from .database import create_db_and_tables, engine
from .security import hash_password
from .models import User

def create_user():
    create_db_and_tables()

    username = input("Digite o username:").strip()

    if not username:
        print("Username não pode ser vazio")
        return

    password = getpass.getpass("Digite a senha: ")

    if len(password) < 8:
        print("A senha precisa ter no minimo 8 caracteres")
        return

    password_confirmation = getpass.getpass("Digite a senha novamente: ")

    if password_confirmation != password:
        print("As senhas não coincidem")
        return

    with Session(engine) as session: 
        user = session.exec(select(User).where(User.username == username)).first()

        if user:
            print("Usuário já existe")
            return 

        new_user = User(
            username=username,
            password_hash=hash_password(password),
        )

        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        print(f"Novo usuário {new_user.username} criado com sucesso!")

if __name__ == '__main__':
    create_user()
