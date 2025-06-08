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
    # Elektronika - Laptopy
    {"id": "LAPTOP001", "nazwa": "MacBook Pro 14", "cena": 8999.99, "kategoria": "elektronika", "marka": "Apple"},
    {"id": "LAPTOP002", "nazwa": "Dell XPS 13", "cena": 4999.99, "kategoria": "elektronika", "marka": "Dell"},
    {"id": "LAPTOP003", "nazwa": "MacBook Air M2", "cena": 5999.99, "kategoria": "elektronika", "marka": "Apple"},
    {"id": "LAPTOP004", "nazwa": "HP Spectre x360", "cena": 6499.99, "kategoria": "elektronika", "marka": "HP"},
    {"id": "LAPTOP005", "nazwa": "Lenovo ThinkPad X1", "cena": 7999.99, "kategoria": "elektronika", "marka": "Lenovo"},
    {"id": "LAPTOP006", "nazwa": "ASUS ZenBook 14", "cena": 3999.99, "kategoria": "elektronika", "marka": "ASUS"},
    {"id": "LAPTOP007", "nazwa": "Microsoft Surface Laptop", "cena": 5499.99, "kategoria": "elektronika", "marka": "Microsoft"},
    {"id": "LAPTOP008", "nazwa": "Acer Swift 3", "cena": 2999.99, "kategoria": "elektronika", "marka": "Acer"},
    {"id": "LAPTOP009", "nazwa": "Gaming Laptop MSI", "cena": 9999.99, "kategoria": "elektronika", "marka": "MSI"},
    {"id": "LAPTOP010", "nazwa": "Razer Blade 15", "cena": 12999.99, "kategoria": "elektronika", "marka": "Razer"},
    {"id": "LAPTOP011", "nazwa": "HP Pavilion 15", "cena": 2799.99, "kategoria": "elektronika", "marka": "HP"},
    {"id": "LAPTOP012", "nazwa": "Lenovo IdeaPad 5", "cena": 3299.99, "kategoria": "elektronika", "marka": "Lenovo"},
    {"id": "LAPTOP013", "nazwa": "ASUS ROG Strix", "cena": 8999.99, "kategoria": "elektronika", "marka": "ASUS"},
    {"id": "LAPTOP014", "nazwa": "Dell Inspiron 15", "cena": 2999.99, "kategoria": "elektronika", "marka": "Dell"},
    {"id": "LAPTOP015", "nazwa": "MacBook Pro 16", "cena": 11999.99, "kategoria": "elektronika", "marka": "Apple"},

    # Telefony
    {"id": "PHONE001", "nazwa": "iPhone 15 Pro", "cena": 5499.99, "kategoria": "telefony", "marka": "Apple"},
    {"id": "PHONE002", "nazwa": "Samsung Galaxy S24", "cena": 3999.99, "kategoria": "telefony", "marka": "Samsung"},
    {"id": "PHONE003", "nazwa": "Google Pixel 8", "cena": 3299.99, "kategoria": "telefony", "marka": "Google"},
    {"id": "PHONE004", "nazwa": "iPhone 14", "cena": 4299.99, "kategoria": "telefony", "marka": "Apple"},
    {"id": "PHONE005", "nazwa": "OnePlus 12", "cena": 3599.99, "kategoria": "telefony", "marka": "OnePlus"},
    {"id": "PHONE006", "nazwa": "Xiaomi 14 Pro", "cena": 2999.99, "kategoria": "telefony", "marka": "Xiaomi"},
    {"id": "PHONE007", "nazwa": "Sony Xperia 1 V", "cena": 4999.99, "kategoria": "telefony", "marka": "Sony"},
    {"id": "PHONE008", "nazwa": "Huawei P60 Pro", "cena": 3799.99, "kategoria": "telefony", "marka": "Huawei"},
    {"id": "PHONE009", "nazwa": "Nothing Phone 2", "cena": 2799.99, "kategoria": "telefony", "marka": "Nothing"},
    {"id": "PHONE010", "nazwa": "Motorola Edge 40", "cena": 2199.99, "kategoria": "telefony", "marka": "Motorola"},
    {"id": "PHONE011", "nazwa": "iPhone 13", "cena": 3599.99, "kategoria": "telefony", "marka": "Apple"},
    {"id": "PHONE012", "nazwa": "Samsung Galaxy A54", "cena": 1899.99, "kategoria": "telefony", "marka": "Samsung"},
    {"id": "PHONE013", "nazwa": "Realme GT 5", "cena": 2299.99, "kategoria": "telefony", "marka": "Realme"},
    {"id": "PHONE014", "nazwa": "Oppo Find X6", "cena": 3499.99, "kategoria": "telefony", "marka": "Oppo"},
    {"id": "PHONE015", "nazwa": "Vivo X90", "cena": 2999.99, "kategoria": "telefony", "marka": "Vivo"},

    # Tablety
    {"id": "TABLET001", "nazwa": "iPad Pro 12.9", "cena": 4999.99, "kategoria": "tablety", "marka": "Apple"},
    {"id": "TABLET002", "nazwa": "Samsung Galaxy Tab S9", "cena": 3599.99, "kategoria": "tablety", "marka": "Samsung"},
    {"id": "TABLET003", "nazwa": "iPad Air", "cena": 2999.99, "kategoria": "tablety", "marka": "Apple"},
    {"id": "TABLET004", "nazwa": "Microsoft Surface Pro", "cena": 4299.99, "kategoria": "tablety", "marka": "Microsoft"},
    {"id": "TABLET005", "nazwa": "Lenovo Tab P11", "cena": 1299.99, "kategoria": "tablety", "marka": "Lenovo"},
    {"id": "TABLET006", "nazwa": "iPad 10.9", "cena": 1999.99, "kategoria": "tablety", "marka": "Apple"},
    {"id": "TABLET007", "nazwa": "Samsung Galaxy Tab A8", "cena": 999.99, "kategoria": "tablety", "marka": "Samsung"},
    {"id": "TABLET008", "nazwa": "Huawei MatePad Pro", "cena": 2799.99, "kategoria": "tablety", "marka": "Huawei"},

    # Audio
    {"id": "AUDIO001", "nazwa": "AirPods Pro", "cena": 1299.99, "kategoria": "audio", "marka": "Apple"},
    {"id": "AUDIO002", "nazwa": "Sony WH-1000XM5", "cena": 1599.99, "kategoria": "audio", "marka": "Sony"},
    {"id": "AUDIO003", "nazwa": "Bose QuietComfort", "cena": 1799.99, "kategoria": "audio", "marka": "Bose"},
    {"id": "AUDIO004", "nazwa": "Sennheiser Momentum 4", "cena": 1999.99, "kategoria": "audio", "marka": "Sennheiser"},
    {"id": "AUDIO005", "nazwa": "JBL Charge 5", "cena": 699.99, "kategoria": "audio", "marka": "JBL"},
    {"id": "AUDIO006", "nazwa": "Marshall Acton III", "cena": 1199.99, "kategoria": "audio", "marka": "Marshall"},
    {"id": "AUDIO007", "nazwa": "Beats Studio Buds", "cena": 799.99, "kategoria": "audio", "marka": "Beats"},
    {"id": "AUDIO008", "nazwa": "Audio-Technica ATH-M50x", "cena": 899.99, "kategoria": "audio", "marka": "Audio-Technica"},
    {"id": "AUDIO009", "nazwa": "AirPods 3", "cena": 899.99, "kategoria": "audio", "marka": "Apple"},
    {"id": "AUDIO010", "nazwa": "Sony WF-1000XM4", "cena": 1299.99, "kategoria": "audio", "marka": "Sony"},
    {"id": "AUDIO011", "nazwa": "JBL Flip 6", "cena": 499.99, "kategoria": "audio", "marka": "JBL"},
    {"id": "AUDIO012", "nazwa": "Bose SoundLink", "cena": 699.99, "kategoria": "audio", "marka": "Bose"},

    # Gaming
    {"id": "GAMING001", "nazwa": "PlayStation 5", "cena": 2499.99, "kategoria": "gaming", "marka": "Sony"},
    {"id": "GAMING002", "nazwa": "Xbox Series X", "cena": 2399.99, "kategoria": "gaming", "marka": "Microsoft"},
    {"id": "GAMING003", "nazwa": "Nintendo Switch OLED", "cena": 1599.99, "kategoria": "gaming", "marka": "Nintendo"},
    {"id": "GAMING004", "nazwa": "Steam Deck", "cena": 2199.99, "kategoria": "gaming", "marka": "Valve"},
    {"id": "GAMING005", "nazwa": "PlayStation 5 Digital", "cena": 1999.99, "kategoria": "gaming", "marka": "Sony"},
    {"id": "GAMING006", "nazwa": "Xbox Series S", "cena": 1399.99, "kategoria": "gaming", "marka": "Microsoft"},
    {"id": "GAMING007", "nazwa": "Nintendo Switch Lite", "cena": 899.99, "kategoria": "gaming", "marka": "Nintendo"},
    {"id": "GAMING008", "nazwa": "Meta Quest 3", "cena": 2299.99, "kategoria": "gaming", "marka": "Meta"},
    {"id": "GAMING009", "nazwa": "PICO 4", "cena": 1899.99, "kategoria": "gaming", "marka": "ByteDance"},

    # TV
    {"id": "TV001", "nazwa": "Samsung QLED 55", "cena": 4999.99, "kategoria": "tv", "marka": "Samsung"},
    {"id": "TV002", "nazwa": "LG OLED 65", "cena": 7999.99, "kategoria": "tv", "marka": "LG"},
    {"id": "TV003", "nazwa": "Sony Bravia XR 55", "cena": 5999.99, "kategoria": "tv", "marka": "Sony"},
    {"id": "TV004", "nazwa": "TCL QLED 43", "cena": 2199.99, "kategoria": "tv", "marka": "TCL"},
    {"id": "TV005", "nazwa": "Philips Ambilight 50", "cena": 3299.99, "kategoria": "tv", "marka": "Philips"},
    {"id": "TV006", "nazwa": "Samsung Neo QLED 75", "cena": 12999.99, "kategoria": "tv", "marka": "Samsung"},
    {"id": "TV007", "nazwa": "LG NanoCell 55", "cena": 3599.99, "kategoria": "tv", "marka": "LG"},
    {"id": "TV008", "nazwa": "Hisense ULED 65", "cena": 4299.99, "kategoria": "tv", "marka": "Hisense"},
    {"id": "TV009", "nazwa": "Sharp Aquos 43", "cena": 1999.99, "kategoria": "tv", "marka": "Sharp"},

    # Akcesoria elektroniczne
    {"id": "ACC001", "nazwa": "Magic Mouse", "cena": 399.99, "kategoria": "elektronika", "marka": "Apple"},
    {"id": "ACC002", "nazwa": "Logitech MX Master 3", "cena": 459.99, "kategoria": "elektronika", "marka": "Logitech"},
    {"id": "ACC003", "nazwa": "Keychron K3", "cena": 599.99, "kategoria": "elektronika", "marka": "Keychron"},
    {"id": "ACC004", "nazwa": "Dell Monitor 27", "cena": 1299.99, "kategoria": "elektronika", "marka": "Dell"},
    {"id": "ACC005", "nazwa": "USB-C Hub", "cena": 299.99, "kategoria": "elektronika", "marka": "Anker"},
    {"id": "ACC006", "nazwa": "Webcam Logitech C920", "cena": 399.99, "kategoria": "elektronika", "marka": "Logitech"},
    {"id": "ACC007", "nazwa": "Mikrofon Blue Yeti", "cena": 899.99, "kategoria": "elektronika", "marka": "Blue"},
    {"id": "ACC008", "nazwa": "Samsung Monitor 32", "cena": 1899.99, "kategoria": "elektronika", "marka": "Samsung"},
    {"id": "ACC009", "nazwa": "Razer DeathAdder V3", "cena": 349.99, "kategoria": "elektronika", "marka": "Razer"},
    {"id": "ACC010", "nazwa": "Corsair K95 RGB", "cena": 799.99, "kategoria": "elektronika", "marka": "Corsair"},

    # Smart Home
    {"id": "SMART001", "nazwa": "Amazon Echo Dot", "cena": 249.99, "kategoria": "elektronika", "marka": "Amazon"},
    {"id": "SMART002", "nazwa": "Google Nest Hub", "cena": 599.99, "kategoria": "elektronika", "marka": "Google"},
    {"id": "SMART003", "nazwa": "Philips Hue Starter Kit", "cena": 799.99, "kategoria": "elektronika", "marka": "Philips"},
    {"id": "SMART004", "nazwa": "Ring Video Doorbell", "cena": 699.99, "kategoria": "elektronika", "marka": "Ring"},
    {"id": "SMART005", "nazwa": "TP-Link Tapo C200", "cena": 149.99, "kategoria": "elektronika", "marka": "TP-Link"},
    {"id": "SMART006", "nazwa": "Xiaomi Mi Smart Band 8", "cena": 199.99, "kategoria": "elektronika", "marka": "Xiaomi"},

    # AGD
    {"id": "AGD001", "nazwa": "Dyson V15 Detect", "cena": 2999.99, "kategoria": "agd", "marka": "Dyson"},
    {"id": "AGD002", "nazwa": "Roomba i7+", "cena": 3999.99, "kategoria": "agd", "marka": "iRobot"},
    {"id": "AGD003", "nazwa": "Philips Airfryer XXL", "cena": 1299.99, "kategoria": "agd", "marka": "Philips"},
    {"id": "AGD004", "nazwa": "Bosch Serie 8 Pralka", "cena": 3599.99, "kategoria": "agd", "marka": "Bosch"},
    {"id": "AGD005", "nazwa": "Whirlpool Lodówka", "cena": 4999.99, "kategoria": "agd", "marka": "Whirlpool"},
    {"id": "AGD006", "nazwa": "Electrolux Zmywarka", "cena": 2799.99, "kategoria": "agd", "marka": "Electrolux"},

    # Fitness
    {"id": "FIT001", "nazwa": "Apple Watch Ultra", "cena": 3799.99, "kategoria": "fitness", "marka": "Apple"},
    {"id": "FIT002", "nazwa": "Garmin Forerunner 955", "cena": 2499.99, "kategoria": "fitness", "marka": "Garmin"},
    {"id": "FIT003", "nazwa": "Fitbit Charge 5", "cena": 899.99, "kategoria": "fitness", "marka": "Fitbit"},
    {"id": "FIT004", "nazwa": "Polar Vantage V3", "cena": 2299.99, "kategoria": "fitness", "marka": "Polar"},
    {"id": "FIT005", "nazwa": "Samsung Galaxy Watch 6", "cena": 1599.99, "kategoria": "fitness", "marka": "Samsung"},

    # Foto
    {"id": "FOTO001", "nazwa": "Canon EOS R5", "cena": 15999.99, "kategoria": "foto", "marka": "Canon"},
    {"id": "FOTO002", "nazwa": "Sony A7 IV", "cena": 12999.99, "kategoria": "foto", "marka": "Sony"},
    {"id": "FOTO003", "nazwa": "Nikon Z6 II", "cena": 9999.99, "kategoria": "foto", "marka": "Nikon"},
    {"id": "FOTO004", "nazwa": "Fujifilm X-T5", "cena": 8999.99, "kategoria": "foto", "marka": "Fujifilm"},
    {"id": "FOTO005", "nazwa": "DJI Mini 3 Pro", "cena": 3999.99, "kategoria": "foto", "marka": "DJI"},
    {"id": "FOTO006", "nazwa": "GoPro Hero 12", "cena": 2199.99, "kategoria": "foto", "marka": "GoPro"},
    {"id": "FOTO007", "nazwa": "Insta360 X3", "cena": 1999.99, "kategoria": "foto", "marka": "Insta360"}
]

