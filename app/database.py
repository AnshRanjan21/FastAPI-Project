from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
#import psycopg2
#from psycopg2.extras import RealDictCursor
#import time 

#SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:password@localhost/fastapi'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.DATABASE_HOSTNAME}:{settings.database_port}/{settings.database_name}'
engine=create_engine(SQLALCHEMY_DATABASE_URL) #think of it as a database engine

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# The "bind" in SQLAlchemy refers to associating a session with a particular database connection.

Base=declarative_base()
#This line defines a base class for your SQLAlchemy models. 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

"""
# we no longer need this while part below since we are using sqlalchemy now to connect to database
while True: # this while loop prevents code from progressing untill a connection has been established
    try:
        conn=psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='password', cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print("Database connection was sucessful")
        break
    except Exception as error:  #error is a variable which is storing the error
        print("Connecting to database failed")
        print("error",error)
        time.sleep(2)
#The cursor_factory=RealDictCursor parameter sets the cursor factory for this connection to RealDictCursor
#meaning that any cursors created from this connection will return query results as dictionaries (with column names as keys).
#cursor = conn.cursor(): After establishing the connection, this line creates a cursor object (cursor) associated with that connection. This cursor can be used to execute SQL commands and queries against the database.
"""