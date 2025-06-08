# 🏪 ELK Stack - System Analityki Sprzedaży

Kompletny system do zbierania, przetwarzania i analizowania danych sprzedażowych w czasie rzeczywistym oparty na stosie ELK (Elasticsearch, Logstash, Kibana) z Flask API jako generatorem danych.

## 📋 Spis treści

- [Architektura systemu](#-architektura-systemu)
- [Funkcjonalności](#-funkcjonalności)
- [Wymagania](#-wymagania)
- [Instalacja i uruchomienie](#-instalacja-i-uruchomienie)
- [Konfiguracja](#-konfiguracja)
- [API Endpoints](#-api-endpoints)
- [Struktura danych](#-struktura-danych)
- [Monitorowanie](#-monitorowanie)
- [Rozwiązywanie problemów](#-rozwiązywanie-problemów)

## 🏗 Architektura systemu

```
┌─────────────┐    HTTP    ┌──────────────┐    ┌─────────────────┐    ┌─────────────┐
│ Flask API   │─────────────▶│  Logstash    │────▶│ Elasticsearch   │────▶│   Kibana    │
│ Generator   │    :8080    │  Pipeline    │     │    Cluster      │     │ Dashboards  │
│ Sprzedaży   │             │              │     │                 │     │             │
└─────────────┘             └──────────────┘     └─────────────────┘     └─────────────┘
     :5001                         :8080              :9200/:9300              :5601
```

### Komponenty:

- **🐍 Flask API** - Generator realistycznych transakcji sprzedażowych
- **📊 Logstash** - Przetwarzanie i wzbogacanie danych w czasie rzeczywistym
- **🔍 Elasticsearch** - Klaster 5 węzłów (3 master + 2 data) do przechowywania danych
- **📈 Kibana** - Interface do wizualizacji i analizy danych

## ✨ Funkcjonalności

### Generator danych (Flask API)
- **15 realistycznych produktów** - Apple, Samsung, Sony, Nintendo, itp.
- **7 lokalizacji sklepów** - Warszawa, Kraków, Gdańsk, Wrocław, Poznań, Łódź, Katowice
- **Różnorodne transakcje** - różne metody płatności, rabaty, klienci
- **Automatyczne generowanie** - możliwość ciągłego generowania danych

### Przetwarzanie danych (Logstash)
- **Klasyfikacja transakcji** - basic/standard/premium według wartości
- **Wzbogacanie geolokalizacyjne** - lokalizacja klientów na podstawie IP
- **Obliczanie marży** - automatyczne wyliczanie marży według kategorii produktu
- **System alertów** - powiadomienia dla transakcji powyżej 8000 PLN
- **Tagowanie kategorii** - automatyczne oznaczanie produktów high-value

### Analityka (Elasticsearch + Kibana)
- **Indeksowanie dzienne** - automatyczne tworzenie indeksów `sprzedaz-YYYY.MM.DD`
- **Indeksy alertów** - oddzielne przechowywanie wysokich transakcji
- **Struktura ECS** - zgodność z Elastic Common Schema
- **Dashboardy** - gotowe do tworzenia wizualizacji w Kibana

## 🔧 Wymagania

- **Docker** 20.10+
- **Docker Compose** 2.0+
- **8GB RAM** (rekomendowane dla Elasticsearch)
- **Porty:** 5001, 5601, 8080, 9200, 9300

## 🚀 Instalacja i uruchomienie

### 1. Klonowanie repozytorium
```bash
git clone <repository-url>
cd ElasticNoSQL
```

### 2. Uruchomienie systemu
```bash
# Uruchomienie wszystkich kontenerów
docker-compose up -d

# Sprawdzenie statusu
docker-compose ps
```

### 3. Weryfikacja uruchomienia
```bash
# Sprawdź czy Elasticsearch działa
curl http://localhost:9200/_cluster/health?pretty

# Sprawdź Flask API
curl http://localhost:5001/health

# Sprawdź Kibana (w przeglądarce)
http://localhost:5601
```

### 4. Generowanie pierwszych danych
```bash
# Wygeneruj 10 transakcji testowych
curl http://localhost:5001/generate/10

# Lub uruchom automatyczne generowanie (20 transakcji co 5 sekund)
curl http://localhost:5001/auto-generate/20
```

## ⚙️ Konfiguracja

### Zmienne środowiskowe

| Zmienna | Wartość domyślna | Opis |
|---------|------------------|------|
| `ELASTICSEARCH_HOST` | `es-data-1` | Host Elasticsearch |
| `LOGSTASH_HOST` | `logstash` | Host Logstash |
| `ES_JAVA_OPTS` | `-Xms1g -Xmx1g` | Ustawienia JVM dla ES |

### Konfiguracja Elasticsearch

```yaml
# docker-compose.yml
environment:
  - cluster.name=sklep-cluster
  - node.roles=master  # lub data,ingest
  - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
  - xpack.security.enabled=false
```

### Konfiguracja Logstash

Pipeline znajduje się w `logstash/pipeline/logstash.conf` i zawiera:
- Input HTTP na porcie 8080
- Filtry do wzbogacania danych
- Output do Elasticsearch

## 🔌 API Endpoints

### Flask API (port 5001)

| Endpoint | Metoda | Opis | Przykład |
|----------|--------|------|----------|
| `/` | GET | Strona główna z informacjami | `GET /` |
| `/health` | GET | Status zdrowia serwera | `GET /health` |
| `/generate/<liczba>` | GET | Generuje N transakcji | `GET /generate/10` |
| `/auto-generate/<liczba>` | GET | Auto-generowanie co 5s | `GET /auto-generate/20` |
| `/stats` | GET | Statystyki produktów | `GET /stats` |

### Przykłady użycia

```bash
# Podstawowe informacje
curl http://localhost:5001/

# Wygeneruj 5 transakcji
curl http://localhost:5001/generate/5

# Statystyki produktów i kategorii
curl http://localhost:5001/stats

# Auto-generowanie 50 transakcji (co 5 sekund)
curl http://localhost:5001/auto-generate/50
```

## 📊 Struktura danych

### Przykładowa transakcja

```json
{
  "timestamp": "2025-06-08T12:30:45.123456",
  "transaction_id": "TXN_20250608_12345",
  "level": "INFO",
  "service": "sklep-pos",
  "action": "sprzedaz",
  "message": "Sprzedaż produktu iPhone 15 Pro",
  
  "product_id": "PHONE001",
  "product_name": "iPhone 15 Pro",
  "product_category": "telefony",
  "product_brand": "Apple",
  "unit_price": 5499.99,
  "quantity": 1,
  
  "amount_gross": 5499.99,
  "discount_percent": 10,
  "discount_amount": 549.99,
  "amount_net": 4950.00,
  "currency": "PLN",
  "payment_method": "karta",
  
  "store_city": "Warszawa",
  "store_code": "WAW",
  "store_location": {
    "lat": 52.2297,
    "lon": 21.0122
  },
  
  "customer_name": "Jan Kowalski",
  "customer_ip": "192.168.1.100",
  "session_id": "sess_123456",
  "employee_id": "EMP1025",
  "receipt_number": "RC_20250608_5432"
}
```

### Pola dodawane przez Logstash

```json
{
  "transaction_class": "premium",  // basic/standard/premium
  "priority": "high",              // low/medium/high
  "margin_percent": 20,            // % marży według kategorii
  "margin_amount": 990.00,         // kwota marży
  "business_hour": "12",           // godzina transakcji
  "data_source": "flask_api",      // źródło danych
  "processed_by": "logstash",      // przetworzony przez
  "environment": "development"     // środowisko
}
```

## 📈 Monitorowanie

### Logi systemu

```bash
# Wszystkie logi
docker-compose logs

# Logi konkretnego serwisu
docker-compose logs -f flask-api
docker-compose logs -f logstash
docker-compose logs -f es-master-1

# Logi w czasie rzeczywistym
docker-compose logs -f
```

### Elasticsearch API

```bash
# Status klastra
curl http://localhost:9200/_cluster/health?pretty

# Lista indeksów
curl http://localhost:9200/_cat/indices?v

# Wyszukiwanie w danych sprzedaży
curl "http://localhost:9200/sprzedaz-*/_search?pretty&size=5"

# Statystyki indeksów
curl http://localhost:9200/_cat/indices/sprzedaz-*?v&h=index,docs.count,store.size
```

### Kibana Dashboards

1. Otwórz http://localhost:5601
2. Przejdź do `Stack Management` → `Index Patterns`
3. Utwórz pattern `sprzedaz-*` z polem czasowym `@timestamp`
4. Przejdź do `Discover` aby przeglądać dane
5. Utwórz dashboardy w `Dashboard`

## 🔧 Rozwiązywanie problemów

### Problem: Flask API nie odpowiada

```bash
# Sprawdź status kontenera
docker-compose ps flask-api

# Sprawdź logi
docker-compose logs flask-api

# Restart serwisu
docker-compose restart flask-api
```

### Problem: Elasticsearch nie uruchamia się

```bash
# Zwiększ vm.max_map_count (Linux)
sudo sysctl -w vm.max_map_count=262144

# Windows/Docker Desktop - zwiększ pamięć do 4GB+
```

### Problem: Brak danych w Elasticsearch

```bash
# Sprawdź czy Logstash otrzymuje dane
docker-compose logs logstash | grep "flask-api"

# Sprawdź indeksy
curl http://localhost:9200/_cat/indices?v

# Test połączenia Logstash
curl -X POST http://localhost:8080 -H "Content-Type: application/json" -d '{"test": "message"}'
```

### Problem: Kibana nie łączy się z Elasticsearch

```bash
# Sprawdź logi Kibana
docker-compose logs kibana

# Sprawdź dostępność ES z kontenera Kibana
docker-compose exec kibana curl http://es-data-1:9200
```

## 📁 Struktura projektu

```
ElasticNoSQL/
├── docker-compose.yml          # Główny plik Docker Compose
├── Dockerfile                  # Dockerfile dla Flask API
├── server.py                   # Flask API - generator danych
├── requirements.txt            # Zależności Python (opcjonalne)
├── .gitignore                  # Pliki ignorowane przez git
├── data/
│   └── logs/
│       └── .gitkeep           # Katalog na logi
└── logstash/
    ├── config/
    │   ├── logstash.yml       # Konfiguracja Logstash
    │   ├── pipelines.yml      # Definicja pipeline
    │   └── sprzedaz-template.json  # Template ES
    └── pipeline/
        └── logstash.conf      # Pipeline przetwarzania
```

### Dodawanie nowych filtrów Logstash

Edytuj `logstash/pipeline/logstash.conf` w sekcji `filter`.

### Modyfikacja klastra Elasticsearch

Dodaj nowe węzły w `docker-compose.yml` lub zmień konfigurację istniejących.

## 📄 Licencja

MIT License - szczegóły w pliku LICENSE.

---

**Autor:** floressek  
**Wersja:** 1.0  
**Data:** 2025-06-08
