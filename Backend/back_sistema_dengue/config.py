from dotenv import load_dotenv
import os

load_dotenv()

user = os.environ["USER"]
password = os.environ["PASSWORD"]
host = os.environ["HOST"]
database = os.environ["DATABASE"]
server = os.environ["SERVER"]

DATABASE_CONNECTION_URI = f'{server}://{user}:{password}@{host}/{database}'
print(DATABASE_CONNECTION_URI)
