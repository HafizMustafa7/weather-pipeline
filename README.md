# 🌦️ Weather ETL Pipeline

> *"Every byte of data tells a story — this pipeline listens to the sky."*

A fully automated, production-style **Extract → Transform → Load** data pipeline that fetches real-time weather data from **20+ cities across the globe**, archives raw data to **AWS S3**, transforms it with **Pandas**, and loads it into a **PostgreSQL** data warehouse — all running silently every night via **GitHub Actions**.

Built from scratch as a portfolio project to demonstrate real-world data engineering skills.

---

## 🌍 Cities Monitored

```
Lahore · Karachi · Islamabad · London · New York · Tokyo · Paris
Dubai · Sydney · Toronto · Berlin · Singapore · Cairo · Mumbai
Beijing · Los Angeles · Istanbul · Moscow · Bangkok · Lagos
```

---

## 🏗️ Architecture

```
OpenWeatherMap API
        │
        ▼
   [extract.py]          ← Fetches live JSON for 20+ cities
        │
        ├──────────────► AWS S3  (raw/weather_YYYYMMDD.json)
        │                         Raw backup — untouched, always safe
        ▼
  [transform.py]         ← Pandas: parse, normalize, remove outliers
        │
        ▼
   [load_db.py]          ← Star Schema insert into PostgreSQL
        │
        ▼
  PostgreSQL @ Neon.tech
  ┌─────────────┐    ┌──────────────────────────────────────────┐
  │  dim_city   │    │              fact_weather                │
  │─────────────│    │──────────────────────────────────────────│
  │ city_id  PK │◄───│ city_id FK                               │
  │ name        │    │ temperature · humidity · wind · pressure │
  │ country     │    │ description · recorded_at                │
  │ lat · lon   │    └──────────────────────────────────────────┘
  └─────────────┘

        ⏰ GitHub Actions — runs every day at midnight UTC
```

---

## ⚙️ Tech Stack

| Layer | Tool | Purpose |
|---|---|---|
| Language | Python 3.11 | Core pipeline logic |
| Data Source | OpenWeatherMap API | Real-time weather JSON |
| Raw Storage | AWS S3 | Immutable raw backup |
| Transformation | Pandas | Cleaning, parsing, outlier removal |
| Data Warehouse | PostgreSQL (Neon.tech) | Star schema storage |
| Automation | GitHub Actions | Daily cron scheduling |
| Secret Management | GitHub Secrets | Secure credential handling |

---

## 📁 Project Structure

```
weather-pipeline/
│
├── pipeline.py              # Main entry point — orchestrates all steps
│
├── steps/
│   ├── extract.py           # Fetches weather data from OpenWeatherMap
│   ├── transform.py         # Cleans and normalizes raw JSON with Pandas
│   ├── load_s3.py           # Uploads raw JSON backup to AWS S3
│   └── load_db.py           # Inserts transformed data into PostgreSQL
│
├── .github/
│   └── workflows/
│       └── pipeline.yml     # GitHub Actions — daily automation
│
├── requirements.txt         # Python dependencies
├── .env                     # Local secrets (never committed)
└── .gitignore               # Protects .env and venv from Git
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/weather-pipeline.git
cd weather-pipeline
```

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac / Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the root directory:

```env
OWM_API_KEY=your_openweathermap_api_key
AWS_ACCESS_KEY=your_aws_access_key
AWS_SECRET_KEY=your_aws_secret_key
AWS_BUCKET=your_s3_bucket_name
AWS_REGION=us-east-1
DATABASE_URL=postgresql://user:pass@ep-xxx.neon.tech/neondb?sslmode=require
```

### 5. Run the pipeline

```bash
python pipeline.py
```

**Expected output:**
```
=== Weather Pipeline Shuru ===
[1] Data fetch ho raha hai...
  ✓ Lahore   ✓ London   ✓ New York  ... (20 cities)
[2] S3 mein save ho raha hai...
  ✓ raw/weather_20240607_000000.json
[3] Data transform ho raha hai...
  ✓ Clean rows: 20
[4] Database mein load ho raha hai...
  ✓ 20 rows inserted
=== Pipeline Complete! ===
```

---

## 🔄 Data Transformation Details

Raw JSON from OpenWeatherMap goes through a 3-step cleaning process:

**1. Parsing** — Nested dictionaries flattened into a clean tabular structure:
```
temperature, humidity, wind_speed, pressure, description, lat, lon, recorded_at
```

**2. Normalization** — Unix timestamps converted to UTC datetime format:
```python
datetime.fromtimestamp(d["dt"], tz=timezone.utc)
```

**3. Outlier Removal** — Physically impossible values are dropped:
```python
df = df[(df["temperature"] >= -100) & (df["temperature"] <= 60)]
```

---

## ⏰ Automation

The pipeline runs **automatically every day at midnight UTC** via GitHub Actions.

```yaml
on:
  schedule:
    - cron: '0 0 * * *'
  workflow_dispatch:         # Can also be triggered manually
```

All secrets (API keys, database credentials) are stored in **GitHub Secrets** — never hardcoded in source code.

---

## 🗄️ Querying the Data

Once data is loaded, you can query it directly from Neon.tech SQL Editor:

```sql
-- Latest weather snapshot for all cities
SELECT
    c.name        AS city,
    c.country,
    w.temperature AS temp_c,
    w.humidity    AS humidity_pct,
    w.wind_speed  AS wind_ms,
    w.description,
    w.recorded_at
FROM fact_weather w
JOIN dim_city c ON w.city_id = c.city_id
ORDER BY w.recorded_at DESC, c.name;
```

```sql
-- Hottest cities today
SELECT c.name, MAX(w.temperature) AS max_temp
FROM fact_weather w
JOIN dim_city c ON w.city_id = c.city_id
WHERE DATE(w.recorded_at) = CURRENT_DATE
GROUP BY c.name
ORDER BY max_temp DESC;
```

---

## 🔐 Security

- `.env` file is listed in `.gitignore` — credentials never reach GitHub
- All CI/CD secrets managed via **GitHub Repository Secrets**
- AWS IAM user has minimal permissions — S3 access only
- Neon.tech connection requires SSL (`sslmode=require`)

---

## 📈 Future Improvements

- [ ] Add a data visualization dashboard (Metabase / Grafana)
- [ ] Expand to 50+ cities
- [ ] Add weather alerts via email/SMS when thresholds crossed
- [ ] Store processed data in S3 Parquet format as well
- [ ] Add data quality checks with Great Expectations

---

## 🤝 Connect

Built with curiosity, caffeine, and a lot of debugging.

If you found this useful or want to collaborate — feel free to reach out!

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=flat&logo=github&logoColor=white)](https://github.com/YOUR_USERNAME)

---


