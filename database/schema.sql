-- ================================================================
--  NISM Career Intelligence Platform
--  schema.sql  —  complete schema with indexes, FKs, and comments
--
--  Run:   mysql -u root -p < database/schema.sql
-- ================================================================

CREATE DATABASE IF NOT EXISTS nism_job_tracker
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE nism_job_tracker;

-- ────────────────────────────────────────────────────────────────
-- TABLE: companies
-- Master list of hiring organisations
-- ────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS companies (
    company_id      INT             NOT NULL AUTO_INCREMENT,
    company_name    VARCHAR(255)    NOT NULL,
    industry        VARCHAR(100)             DEFAULT NULL,
    headquarters    VARCHAR(255)             DEFAULT NULL,
    website         VARCHAR(255)             DEFAULT NULL,
    linkedin_url    VARCHAR(255)             DEFAULT NULL,
    employee_count  VARCHAR(50)              DEFAULT NULL   COMMENT 'e.g. 1000-5000',
    is_nism_hirer   BOOLEAN                  DEFAULT FALSE  COMMENT 'Company regularly posts NISM jobs',
    created_at      TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (company_id),
    UNIQUE  KEY uq_company_name (company_name),
    INDEX   idx_industry        (industry),
    INDEX   idx_nism_hirer      (is_nism_hirer)
) ENGINE=InnoDB COMMENT='Master company register';


