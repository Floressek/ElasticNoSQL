from flask import Flask, request, jsonify
import json
import random
from datetime import datetime, timedelta
import requests
import threading
import time

app = Flask(__name__)

# Prawdziwe dane produktów
PRODUKTY = [
    {"id": "LAPTOP001", "nazwa": "MacBook Pro 14", "cena": 8999.99, "kategoria": "elektronika", "marka": "Apple"},
    {"id": "LAPTOP002", "nazwa": "Dell XPS 13", "cena": 4999.99, "kategoria": "elektronika", "marka": "Dell"},
    {"id": "PHONE001", "nazwa": "iPhone 15 Pro", "cena": 5499.99, "kategoria": "telefony", "marka": "Apple"},
    {"id": "PHONE002", "nazwa": "Samsung Galaxy S24", "cena": 3999.99, "kategoria": "telefony", "marka": "Samsung"},
    {"id": "PHONE003", "nazwa": "Google Pixel 8", "cena": 3299.99, "kategoria": "telefony", "marka": "Google"},
    {"id": "TABLET001", "nazwa": "iPad Pro 12.9", "cena": 4999.99, "kategoria": "tablety", "marka": "Apple"},
    {"id": "TABLET002", "nazwa": "Samsung Galaxy Tab S9", "cena": 3599.99, "kategoria": "tablety", "marka": "Samsung"},
    {"id": "AUDIO001", "nazwa": "AirPods Pro", "cena": 1299.99, "kategoria": "audio", "marka": "Apple"},
    {"id": "AUDIO002", "nazwa": "Sony WH-1000XM5", "cena": 1599.99, "kategoria": "audio", "marka": "Sony"},
    {"id": "AUDIO003", "nazwa": "Bose QuietComfort", "cena": 1799.99, "kategoria": "audio", "marka": "Bose"},
    {"id": "GAMING001", "nazwa": "PlayStation 5", "cena": 2499.99, "kategoria": "gaming", "marka": "Sony"},
    {"id": "GAMING002", "nazwa": "Xbox Series X", "cena": 2399.99, "kategoria": "gaming", "marka": "Microsoft"},
    {"id": "GAMING003", "nazwa": "Nintendo Switch OLED", "cena": 1599.99, "kategoria": "gaming", "marka": "Nintendo"},
    {"id": "TV001", "nazwa": "Samsung QLED 55", "cena": 4999.99, "kategoria": "tv", "marka": "Samsung"},
    {"id": "TV002", "nazwa": "LG OLED 65", "cena": 7999.99, "kategoria": "tv", "marka": "LG"},
]

# Prawdziwe lokalizacje sklepów w Polsce
LOKALIZACJE_SKLEPOW = [
    {"miasto": "Warszawa", "lat": 52.2297, "lon": 21.0122, "kod": "WAW"},
    {"miasto": "Kraków", "lat": 50.0647, "lon": 19.9450, "kod": "KRK"},
    {"miasto": "Gdańsk", "lat": 54.3520, "lon": 18.6466, "kod": "GDA"},
    {"miasto": "Wrocław", "lat": 51.1079, "lon": 17.0385, "kod": "WRO"},
    {"miasto": "Poznań", "lat": 52.4064, "lon": 16.9252, "kod": "POZ"},
    {"miasto": "Łódź", "lat": 51.7592, "lon": 19.4560, "kod": "LOD"},
    {"miasto": "Katowice", "lat": 50.2649, "lon": 19.0238, "kod": "KAT"},
]

# Imiona klientów
IMIONA = ["Jan", "Anna", "Piotr", "Maria", "Tomasz", "Katarzyna", "Michał", "Agnieszka", "Krzysztof", "Magdalena",
          "Andrzej", "Barbara", "Józef", "Elżbieta", "Stanisław", "Teresa", "Marek", "Małgorzata", "Jerzy", "Joanna"]

NAZWISKA = ["Kowalski", "Nowak", "Wiśniewski", "Dąbrowski", "Lewandowski", "Wójcik", "Kamiński", "Kowalczyk",
            "Zieliński", "Szymański", "Woźniak", "Kozłowski", "Jankowski", "Mazur", "Kwiatkowski"]

def generuj_transakcje_sprzedazy(liczba=1):
    """Generuje prawdziwe transakcje sprzedaży"""
    transakcje = []

    for _ in range(liczba):
        # Losowy produkt
        produkt = random.choice(PRODUKTY)

        # Losowa lokalizacja
        sklep = random.choice(LOKALIZACJE_SKLEPOW)

        # Losowy klient
        imie = random.choice(IMIONA)
        nazwisko = random.choice(NAZWISKA)

        # Losowa ilość (1-3 sztuki)
        ilosc = random.randint(1, 3)

        # Oblicz wartość
        wartosc_brutto = produkt["cena"] * ilosc

        # Losowy rabat (0-20%)
        rabat_procent = random.choice([0, 0, 0, 5, 10, 15, 20])  # częściej brak rabatu
        rabat_kwota = wartosc_brutto * (rabat_procent / 100)
        wartosc_netto = wartosc_brutto - rabat_kwota

        # Sposób płatności
        platnosc = random.choice(["karta", "karta", "karta", "gotówka", "BLIK", "przelew"])

        # Czas transakcji (ostatnie 30 dni)
        czas = datetime.now() - timedelta(
            days=random.randint(0, 30),
            hours=random.randint(9, 22),  # godziny otwarcia sklepu
            minutes=random.randint(0, 59)
        )

        # ID transakcji
        transaction_id = f"TXN_{czas.strftime('%Y%m%d')}_{random.randint(10000, 99999)}"

        # IP klienta (symulowane)
        ip_ranges = ["192.168.1", "10.0.0", "172.16.0", "203.0.113"]
        ip = f"{random.choice(ip_ranges)}.{random.randint(1, 254)}"

        transakcja = {
            "timestamp": czas.isoformat(),
            "transaction_id": transaction_id,
            "level": "INFO",
            "service": "sklep-pos",
            "action": "sprzedaz",
            "message": f"Sprzedaż produktu {produkt['nazwa']}",

            # Dane produktu
            "product_id": produkt["id"],
            "product_name": produkt["nazwa"],
            "product_category": produkt["kategoria"],
            "product_brand": produkt["marka"],
            "unit_price": produkt["cena"],
            "quantity": ilosc,

            # Finansowe
            "amount_gross": round(wartosc_brutto, 2),
            "discount_percent": rabat_procent,
            "discount_amount": round(rabat_kwota, 2),
            "amount_net": round(wartosc_netto, 2),
            "currency": "PLN",
            "payment_method": platnosc,

            # Lokalizacja
            "store_city": sklep["miasto"],
            "store_code": sklep["kod"],
            "store_location": {
                "lat": sklep["lat"],
                "lon": sklep["lon"]
            },

            # Klient
            "customer_name": f"{imie} {nazwisko}",
            "customer_ip": ip,

            # Metadata
            "session_id": f"sess_{random.randint(100000, 999999)}",
            "employee_id": f"EMP{random.randint(1001, 1050)}",
            "receipt_number": f"RC_{czas.strftime('%Y%m%d')}_{random.randint(1000, 9999)}"
        }

        transakcje.append(transakcja)

    return transakcje

