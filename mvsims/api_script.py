from sqlalchemy import create_engine, Integer, Column, String, Float, DateTime, Table, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.sql import text as sa_text
from sqlalchemy.engine import URL

import time
from datetime import datetime, timedelta
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Access environment variables
username = os.getenv('AUTH_USER')
password = os.getenv('AUTH_PASS')

auth_url = 'https://console.monogoto.io/Auth'
things_url = 'https://console.monogoto.io/things'
thing_url = 'https://console.monogoto.io/thing/'
invoice_url = 'https://console.monogoto.io/billingreports/customerInvoices/'

auth_payload = {
    "UserName": username,
    "Password": password
}

DB_USER_NM = os.getenv('DB_USER_NM')
DB_USER_PW = os.getenv('DB_USER_PW')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_TABLE_NAME = os.getenv('DB_TABLE_NAME')

db_url = f'postgresql+psycopg2://{DB_USER_NM}:{DB_USER_PW}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

def getAuthToken():
    auth_response = requests.post(auth_url, headers={'Content-Type': 'application/json'}, data=json.dumps(auth_payload))
    if auth_response.status_code == 200:
        auth_data = auth_response.json()
        token = auth_data.get('token')
        return token

token = getAuthToken()

def getThings():
    things_response = requests.get(things_url, headers={
        'Accept': 'application/json',
        'Authorization': f'Bearer {token}'
    })

    if things_response.status_code == 200:
        things_data = things_response.json()
        return things_data

def getThingUsage(thingId):
    thing_response = requests.get(thing_url + thingId, headers={
        'Accept': 'application/json',
        'Authorization': f'Bearer {token}'
    })
    thing_data = thing_response.json()
    return thing_data.get("ActualUsage")

def updateData():
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    metadata = MetaData()
    usages = Table(DB_TABLE_NAME, metadata,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('ts', DateTime),
        Column('thing', String(200)),
        Column('data', Float)
    )

    metadata.create_all(engine)

    things = getThings()
    data = []
    now = datetime.now()
    for thing in things:
        usage = getThingUsage(thing.get("ThingId"))
        data.append({
            'ThingName': thing.get("ThingName"),
            'DataUsage': usage["Data_"] / (1024 ** 3),
            'Timestamp': now,
        })
        print(f'Data usage for: {thing.get("ThingName")} -> {usage["Data_"]}')

    try:
        for thing in data:
            thing_name = thing['ThingName']
            use = thing['DataUsage']
            time = thing['Timestamp']

            print(f'Inserting data: Time={time}, ThingName={thing_name}, DataUsage={use}')
            session.execute(
                sa_text(f'INSERT INTO {DB_TABLE_NAME} (ts, thing, data) VALUES (:time, :thingname, :datause);'),
                {'time': time, 'thingname': thing_name, 'datause': use}
            )
        session.commit()
    except Exception as e:
        print(f"Error occurred: {e}")
        session.rollback()
    finally:
        session.close()


while True:
    updateData()
    print("Waiting 1 hour....")
    time.sleep(3600)