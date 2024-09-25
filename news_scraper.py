import requests
import csv
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

# .env-Datei laden
load_dotenv(dotenv_path="hier pfad zur .env-Datei eintragen")

# API Key aus Umgebungsvariablen laden
API_KEY = os.getenv("NEWS_API_KEY")

# Debug-Ausgabe des API Keys
print(f"Geladener API-Schlüssel: {API_KEY}")

# Keywords für die Suche
keywords = "Israel Palästina Gaza"

# Datum der letzten 7 Tage berechnen
end_date = datetime.now()
start_date = end_date - timedelta(days=7)

# Datum in passendes Format umwandeln
start_date_str = start_date.strftime("%Y-%m-%d")
end_date_str = end_date.strftime("%Y-%m-%d")

# Endpunkt der News API
url = f"https://newsapi.org/v2/everything?q={keywords}&from={start_date_str}&to={end_date_str}&sortBy=publishedAt&apiKey={API_KEY}"

# Anfrage an die API
response = requests.get(url)

# Überprüfen ob die Anfrage erfolgreich war
if response.status_code == 200:
    # Daten extrahieren
    data = response.json()
    
    # Nachrichten extrahieren
    articles = data.get("articles", [])

    # CSV-Datei öffnen (oder erstellen) und Nachrichten speichern
    with open("israel_diese_woche.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
    
        #Kopfzeile der CSV-Datei
        writer.writerow(["Title", "Description", "URL", "Published At"])

        # Schleife über alle Nachrichten
        for article in articles:
            title = article.get("title", "Keine Überschrift verfügbar")
            description = article.get("description", "Keine Beschreibung verfügbar")
            news_url = article.get("url", "Keine URL verfügbar")
            published_at = article.get("publishedAt", "Kein Veröffentlichungsdatum verfügbar")
            writer.writerow([title, description, news_url, published_at])

    print("Nachrichten erfolgreich in CSV-Datei gespeichert.")
else:
    print(f"Fehler bei der API-Anfrage: {response.status_code}")