@app.route('/')
def home():
    return jsonify({
        "status": "running",
        "service": "Sklep Internetowy - Generator Sprzedaży",
        "endpoints": {
            "/generate/<liczba>": "Generuje N transakcji sprzedaży",
            "/auto-generate/<liczba>": "Automatycznie generuje N transakcji co 5 sekund",
            "/stats": "Statystyki produktów",
            "/health": "Status serwera"
        },
        "logstash_endpoint": "http://logstash:8080"
    })

@app.route('/generate/<int:liczba>')
def generuj_sprzedaz(liczba):
    """Endpoint do generowania transakcji sprzedaży"""
    if liczba > 100:
        return jsonify({"error": "Maksymalnie 100 transakcji na raz"}), 400

    transakcje = generuj_transakcje_sprzedazy(liczba)

    # Wyślij do Logstash (opcjonalnie)
    try:
        for transakcja in transakcje:
            # Wysłanie do Logstash przez HTTP
            response = requests.post(
                'http://logstash:8080',  # Logstash HTTP input
                json=transakcja,
                timeout=5
            )
    except:
        pass  # Nie blokuj jeśli Logstash nie działa

    return jsonify({
        "status": "success",
        "generated_transactions": len(transakcje),
        "sample_transaction": transakcje[0] if transakcje else None,
        "logstash_sent": True
    })

@app.route('/auto-generate/<int:liczba>')
def auto_generuj(liczba):
    """Automatycznie generuje transakcje co 5 sekund"""

    def generate_loop():
        for i in range(liczba):
            transakcje = generuj_transakcje_sprzedazy(1)
            print(f"[{datetime.now()}] Wygenerowano transakcję {i+1}/{liczba}: {transakcje[0]['transaction_id']}")

            # Wyślij do Elasticsearch bezpośrednio
            try:
                requests.post(
                    'http://localhost:9200/sprzedaz/_doc',
                    json=transakcje[0],
                    headers={'Content-Type': 'application/json'}
                )
            except:
                pass

            time.sleep(5)  # Co 5 sekund

    # Uruchom w tle
    thread = threading.Thread(target=generate_loop)
    thread.daemon = True
    thread.start()

    return jsonify({
        "status": "started",
        "message": f"Generowanie {liczba} transakcji co 5 sekund rozpoczęte",
        "estimated_time": f"{liczba * 5} sekund"
    })

@app.route('/stats')
def statystyki():
    """Statystyki produktów"""
    kategorie = {}
    marki = {}

    for produkt in PRODUKTY:
        kat = produkt["kategoria"]
        marka = produkt["marka"]

        if kat not in kategorie:
            kategorie[kat] = {"count": 0, "avg_price": 0, "products": []}
        if marka not in marki:
            marki[marka] = {"count": 0, "avg_price": 0}

        kategorie[kat]["count"] += 1
        kategorie[kat]["products"].append(produkt["nazwa"])
        marki[marka]["count"] += 1

    # Oblicz średnie ceny
    for kat in kategorie:
        ceny = [p["cena"] for p in PRODUKTY if p["kategoria"] == kat]
        kategorie[kat]["avg_price"] = round(sum(ceny) / len(ceny), 2)

    for marka in marki:
        ceny = [p["cena"] for p in PRODUKTY if p["marka"] == marka]
        marki[marka]["avg_price"] = round(sum(ceny) / len(ceny), 2)

    return jsonify({
        "total_products": len(PRODUKTY),
        "categories": kategorie,
        "brands": marki,
        "stores": len(LOKALIZACJE_SKLEPOW),
        "store_locations": [f"{s['miasto']} ({s['kod']})" for s in LOKALIZACJE_SKLEPOW]
    })

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "uptime": "OK"
    })

if __name__ == '__main__':
    print("🏪 Sklep Internetowy - Generator Sprzedaży")
    print("📊 Dostępne endpointy:")
    print("   http://localhost:5000/generate/10    - Generuje 10 transakcji")
    print("   http://localhost:5000/auto-generate/20 - Auto-generuje 20 transakcji co 5s")
    print("   http://localhost:5000/stats          - Statystyki produktów")
    print("")

    app.run(host='0.0.0.0', port=5000, debug=True)