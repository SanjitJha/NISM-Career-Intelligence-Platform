-- ============================================================
--  NISM Career Intelligence Platform — Schema
--  Run: mysql -u root -p < database/schema.sql
-- ============================================================

CREATE DATABASE IF NOT EXISTS nism_job_tracker
    CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE nism_job_tracker;

-- ── Companies ────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS companies (
    company_id      INT AUTO_INCREMENT PRIMARY KEY,
    company_name    VARCHAR(255) NOT NULL,
    industry        VARCHAR(100),
    headquarters    VARCHAR(255),
    website         VARCHAR(255),
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_company_name (company_name)
);

-- ── Jobs ─────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS jobs (
    job_id              INT AUTO_INCREMENT PRIMARY KEY,
    company_name        VARCHAR(255),
    position            VARCHAR(255),
    salary              VARCHAR(100),
    location            VARCHAR(255),
    experience_required VARCHAR(100),
    nism_required       BOOLEAN DEFAULT FALSE,
    source              VARCHAR(100),
    apply_link          TEXT,
    job_description     TEXT,
    relevance_score     INT DEFAULT 0,
    posted_date         DATE,
    scraped_date        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active           BOOLEAN DEFAULT TRUE,
    INDEX idx_location      (location),
    INDEX idx_source        (source),
    INDEX idx_nism          (nism_required),
    INDEX idx_relevance     (relevance_score),
    INDEX idx_posted_date   (posted_date)
);

-- ── Weekly Statistics ────────────────────────────────────────
CREATE TABLE IF NOT EXISTS weekly_stats (
    stat_id             INT AUTO_INCREMENT PRIMARY KEY,
    week_start          DATE NOT NULL,
    total_jobs          INT DEFAULT 0,
    new_jobs_this_week  INT DEFAULT 0,
    total_companies     INT DEFAULT 0,
    nism_required_jobs  INT DEFAULT 0,
    top_city            VARCHAR(100),
    top_position        VARCHAR(255),
    avg_relevance_score DECIMAL(5,2),
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_week_start (week_start)
);

-- ── Scrape Logs ──────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS scrape_logs (
    log_id          INT AUTO_INCREMENT PRIMARY KEY,
    source          VARCHAR(100),
    jobs_found      INT DEFAULT 0,
    jobs_inserted   INT DEFAULT 0,
    jobs_skipped    INT DEFAULT 0,
    status          ENUM('success','failed','partial') DEFAULT 'success',
    error_message   TEXT,
    started_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    finished_at     TIMESTAMP NULL
);
