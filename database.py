import mysql.connector 
from mysql.connector import errorcode
import os
from dotenv import load_dotenv
load_dotenv()

# try:
db = mysql.connector.connect(user=os.getenv("DB_USER"), 
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_DATABASE")
)
print('Connected to Database')
# except mysql.connector.Error as err:
#     if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
#         print("Something is wrong with your user name or password")
#     elif err.errno == errorcode.ER_BAD_DB_ERROR:
#         print("Database does not exist")
#     else:
#         print(err)


def connect():
    db=mysql.connector.connect(user=os.getenv("DB_USER"), 
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_DATABASE")
    )
    print('Reonnected to Database')

cursor = db.cursor()