import requests
import sqlite3
import time
from datetime import datetime

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS flights (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    icao24 TEXT,
    callsign TEXT,
    latitude REAL,
    longitude REAL,
    altitude REAL
)
""")

LAMIN = 2.0
LAMAX = 7.0
LOMIN = 99.0
LOMAX = 104.0

def fetch_data():
    url = f"https://opensky-network.org/api/states/all?lamin={LAMIN}&lomin={LOMIN}&lamax={LAMAX}&lomax={LOMAX}"
    
    try:
        response = requests.get(url, timeout=30)

        if response.status_code == 200:
            data = response.json()

            if data["states"]:
                for flight in data["states"]:
                    icao24 = flight[0]
                    callsign = flight[1]
                    longitude = flight[5]
                    latitude = flight[6]
                    altitude = flight[7]

                    if latitude is not None and longitude is not None:
                        cursor.execute("""
                            INSERT INTO flights (timestamp, icao24, callsign, latitude, longitude, altitude)
                            VALUES (?, ?, ?, ?, ?, ?)
                        """, (
                            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            icao24,
                            callsign.strip() if callsign else None,
                            latitude,
                            longitude,
                            altitude
                        ))

                conn.commit()
                print("Data saved at", datetime.now())
            else:
                print("No flights found at", datetime.now())
        else:
            print("API error:", response.status_code)

    except Exception as e:
        print("Error:", e)

while True:
    fetch_data()
    time.sleep(300)