# Rozszerzone lokalizacje sklepów - więcej miast w Polsce
LOKALIZACJE_SKLEPOW = [
    {"miasto": "Warszawa", "lat": 52.2297, "lon": 21.0122, "kod": "WAW"},
    {"miasto": "Kraków", "lat": 50.0647, "lon": 19.9450, "kod": "KRK"},
    {"miasto": "Gdańsk", "lat": 54.3520, "lon": 18.6466, "kod": "GDA"},
    {"miasto": "Wrocław", "lat": 51.1079, "lon": 17.0385, "kod": "WRO"},
    {"miasto": "Poznań", "lat": 52.4064, "lon": 16.9252, "kod": "POZ"},
    {"miasto": "Łódź", "lat": 51.7592, "lon": 19.4560, "kod": "LOD"},
    {"miasto": "Katowice", "lat": 50.2649, "lon": 19.0238, "kod": "KAT"},
    {"miasto": "Szczecin", "lat": 53.4285, "lon": 14.5528, "kod": "SZC"},
    {"miasto": "Bydgoszcz", "lat": 53.1235, "lon": 18.0084, "kod": "BYD"},
    {"miasto": "Lublin", "lat": 51.2465, "lon": 22.5684, "kod": "LUB"},
    {"miasto": "Białystok", "lat": 53.1325, "lon": 23.1688, "kod": "BIA"},
    {"miasto": "Gdynia", "lat": 54.5189, "lon": 18.5305, "kod": "GDY"},
    {"miasto": "Częstochowa", "lat": 50.7971, "lon": 19.1200, "kod": "CZE"},
    {"miasto": "Radom", "lat": 51.4027, "lon": 21.1471, "kod": "RAD"},
    {"miasto": "Sosnowiec", "lat": 50.2862, "lon": 19.1040, "kod": "SOS"},
    {"miasto": "Toruń", "lat": 53.0138, "lon": 18.5984, "kod": "TOR"},
    {"miasto": "Kielce", "lat": 50.8661, "lon": 20.6286, "kod": "KIE"},
    {"miasto": "Gliwice", "lat": 50.2945, "lon": 18.6714, "kod": "GLI"},
    {"miasto": "Zabrze", "lat": 50.3249, "lon": 18.7856, "kod": "ZAB"},
    {"miasto": "Olsztyn", "lat": 53.7784, "lon": 20.4801, "kod": "OLS"},
    {"miasto": "Rzeszów", "lat": 50.0412, "lon": 21.9991, "kod": "RZE"},
    {"miasto": "Opole", "lat": 50.6751, "lon": 17.9213, "kod": "OPO"},
    {"miasto": "Zielona Góra", "lat": 51.9356, "lon": 15.5062, "kod": "ZGO"},
    {"miasto": "Płock", "lat": 52.5463, "lon": 19.7065, "kod": "PLO"},
    {"miasto": "Elbląg", "lat": 54.1522, "lon": 19.4044, "kod": "ELB"}
]