-- ────────────────────────────────────────────────────────────────
-- TABLE: jobs
-- Every scraped / manually entered job listing
-- ────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS jobs (
    job_id              INT             NOT NULL AUTO_INCREMENT,
    company_id          INT                      DEFAULT NULL,   -- FK → companies
    company_name        VARCHAR(255)             DEFAULT NULL,   -- denormalised for speed
    position            VARCHAR(255)    NOT NULL,
    salary_raw          VARCHAR(150)             DEFAULT NULL    COMMENT 'Raw string as scraped',
    salary_min          DECIMAL(12,2)            DEFAULT NULL    COMMENT 'Parsed lower bound (INR/year)',
    salary_max          DECIMAL(12,2)            DEFAULT NULL    COMMENT 'Parsed upper bound (INR/year)',
    location            VARCHAR(255)             DEFAULT NULL,
    city                VARCHAR(100)             DEFAULT NULL    COMMENT 'Normalised city extracted from location',
    experience_required VARCHAR(100)             DEFAULT NULL,
    exp_min_years       TINYINT                  DEFAULT NULL    COMMENT 'Parsed lower bound',
    exp_max_years       TINYINT                  DEFAULT NULL    COMMENT 'Parsed upper bound',
    nism_required       BOOLEAN         NOT NULL DEFAULT FALSE,
    nism_series         VARCHAR(255)             DEFAULT NULL    COMMENT 'e.g. Series V-A, VIII',
    source              VARCHAR(100)             DEFAULT NULL,
    apply_link          TEXT                     DEFAULT NULL,
    job_description     TEXT                     DEFAULT NULL,
    relevance_score     TINYINT UNSIGNED         DEFAULT 0       COMMENT '0-100 score',
    posted_date         DATE                     DEFAULT NULL,
    scraped_date        TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_active           BOOLEAN         NOT NULL DEFAULT TRUE,
    is_duplicate        BOOLEAN         NOT NULL DEFAULT FALSE,

    PRIMARY KEY  (job_id),
    INDEX idx_company_id     (company_id),
    INDEX idx_location       (location),
    INDEX idx_city           (city),
    INDEX idx_source         (source),
    INDEX idx_nism_required  (nism_required),
    INDEX idx_relevance      (relevance_score),
    INDEX idx_posted_date    (posted_date),
    INDEX idx_is_active      (is_active),
    INDEX idx_salary_min     (salary_min),

    CONSTRAINT fk_jobs_company
        FOREIGN KEY (company_id)
        REFERENCES  companies (company_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE

) ENGINE=InnoDB COMMENT='All scraped and manually added job listings';


-- ────────────────────────────────────────────────────────────────
-- TABLE: weekly_stats
-- One row per week — pre-aggregated KPIs
-- ────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS weekly_stats (
    stat_id             INT             NOT NULL AUTO_INCREMENT,
    week_start          DATE            NOT NULL                COMMENT 'Monday of the week (YYYY-MM-DD)',
    total_jobs          INT                      DEFAULT 0,
    new_jobs_this_week  INT                      DEFAULT 0,
    total_companies     INT                      DEFAULT 0,
    nism_required_jobs  INT                      DEFAULT 0,
    avg_relevance_score DECIMAL(5,2)             DEFAULT NULL,
    top_city            VARCHAR(100)             DEFAULT NULL,
    top_position        VARCHAR(255)             DEFAULT NULL,
    top_source          VARCHAR(100)             DEFAULT NULL,
    high_score_jobs     INT                      DEFAULT 0      COMMENT 'jobs with score >= 80',
    created_at          TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at          TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (stat_id),
    UNIQUE KEY  uq_week_start (week_start)

) ENGINE=InnoDB COMMENT='Weekly aggregated KPI snapshots';


-- ────────────────────────────────────────────────────────────────
-- TABLE: scrape_logs
-- Audit trail for every ETL pipeline run
-- ────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS scrape_logs (
    log_id          INT             NOT NULL AUTO_INCREMENT,
    run_id          VARCHAR(36)              DEFAULT NULL    COMMENT 'UUID for grouping multi-source runs',
    source          VARCHAR(100)             DEFAULT NULL,
    jobs_found      INT                      DEFAULT 0,
    jobs_inserted   INT                      DEFAULT 0,
    jobs_skipped    INT                      DEFAULT 0,
    jobs_duplicate  INT                      DEFAULT 0,
    status          ENUM('running','success','failed','partial')
                                    NOT NULL DEFAULT 'running',
    error_message   TEXT                     DEFAULT NULL,
    started_at      TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    finished_at     TIMESTAMP                DEFAULT NULL,

    PRIMARY KEY (log_id),
    INDEX idx_run_id    (run_id),
    INDEX idx_source    (source),
    INDEX idx_status    (status),
    INDEX idx_started   (started_at)

) ENGINE=InnoDB COMMENT='ETL pipeline execution audit log';


-- ────────────────────────────────────────────────────────────────
-- TABLE: salary_benchmarks
-- Weekly salary stats by role/city for trend analysis
-- ────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS salary_benchmarks (
    benchmark_id    INT             NOT NULL AUTO_INCREMENT,
    week_start      DATE            NOT NULL,
    city            VARCHAR(100)             DEFAULT NULL,
    position_group  VARCHAR(100)             DEFAULT NULL    COMMENT 'Bucketed role e.g. Analyst, Advisor, Manager',
    sample_size     INT                      DEFAULT 0,
    salary_min      DECIMAL(12,2)            DEFAULT NULL,
    salary_max      DECIMAL(12,2)            DEFAULT NULL,
    salary_avg      DECIMAL(12,2)            DEFAULT NULL,
    salary_median   DECIMAL(12,2)            DEFAULT NULL,
    created_at      TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (benchmark_id),
    INDEX idx_week      (week_start),
    INDEX idx_city      (city),
    INDEX idx_position  (position_group)

) ENGINE=InnoDB COMMENT='Salary trend benchmarks by role and city';


-- ────────────────────────────────────────────────────────────────
-- VERIFY
-- ────────────────────────────────────────────────────────────────
SELECT
    TABLE_NAME,
    TABLE_ROWS,
    ENGINE,
    TABLE_COMMENT
FROM information_schema.TABLES
WHERE TABLE_SCHEMA = 'nism_job_tracker'
ORDER BY TABLE_NAME;
