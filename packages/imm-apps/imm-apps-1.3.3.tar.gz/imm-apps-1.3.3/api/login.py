import requests
from pprint import pprint
from getpass import getpass
from system.config import config, path as IMM_ENV_FILE


def login(email, password):
    session = requests.Session()
    payload = {"username": email, "password": password}
    res = session.post("http://127.0.0.1:8000/login", data=payload)
    if res.status_code == 404:
        print(res.json().get("detail"))
        exit(1)
    session.headers.update(
        {
            "Content-Type": "application/json",
            "Authorization": f"{res.json()['token_type']} {res.json()['access_token']}",
        }
    )
    return session


def get_session():
    if config.get("imm_account") == None or config.get("imm_password") == None:
        imm_account = input("Input your email: ")
        imm_password = getpass()
        try:
            session = login(imm_account, imm_password)
            with open(IMM_ENV_FILE, mode="a") as f:
                f.write(f"\nimm_account={imm_account}\nimm_password={imm_password}")
            return session
        except Exception as e:
            print(e.args)
            exit(1)
    else:
        imm_account = config.get("imm_account")
        imm_password = config.get("imm_password")
        return login(imm_account, imm_password)
