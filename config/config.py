import os
from dotenv import load_dotenv

load_dotenv()

# ── Database ────────────────────────────────────────────────
DB_HOST     = os.getenv("DB_HOST", "localhost")
DB_USER     = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root")
DB_NAME     = os.getenv("DB_NAME", "nism_job_tracker")
DB_PORT     = int(os.getenv("DB_PORT", 3306))

# ── Scraper ─────────────────────────────────────────────────
REQUEST_TIMEOUT     = 10          # seconds
REQUEST_DELAY       = 2           # seconds between requests (polite scraping)
MAX_RETRIES         = 3
USER_AGENT          = "Mozilla/5.0 (compatible; NISMJobBot/1.0)"

# ── Keywords (used to judge NISM relevance) ─────────────────
NISM_KEYWORDS = [
    "NISM", "NISM certified", "AMFI", "SEBI",
    "mutual fund", "equity research", "wealth management",
    "portfolio management", "research analyst", "financial advisor",
    "investment banking", "capital markets", "stock broker",
]

# ── Data Paths ───────────────────────────────────────────────
DATA_RAW_PATH       = "data/raw/"
DATA_PROCESSED_PATH = "data/processed/"
DATA_EXPORTS_PATH   = "data/exports/"
LOG_PATH            = "logs/"

# ── Email Report (fill in .env) ──────────────────────────────
EMAIL_SENDER    = os.getenv("EMAIL_SENDER", "")
EMAIL_PASSWORD  = os.getenv("EMAIL_PASSWORD", "")
EMAIL_RECIPIENT = os.getenv("EMAIL_RECIPIENT", "")
SMTP_HOST       = "smtp.gmail.com"
SMTP_PORT       = 587
