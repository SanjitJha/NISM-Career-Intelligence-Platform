# 📊 NISM Career Intelligence Platform

> Automated job market intelligence for NISM-certified finance professionals.
> Built with Python · MySQL · Streamlit · Plotly

---

## 🧭 Overview

The NISM Career Intelligence Platform aggregates, analyses, and visualises
job listings requiring NISM certifications across major Indian job portals.
It runs a weekly ETL pipeline, stores data in MySQL, and surfaces insights
through an interactive Streamlit dashboard.

---

## ✨ Features

| Feature               | Description                                      |
|-----------------------|--------------------------------------------------|
| 🕷️ Multi-source Scraping | LinkedIn, Naukri, Indeed (pluggable architecture) |
| 🔄 ETL Pipeline        | Extract → Transform → Load with relevance scoring |
| 🗄️ MySQL Storage       | Normalised schema with weekly statistics          |
| 📊 Live Dashboard      | Streamlit + Plotly with filters & charts          |
| 📅 Weekly Automation   | Schedule-based auto-scrape + email reports        |
| 📧 Email Reports       | Excel attachment sent every Monday               |

---

## 🗂️ Project Structure

```
NISM-Career-Intelligence-Platform/
├── config/          # DB credentials, app settings, keywords
├── database/        # Schema, seed data, reusable DB connector
├── data/            # raw/ · processed/ · exports/
├── etl/             # extractor · transformer · loader · pipeline
├── scraper/         # LinkedIn · Naukri · Indeed · common utils
├── dashboard/       # Streamlit app + pages (overview, jobs, analytics, reports)
├── scheduler/       # Weekly cron-style automation
├── reports/         # Excel report generator + email sender
├── tests/           # pytest unit tests for ETL modules
└── docs/            # Architecture diagram, screenshots
```

---

## 🧰 Technology Stack

- **Language:** Python 3.11+
- **Database:** MySQL 8.0
- **Dashboard:** Streamlit + Plotly
- **Scraping:** Requests + BeautifulSoup
- **ETL:** Pandas + mysql-connector-python
- **Scheduler:** schedule
- **Testing:** pytest

---

## 🚀 Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/NISM-Career-Intelligence-Platform.git
cd NISM-Career-Intelligence-Platform
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment
```bash
cp .env.example .env
# Edit .env with your MySQL credentials
```

### 5. Set up MySQL database
```bash
mysql -u root -p < database/schema.sql
mysql -u root -p nism_job_tracker < database/seed_data.sql
```

### 6. Test the connection
```bash
python database/db_connection.py
```

### 7. Run the dashboard
```bash
streamlit run dashboard/app.py
```

### 8. Run ETL pipeline (processes files in data/raw/)
```bash
python etl/pipeline.py
```

### 9. Run tests
```bash
pytest tests/
```

---

## 📐 Architecture

```
Job Sources (LinkedIn / Naukri / Indeed)
             │
             ▼
      [ ETL Pipeline ]
      Extract → Transform → Load
             │
             ▼
      [ MySQL Database ]
      jobs · companies · weekly_stats · scrape_logs
             │
             ▼
      [ Streamlit Dashboard ]
      Overview · Jobs · Analytics · Reports
             │
             ▼
      [ Weekly Scheduler ]
      Auto-scrape every Monday → Email report
```

---

## 🗄️ Database Schema

| Table           | Purpose                             |
|-----------------|-------------------------------------|
| `jobs`          | All scraped job listings            |
| `companies`     | Company master data                 |
| `weekly_stats`  | Aggregated weekly KPI snapshots     |
| `scrape_logs`   | ETL run audit trail                 |

---

## 📸 Screenshots

> *(Add screenshots to docs/screenshots/ after running the dashboard)*

---

## 🔮 Roadmap

- [ ] Milestone 1: Foundation (DB + ETL) ✅
- [ ] Milestone 2: Live scrapers (LinkedIn, Naukri)
- [ ] Milestone 3: Full Streamlit dashboard
- [ ] Milestone 4: Weekly automation + email
- [ ] Milestone 5: Salary trend analysis

---

## 👨‍💻 Author

Built as a portfolio project demonstrating end-to-end data engineering.
