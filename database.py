import mysql.connector 
from mysql.connector import errorcode
import os
from dotenv import load_dotenv
load_dotenv()

db = mysql.connector.connect(user=os.getenv("DB_USER"), 
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_DATABASE")
)
print('Connected to Database')

cursor = db.cursor()



def connect():
    global db
    db=mysql.connector.connect(user=os.getenv("DB_USER"), 
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_DATABASE")
    )
    print('Reconnected to Database')
    
    global cursor 
    cursor= db.cursor()

