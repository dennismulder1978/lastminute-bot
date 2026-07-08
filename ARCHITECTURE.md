# HolidayHunter Architecture

## Mappenstructuur

app/

config/
settings.py
config_loader.py

core/
deal_service.py

database/
db.py
manager.py

models/
deal.py

notifier/
telegram.py

scrapers/

base.py

centerparcs.py

manager.py

scheduler.py

main.py

---

# Flow

Scheduler

↓

run_scrapers()

↓

CenterParcsScraper

↓

Deal object

↓

DealService

↓

DatabaseManager

↓

TelegramNotifier

---

# Deal object

Iedere scraper levert altijd een lijst met Deal objecten.

```python
Deal(
    source,
    title,
    location,
    price,
    url,
)