# Rozszerzone listy imion
IMIONA = [
    "Jan", "Anna", "Piotr", "Maria", "Tomasz", "Katarzyna", "Michał", "Agnieszka",
    "Krzysztof", "Magdalena", "Andrzej", "Barbara", "Józef", "Elżbieta", "Stanisław",
    "Teresa", "Marek", "Małgorzata", "Jerzy", "Joanna", "Wojciech", "Ewa", "Adam",
    "Beata", "Paweł", "Danuta", "Marcin", "Monika", "Łukasz", "Renata", "Jakub",
    "Dorota", "Robert", "Iwona", "Dariusz", "Halina", "Mariusz", "Grażyna", "Grzegorz",
    "Bożena", "Sebastian", "Urszula", "Damian", "Aleksandra", "Bartosz", "Paulina",
    "Kamil", "Natalia", "Rafał", "Karolina", "Mateusz", "Sylwia", "Artur", "Aneta",
    "Maciej", "Jolanta", "Daniel", "Agata", "Dawid", "Justyna", "Szymon", "Patrycja",
    "Filip", "Weronika", "Hubert", "Zofia", "Adrian", "Julia", "Dominik", "Martyna",
    "Patryk", "Kinga", "Igor", "Klaudia", "Wiktor", "Marta", "Oskar", "Oliwia"
]

