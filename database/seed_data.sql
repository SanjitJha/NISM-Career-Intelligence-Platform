-- ============================================================
--  Seed Data — 20 sample jobs for testing
-- ============================================================
USE nism_job_tracker;

INSERT INTO companies (company_name, industry, headquarters) VALUES
('HDFC Asset Management',   'Asset Management', 'Mumbai'),
('Zerodha',                 'FinTech',          'Bangalore'),
('ICICI Securities',        'Brokerage',        'Mumbai'),
('Motilal Oswal',           'Wealth Management','Mumbai'),
('Groww',                   'FinTech',          'Bangalore'),
('Angel One',               'Brokerage',        'Mumbai'),
('Mirae Asset',             'Asset Management', 'Mumbai'),
('Kotak Securities',        'Brokerage',        'Mumbai');

INSERT INTO jobs
    (company_name, position, salary, location, experience_required,
     nism_required, source, relevance_score, posted_date, job_description)
VALUES
('HDFC Asset Management','Mutual Fund Advisor','₹4L–₹7L PA','Mumbai','1–3 years',TRUE,'LinkedIn',90,'2024-01-10','NISM Series V-A certification required. Role involves client advisory for mutual fund investments.'),
('Zerodha','Equity Research Analyst','₹6L–₹10L PA','Bangalore','2–4 years',TRUE,'Naukri',85,'2024-01-12','NISM Series VIII required. Responsible for in-depth research on listed equities.'),
('ICICI Securities','Relationship Manager – Wealth','₹5L–₹9L PA','Mumbai','2–5 years',TRUE,'LinkedIn',88,'2024-01-08','AMFI/NISM certified preferred. Manage HNI client portfolios and provide investment advisory.'),
('Motilal Oswal','Research Analyst – Derivatives','₹8L–₹14L PA','Delhi','3–6 years',TRUE,'Indeed',82,'2024-01-15','NISM Series VIII certification mandatory. Derivative strategy and option chain analysis.'),
('Groww','Product Manager – Investment','₹12L–₹18L PA','Bangalore','4–7 years',FALSE,'LinkedIn',60,'2024-01-11','Experience with mutual funds and investment products preferred. No mandatory NISM requirement.'),
('Angel One','Branch Manager','₹6L–₹10L PA','Hyderabad','3–5 years',TRUE,'Naukri',80,'2024-01-09','NISM Series VII or equivalent. Manage branch operations and client acquisition.'),
('Mirae Asset','Fund Manager Assistant','₹7L–₹12L PA','Mumbai','2–4 years',TRUE,'LinkedIn',87,'2024-01-14','NISM Series V-A + CFA Level 1 preferred. Support senior fund managers in portfolio construction.'),
('Kotak Securities','Dealer – Equity','₹4L–₹6L PA','Chennai','1–2 years',TRUE,'Naukri',75,'2024-01-07','NISM Series VII mandatory. Execute equity trades and manage client portfolios.'),
('HDFC Asset Management','Compliance Officer','₹8L–₹13L PA','Mumbai','4–6 years',TRUE,'LinkedIn',78,'2024-01-16','NISM Series VI preferred. Ensure regulatory compliance with SEBI guidelines.'),
('Zerodha','Data Analyst – Trading','₹8L–₹12L PA','Bangalore','2–4 years',FALSE,'LinkedIn',55,'2024-01-13','Analyse trading data and user behaviour. Python and SQL required.'),
('ICICI Securities','Investment Advisor','₹5L–₹8L PA','Pune','1–3 years',TRUE,'Naukri',85,'2024-01-10','NISM Series X-A mandatory. Provide personalised investment advice to retail clients.'),
('Motilal Oswal','Portfolio Manager','₹15L–₹22L PA','Mumbai','6–10 years',TRUE,'Indeed',92,'2024-01-05','NISM Series XXI-A required for PMS operations. Manage discretionary portfolios for HNI clients.'),
('Groww','Business Analyst','₹7L–₹11L PA','Bangalore','2–3 years',FALSE,'LinkedIn',45,'2024-01-12','Analyse business metrics and drive growth. Finance background a plus.'),
('Angel One','Equity Advisor','₹4L–₹7L PA','Kolkata','1–2 years',TRUE,'Manual',78,'2024-01-06','NISM Series VIII certification required. Advise clients on equity investments.'),
('Mirae Asset','Marketing Executive – MF','₹4L–₹6L PA','Delhi','1–2 years',FALSE,'Naukri',50,'2024-01-11','Promote mutual fund schemes. NISM awareness preferred but not mandatory.'),
('Kotak Securities','Risk Analyst','₹9L–₹14L PA','Mumbai','3–5 years',TRUE,'LinkedIn',80,'2024-01-15','NISM certifications valued. Assess market and credit risk for equity portfolios.'),
('HDFC Asset Management','Sales Manager – Direct MF','₹7L–₹11L PA','Ahmedabad','3–5 years',TRUE,'Naukri',83,'2024-01-08','NISM Series V-A required. Drive direct mutual fund sales across the region.'),
('Zerodha','Backend Developer – FinTech','₹14L–₹20L PA','Bangalore','3–5 years',FALSE,'LinkedIn',30,'2024-01-14','Python, Go, distributed systems. Finance domain knowledge a plus.'),
('ICICI Securities','Derivatives Trader','₹10L–₹16L PA','Mumbai','2–4 years',TRUE,'Indeed',86,'2024-01-09','NISM Series VIII mandatory. Execute derivatives strategies for institutional clients.'),
('Motilal Oswal','Wealth Advisor – HNI','₹9L–₹15L PA','Mumbai','3–6 years',TRUE,'LinkedIn',89,'2024-01-16','NISM Series X-A + CFP preferred. Build and manage relationships with high net worth clients.');

-- Initial weekly stats snapshot
INSERT INTO weekly_stats
    (week_start, total_jobs, new_jobs_this_week, total_companies,
     nism_required_jobs, top_city, top_position, avg_relevance_score)
VALUES ('2024-01-08', 20, 20, 8, 15, 'Mumbai', 'Mutual Fund Advisor', 74.50);
