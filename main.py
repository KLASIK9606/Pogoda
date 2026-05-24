import requests
import pandas as pd
import sqlite3
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

if not API_KEY:
    print("BŁĄD: Brak klucza API w pliku .env")
    exit(1)


CITIES = ["Gdansk", "Warszawa", "Krakow", "Wroclaw", "Poznan"]
all_weather_data = []


for city in CITIES:
    URL = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    
    try:
        response = requests.get(URL, timeout=10)
        data = response.json()

        if response.status_code == 200:
            weather_dict = {
                "miasto": data["name"],
                "temperatura_celsius": data["main"]["temp"],
                "wilgotnosc_procent": data["main"]["humidity"],
                "opis": data["weather"][0]["description"],
                "data_pobrania": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
          
            all_weather_data.append(weather_dict)
            print(f"✓ Złowiono: {city}")
            
        else:
            print(f"BŁĄD dla {city}: Status {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"BŁĄD sieci dla {city}: {e}")


if all_weather_data:
    df = pd.DataFrame(all_weather_data)
    conn = sqlite3.connect('weather_data.db')
    df.to_sql('historia_pogody', conn, if_exists='append', index=False)
    conn.close()
    print("\nSUKCES: Wszystkie miasta zapisane do bazy danych!")
else:
    print("\nBŁĄD: Nie pobrano żadnych danych, baza nietknięta.")