NAZWISKA = [
    "Kowalski", "Nowak", "Wiśniewski", "Dąbrowski", "Lewandowski", "Wójcik",
    "Kamiński", "Kowalczyk", "Zieliński", "Szymański", "Woźniak", "Kozłowski",
    "Jankowski", "Mazur", "Kwiatkowski", "Krawczyk", "Kaczmarek", "Piotrowski",
    "Grabowski", "Nowakowski", "Pawłowski", "Michalski", "Nowicki", "Adamczyk",
    "Dudek", "Zając", "Wieczorek", "Jabłoński", "Król", "Majewski", "Olszewski",
    "Jaworski", "Wróbel", "Malinowski", "Pawlak", "Witkowski", "Walczak",
    "Stępień", "Górski", "Rutkowski", "Michalak", "Sikora", "Ostrowski",
    "Baran", "Duda", "Szewczyk", "Tomaszewski", "Pietrzak", "Marciniak",
    "Sadowski", "Włodarczyk", "Czerwiński", "Laskowski", "Ziółkowski", "Przybylski",
    "Zakrzewski", "Krajewski", "Sokołowski", "Sawicki", "Lis", "Kalinowski",
    "Kołodziej", "Gajewski", "Kubiak", "Sobczak", "Wysocki", "Maciejewski"
]

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
        ip_ranges = ["192.168.1", "10.0.0", "172.16.0", "203.0.113", "198.51.100",
                     "192.0.2", "198.18.0", "203.0.113"]
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
    if liczba > 10000:
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