# ── Dashboard Settings ───────────────────────────────────────
APP_TITLE       = "NISM Career Intelligence Platform"
APP_ICON        = "📊"
APP_LAYOUT      = "wide"
THEME_COLOR     = "#1565C0"

# ── Scheduler ────────────────────────────────────────────────
SCRAPE_DAY      = "monday"         # day of week to auto-scrape
SCRAPE_TIME     = "08:00"          # 24h format
REPORT_TIME     = "09:00"          # send email report after scrape

# ── Scoring Weights ──────────────────────────────────────────
RELEVANCE_WEIGHTS = {
    "nism_required": 40,
    "keyword_in_title": 30,
    "keyword_in_description": 20,
    "recent_posting": 10,
}

# ── Job Sources ──────────────────────────────────────────────
SOURCES = ["LinkedIn", "Naukri", "Indeed", "Manual"]

# ── Locations to prioritise ──────────────────────────────────
TARGET_CITIES = [
    "Mumbai", "Delhi", "Bangalore", "Hyderabad",
    "Chennai", "Pune", "Kolkata", "Ahmedabad",
]
