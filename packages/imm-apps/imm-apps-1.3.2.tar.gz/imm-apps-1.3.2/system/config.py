from pymongo import MongoClient
import os
import dotenv
import certifi

path = os.path.abspath(os.path.join(os.path.expanduser("~"), ".immenv"))
config = dotenv.dotenv_values(path)

# Mongodb
account = config.get("MongoDBUser")
password = config.get("MongoDBPassword")
connection = f"mongodb+srv://{account}:{password}@noah.yi5fo.mongodb.net/test?retryWrites=true&w=majority"
client = MongoClient(connection,tlsCAFile=certifi.where())
database = "test"
db = client[database]

# imm account
imm_account: str = config.get("imm_user")
imm_password: str = config.get("imm_password")


class Default:
    rcic = "jacky"
    rciccompany = "noah"
    temp_num = 1  # for word generation using template
    uploaddir = "."  # for webform, uploading all dir's file
    initial = True  # Only for BCPNP webform to check if it is initial reg or app
    previous = False  # Only for BCPNP webform to check if there is previous application
    user_permission = ["make", "check"]
