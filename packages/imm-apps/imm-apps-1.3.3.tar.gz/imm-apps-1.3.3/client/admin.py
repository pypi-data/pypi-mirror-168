# import context
from pprint import pprint
import typer
from rich.console import Console
from rich.text import Text
from getpass import getpass
from api.login import login, get_session
import requests
from typing import List
from api.hashing import Hash

app = typer.Typer()
console = Console()

headers = {"accept": "application/json", "Content-Type": "application/json"}


def get_id_by_email(session: requests.Session, email: str):
    users = session.get("http://localhost:8000/user/")
    for user in users.json()["data"]:
        if email == user.get("email"):
            return user.get("_id")


def delete_by_email(session: requests.Session, email: str):
    user_id = get_id_by_email(session, email)
    res = session.delete(f"http://localhost:8000/user/{user_id}")
    result = res.json()
    if result.get("status_code") == 204:
        f"Record with id {user_id} has been deleted.",
        return user_id
    elif result.get("status_code") == 401:
        print(res.json().get("detail"))
    else:
        print(f"No record with email as {email}")


def delete_by_id(session: requests.Session, id: str):
    res = session.delete(f"http://localhost:8000/user/{id}")
    status = res.json()
    if status["status_code"] == 204:
        print(
            f"Record with id {id} has been deleted.",
        )
    elif status["status_code"] == 401:
        print("Error:", status["detail"])


@app.command()
def register(
    username: str = typer.Argument(None, help="User name"),
    email: str = typer.Argument(None, help="Email, used as login name"),
    phone: str = typer.Argument(None, help="Telephone"),
):
    psw1 = getpass()
    psw2 = getpass("Input password again: ")
    if psw1 != psw2:
        raise ValueError("The two passwords are not same.")
    user = {
        "username": username,
        "email": email,
        "phone": phone,
        "password": psw2,
    }
    r = requests.post("http://localhost:8000/user/", json=user)
    if r.status_code == 200:
        print(r.json())
    else:
        print(r.status_code, r.json["detail"])


@app.command()
def show(
    email: str = typer.Argument(None, help="Email, used as login name"),
    id: str = typer.Option(None, help="id, record id"),
):
    session = get_session()
    if id:
        r = session.get(f"http://localhost:8000/user/{id}")
    elif email:
        id = get_id_by_email(session, email)
        if id:
            r = session.get(f"http://localhost:8000/user/{id}")
        else:
            print(f"No user with email as {email}")
            exit(1)
    else:
        r = session.get("http://localhost:8000/user/")
    if r.status_code == 200:
        pprint(r.json()["data"])
    else:
        print(r.status_code, r.json().get("detail"))


@app.command()
def delete(
    email: str = typer.Argument(None, help="Email, used as login name"),
    id: str = typer.Option(None, help="id, record id"),
):
    session = get_session()
    if email:
        delete_by_email(session, email)
    elif id:
        delete_by_id(session, id)
    else:
        print("You have to either assign email or _id")


@app.command()
def role(user_email: str, role: str):
    session = get_session()
    data = {"user_email": user_email, "role": role}
    r = session.post("http://localhost:8000/user/role", json=data)
    print(r.status_code, r.json())


@app.command()
def permission(
    user_email: str,
    remove: bool = typer.Option(False),
    permission: List[str] = typer.Option(None),
):
    session = get_session()
    data = {"user_email": user_email, "permissions": list(permission), "remove": remove}
    r = session.post("http://localhost:8000/user/permission", json=data)
    print(r.status_code, r.json())


@app.command()
def password(user_email: str, password: str):
    session = get_session()
    _id = get_id_by_email(session, user_email)
    query = {"password": password}
    r = session.put(f"http://localhost:8000/user/password/{_id}", params=query)
    print(
        "Your password has been updated successfully. Don't forget to update the imm_password variable  in .immenv file  "
    )


if __name__ == "__main__":
    try:
        app()
    except Exception as e:
        print(e)
