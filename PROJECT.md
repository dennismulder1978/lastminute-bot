# HolidayHunter

HolidayHunter is een Python-applicatie die automatisch vakantiedeals verzamelt van verschillende aanbieders en de gebruiker via Telegram informeert over:

- nieuwe deals;
- prijsdalingen;
- interessante aanbiedingen.

Het uiteindelijke doel is één centrale zoekmachine voor vakanties met slimme filters, deal scoring en een dashboard.

---

# Huidige functionaliteit

## Werkt

- Center Parcs scraper (dummy)
- Scheduler (APScheduler)
- Telegram notificaties
- SQLite database
- Nieuwe deals detecteren
- Prijswijzigingen detecteren
- Configuratie via YAML

---

# Providers

| Provider | Status |
|----------|--------|
| Center Parcs | In ontwikkeling |
| Eurocamp | Gepland |
| Roan | Gepland |
| Landal | Gepland |
| Sunweb | Toekomst |
| TUI | Toekomst |
| Corendon | Toekomst |

---

# Roadmap

## Sprint 1
- Projectstructuur

## Sprint 2
- Telegram notificaties

## Sprint 3
- Scheduler

## Sprint 4
- Database

## Sprint 5
- Deal detectie
- Prijswijzigingen
- YAML configuratie

## Sprint 6
- Echte Center Parcs scraper

## Sprint 7
- Eurocamp scraper

## Sprint 8
- Roan scraper

## Sprint 9
- Landal scraper

## Sprint 10
- AI Deal Score

## Sprint 11
- Dashboard

## Sprint 12
- Docker deployment

---

# Configuratie

De gebruiker configureert alles via:

config.yaml

Daarin staan onder andere:

- gezinssamenstelling
- reisduur
- vertrekdata
- landen
- providers
- scheduler

---

# Database

SQLite

Momenteel:

table deals

Belangrijkste velden:

- source
- title
- location
- url
- price
- first_seen
- last_seen

---

# Notificaties

Telegram Bot API

Berichten:

- nieuwe deal
- prijswijziging

Later:

- dagelijkse samenvatting
- wekelijkse samenvatting
- AI aanbevelingen

---

# Techniek

Python 3.14

Belangrijkste libraries

- APScheduler
- python-telegram-bot
- requests
- BeautifulSoup
- SQLite
- PyYAML

Later

- FastAPI
- SQLAlchemy
- Docker
- Playwright