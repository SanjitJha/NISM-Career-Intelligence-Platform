-- ================================================================
--  NISM Career Intelligence Platform
--  seed_data.sql  —  realistic test data (50 jobs, 10 companies)
--
--  Run AFTER schema.sql:
--     mysql -u root -p nism_job_tracker < database/seed_data.sql
-- ================================================================

USE nism_job_tracker;

-- ────────────────────────────────────────────────────────────────
-- COMPANIES  (10 real-world finance firms)
-- ────────────────────────────────────────────────────────────────
INSERT INTO companies
    (company_name, industry, headquarters, website, is_nism_hirer)
VALUES
    ('HDFC Asset Management',    'Asset Management',  'Mumbai',    'https://www.hdfcfund.com',    TRUE),
    ('Zerodha',                  'FinTech / Brokerage','Bangalore','https://zerodha.com',          TRUE),
    ('ICICI Securities',         'Brokerage',         'Mumbai',    'https://www.icicidirect.com',  TRUE),
    ('Motilal Oswal Financial',  'Wealth Management', 'Mumbai',    'https://www.motilaloswal.com', TRUE),
    ('Groww',                    'FinTech',           'Bangalore', 'https://groww.in',             FALSE),
    ('Angel One',                'Brokerage',         'Mumbai',    'https://www.angelone.in',      TRUE),
    ('Mirae Asset',              'Asset Management',  'Mumbai',    'https://www.miraeassetmf.co.in',TRUE),
    ('Kotak Securities',         'Brokerage',         'Mumbai',    'https://www.kotaksecurities.com',TRUE),
    ('Nippon India Mutual Fund', 'Asset Management',  'Mumbai',    'https://www.nipponindiamf.com',TRUE),
    ('Paytm Money',              'FinTech',           'Bangalore', 'https://www.paytmmoney.com',   FALSE)
ON DUPLICATE KEY UPDATE is_nism_hirer = VALUES(is_nism_hirer);


-- ────────────────────────────────────────────────────────────────
-- JOBS  (50 listings covering 8 cities, varied NISM series)
-- ────────────────────────────────────────────────────────────────
INSERT INTO jobs
    (company_name, position, salary_raw, salary_min, salary_max,
     location, city, experience_required, exp_min_years, exp_max_years,
     nism_required, nism_series, source, apply_link,
     relevance_score, posted_date, job_description)
VALUES

-- ── HDFC Asset Management ──────────────────────────────────
('HDFC Asset Management',
 'Mutual Fund Advisor', '₹4L–₹7L PA', 400000, 700000,
 'Mumbai, Maharashtra', 'Mumbai', '1–3 years', 1, 3,
 TRUE, 'Series V-A', 'LinkedIn', 'https://linkedin.com/jobs/1001',
 90, '2024-01-10',
 'NISM Series V-A certification mandatory. Role involves advising retail clients on SIP, lump sum, and goal-based mutual fund investments. Strong interpersonal and financial planning skills required.'),

('HDFC Asset Management',
 'Compliance Officer – MF', '₹8L–₹13L PA', 800000, 1300000,
 'Mumbai, Maharashtra', 'Mumbai', '4–6 years', 4, 6,
 TRUE, 'Series VI', 'Naukri', 'https://naukri.com/jobs/1002',
 78, '2024-01-16',
 'NISM Series VI preferred. Ensure SEBI LODR and AMFI compliance. Handle regulatory filings and internal audit coordination.'),

('HDFC Asset Management',
 'Sales Manager – Direct MF', '₹7L–₹11L PA', 700000, 1100000,
 'Ahmedabad, Gujarat', 'Ahmedabad', '3–5 years', 3, 5,
 TRUE, 'Series V-A', 'Naukri', 'https://naukri.com/jobs/1003',
 83, '2024-01-08',
 'Drive direct mutual fund sales across Gujarat. NISM Series V-A required. Manage distributor relationships and achieve monthly AUM targets.'),

-- ── Zerodha ────────────────────────────────────────────────
('Zerodha',
 'Equity Research Analyst', '₹6L–₹10L PA', 600000, 1000000,
 'Bangalore, Karnataka', 'Bangalore', '2–4 years', 2, 4,
 TRUE, 'Series VIII', 'Naukri', 'https://naukri.com/jobs/1004',
 85, '2024-01-12',
 'NISM Series VIII mandatory. Conduct deep-dive research on NSE/BSE listed equities. Publish weekly equity notes for 1M+ Zerodha users. Python for data analysis a strong plus.'),

('Zerodha',
 'Data Analyst – Trading Insights', '₹8L–₹12L PA', 800000, 1200000,
 'Bangalore, Karnataka', 'Bangalore', '2–4 years', 2, 4,
 FALSE, NULL, 'LinkedIn', 'https://linkedin.com/jobs/1005',
 55, '2024-01-13',
 'Analyse trading behaviour, cohort metrics, and product funnel data. SQL, Python, Tableau required. Finance domain knowledge appreciated but NISM not mandatory.'),

('Zerodha',
 'Backend Developer – FinTech', '₹14L–₹20L PA', 1400000, 2000000,
 'Bangalore, Karnataka', 'Bangalore', '3–5 years', 3, 5,
 FALSE, NULL, 'LinkedIn', 'https://linkedin.com/jobs/1006',
 30, '2024-01-14',
 'Build Zerodha trading infrastructure in Python and Go. Distributed systems, Redis, Kafka experience needed. Finance knowledge a plus but not required.'),

-- ── ICICI Securities ───────────────────────────────────────
('ICICI Securities',
 'Relationship Manager – Wealth', '₹5L–₹9L PA', 500000, 900000,
 'Mumbai, Maharashtra', 'Mumbai', '2–5 years', 2, 5,
 TRUE, 'Series X-A', 'LinkedIn', 'https://linkedin.com/jobs/1007',
 88, '2024-01-08',
 'AMFI and NISM Series X-A certified preferred. Manage HNI client portfolios above ₹50L. Conduct quarterly portfolio reviews and recommend rebalancing strategies.'),

('ICICI Securities',
 'Investment Advisor – Retail', '₹5L–₹8L PA', 500000, 800000,
 'Pune, Maharashtra', 'Pune', '1–3 years', 1, 3,
 TRUE, 'Series X-A', 'Naukri', 'https://naukri.com/jobs/1008',
 85, '2024-01-10',
 'NISM Series X-A mandatory. Provide personalised investment advice (equities, MF, bonds) to retail clients. Must be SEBI IA registered or eligible.'),

('ICICI Securities',
 'Derivatives Trader', '₹10L–₹16L PA', 1000000, 1600000,
 'Mumbai, Maharashtra', 'Mumbai', '2–4 years', 2, 4,
 TRUE, 'Series VIII', 'Indeed', 'https://indeed.com/jobs/1009',
 86, '2024-01-09',
 'NISM Series VIII mandatory. Execute F&O strategies for proprietary desk. Options pricing, Greeks, and volatility surface analysis experience required.'),

-- ── Motilal Oswal ──────────────────────────────────────────
('Motilal Oswal Financial',
 'Research Analyst – Derivatives', '₹8L–₹14L PA', 800000, 1400000,
 'Delhi, NCR', 'Delhi', '3–6 years', 3, 6,
 TRUE, 'Series VIII', 'Indeed', 'https://indeed.com/jobs/1010',
 82, '2024-01-15',
 'NISM Series VIII certification mandatory. Derivative strategy and option chain analysis. Publish daily option flow reports. CFA Level 1 or higher preferred.'),

('Motilal Oswal Financial',
 'Portfolio Manager – PMS', '₹15L–₹22L PA', 1500000, 2200000,
 'Mumbai, Maharashtra', 'Mumbai', '6–10 years', 6, 10,
 TRUE, 'Series XXI-A', 'Indeed', 'https://indeed.com/jobs/1011',
 92, '2024-01-05',
 'NISM Series XXI-A (Portfolio Managers) required for SEBI-registered PMS operations. Manage discretionary portfolios for HNI clients (>₹50L ticket size). CFA / CPA strongly preferred.'),

('Motilal Oswal Financial',
 'Wealth Advisor – HNI', '₹9L–₹15L PA', 900000, 1500000,
 'Mumbai, Maharashtra', 'Mumbai', '3–6 years', 3, 6,
 TRUE, 'Series X-A', 'LinkedIn', 'https://linkedin.com/jobs/1012',
 89, '2024-01-16',
 'NISM Series X-A and CFP preferred. Build and manage relationships with high net worth clients. Provide holistic financial planning covering equity, debt, insurance, and real estate.'),

-- ── Groww ──────────────────────────────────────────────────
('Groww',
 'Product Manager – Investment', '₹12L–₹18L PA', 1200000, 1800000,
 'Bangalore, Karnataka', 'Bangalore', '4–7 years', 4, 7,
 FALSE, NULL, 'LinkedIn', 'https://linkedin.com/jobs/1013',
 60, '2024-01-11',
 'Lead the investment products roadmap (mutual funds, stocks, gold). NISM awareness preferred. Work cross-functionally with engineering, design, and compliance teams.'),

('Groww',
 'Business Analyst – Growth', '₹7L–₹11L PA', 700000, 1100000,
 'Bangalore, Karnataka', 'Bangalore', '2–3 years', 2, 3,
 FALSE, NULL, 'LinkedIn', 'https://linkedin.com/jobs/1014',
 45, '2024-01-12',
 'Analyse user acquisition funnels and cohort retention for Groww''s investment platform. SQL and Excel proficiency required. Finance knowledge a strong plus.'),

-- ── Angel One ──────────────────────────────────────────────
('Angel One',
 'Branch Manager – Brokerage', '₹6L–₹10L PA', 600000, 1000000,
 'Hyderabad, Telangana', 'Hyderabad', '3–5 years', 3, 5,
 TRUE, 'Series VII', 'Naukri', 'https://naukri.com/jobs/1015',
 80, '2024-01-09',
 'NISM Series VII or equivalent. Manage branch P&L, team of 10 advisors, and client acquisition. Strong knowledge of equity markets and demat account operations.'),

('Angel One',
 'Equity Advisor – Retail', '₹4L–₹7L PA', 400000, 700000,
 'Kolkata, West Bengal', 'Kolkata', '1–2 years', 1, 2,
 TRUE, 'Series VIII', 'Manual', 'https://angelone.in/careers/1016',
 78, '2024-01-06',
 'NISM Series VIII certification required. Advise retail clients on equity investments. Target-driven role with performance incentives. Freshers with NISM certification may apply.'),

('Angel One',
 'KYC & Compliance Executive', '₹3.5L–₹5.5L PA', 350000, 550000,
 'Chennai, Tamil Nadu', 'Chennai', '0–2 years', 0, 2,
 TRUE, 'Series VI', 'Naukri', 'https://naukri.com/jobs/1017',
 65, '2024-01-13',
 'NISM Series VI preferred. Manage KYC documentation, SEBI compliance filings, and anti-money laundering (AML) monitoring. Entry-level role suitable for recent graduates.'),

-- ── Mirae Asset ────────────────────────────────────────────
('Mirae Asset',
 'Fund Manager Assistant', '₹7L–₹12L PA', 700000, 1200000,
 'Mumbai, Maharashtra', 'Mumbai', '2–4 years', 2, 4,
 TRUE, 'Series V-A', 'LinkedIn', 'https://linkedin.com/jobs/1018',
 87, '2024-01-14',
 'NISM Series V-A and CFA Level 1 preferred. Support senior fund managers in equity portfolio construction, fundamental analysis, and performance attribution.'),

('Mirae Asset',
 'Marketing Executive – MF Distribution', '₹4L–₹6L PA', 400000, 600000,
 'Delhi, NCR', 'Delhi', '1–2 years', 1, 2,
 FALSE, NULL, 'Naukri', 'https://naukri.com/jobs/1019',
 50, '2024-01-11',
 'Promote Mirae Asset mutual fund schemes through IFA and bank channels. NISM awareness preferred but not mandatory. Good communication and presentation skills required.'),

-- ── Kotak Securities ───────────────────────────────────────
('Kotak Securities',
 'Dealer – Equity Trading', '₹4L–₹6L PA', 400000, 600000,
 'Chennai, Tamil Nadu', 'Chennai', '1–2 years', 1, 2,
 TRUE, 'Series VII', 'Naukri', 'https://naukri.com/jobs/1020',
 75, '2024-01-07',
 'NISM Series VII (Securities Operations and Risk Management) mandatory. Execute equity trades on NSE/BSE. Experience with trading terminals (ODIN/NOW) preferred.'),

('Kotak Securities',
 'Risk Analyst – Market Risk', '₹9L–₹14L PA', 900000, 1400000,
 'Mumbai, Maharashtra', 'Mumbai', '3–5 years', 3, 5,
 TRUE, 'Series VIII', 'LinkedIn', 'https://linkedin.com/jobs/1021',
 80, '2024-01-15',
 'NISM Series VIII valued. Assess VaR, stress-testing, and scenario analysis for equity derivative portfolios. FRM / CQF certification a strong plus.'),

-- ── Nippon India MF ────────────────────────────────────────
('Nippon India Mutual Fund',
 'Regional Sales Manager', '₹10L–₹16L PA', 1000000, 1600000,
 'Mumbai, Maharashtra', 'Mumbai', '5–8 years', 5, 8,
 TRUE, 'Series V-A', 'LinkedIn', 'https://linkedin.com/jobs/1022',
 84, '2024-01-10',
 'NISM Series V-A mandatory. Lead a team of 6 sales officers across Maharashtra. Drive AUM growth through IFA, National Distributor, and direct channels.'),

('Nippon India Mutual Fund',
 'Investment Operations Analyst', '₹5L–₹8L PA', 500000, 800000,
 'Pune, Maharashtra', 'Pune', '2–4 years', 2, 4,
 TRUE, 'Series VII', 'Naukri', 'https://naukri.com/jobs/1023',
 72, '2024-01-11',
 'NISM Series VII required for operations role covering NAV computation, fund accounting, and SEBI MF reporting. Experience with Finacle or similar fund accounting systems preferred.'),

-- ── Paytm Money ────────────────────────────────────────────
('Paytm Money',
 'Product Analyst – Stocks & MF', '₹8L–₹13L PA', 800000, 1300000,
 'Bangalore, Karnataka', 'Bangalore', '2–4 years', 2, 4,
 FALSE, NULL, 'LinkedIn', 'https://linkedin.com/jobs/1024',
 48, '2024-01-12',
 'Define product metrics for Paytm Money''s stocks and mutual fund verticals. SQL, Mixpanel, and Amplitude experience required. Understanding of capital markets is a big plus.'),

-- ── Additional high-value jobs across cities ───────────────
('ICICI Securities',
 'Credit Analyst – Structured Products', '₹12L–₹18L PA', 1200000, 1800000,
 'Mumbai, Maharashtra', 'Mumbai', '4–7 years', 4, 7,
 TRUE, 'Series XV', 'LinkedIn', 'https://linkedin.com/jobs/1025',
 76, '2024-01-08',
 'NISM Series XV (Research Analyst) preferred. Evaluate credit ratings and structure debt capital market instruments. CFA / CA qualification strongly preferred.'),

('Motilal Oswal Financial',
 'Fixed Income Dealer', '₹8L–₹13L PA', 800000, 1300000,
 'Mumbai, Maharashtra', 'Mumbai', '3–5 years', 3, 5,
 TRUE, 'Series VII', 'Indeed', 'https://indeed.com/jobs/1026',
 79, '2024-01-14',
 'NISM Series VII required. Execute debt market trades (G-Secs, SDL, corporate bonds). Bloomberg / CCIL / NDS-OM platform experience essential.'),

('HDFC Asset Management',
 'Digital Marketing – MF', '₹5L–₹8L PA', 500000, 800000,
 'Mumbai, Maharashtra', 'Mumbai', '2–4 years', 2, 4,
 FALSE, NULL, 'LinkedIn', 'https://linkedin.com/jobs/1027',
 40, '2024-01-09',
 'Drive digital campaigns for HDFC MF investor education and AUM growth. Google Ads, Meta Ads, SEO experience required. Finance knowledge a plus.'),

('Angel One',
 'Algorithmic Trading Analyst', '₹12L–₹20L PA', 1200000, 2000000,
 'Mumbai, Maharashtra', 'Mumbai', '3–5 years', 3, 5,
 TRUE, 'Series VIII', 'LinkedIn', 'https://linkedin.com/jobs/1028',
 82, '2024-01-15',
 'NISM Series VIII preferred. Develop and backtest algorithmic trading strategies on NSE F&O. Python, pandas, zipline experience essential.'),

('Kotak Securities',
 'Relationship Manager – NRI', '₹7L–₹12L PA', 700000, 1200000,
 'Mumbai, Maharashtra', 'Mumbai', '3–6 years', 3, 6,
 TRUE, 'Series X-A', 'Naukri', 'https://naukri.com/jobs/1029',
 81, '2024-01-07',
 'NISM Series X-A certified. Manage NRI client portfolios including PIS accounts, repatriation, and FEMA compliance. Arabic or Gujarati language skills a plus.'),

('Mirae Asset',
 'Quant Analyst – Risk', '₹15L–₹22L PA', 1500000, 2200000,
 'Mumbai, Maharashtra', 'Mumbai', '3–6 years', 3, 6,
 TRUE, 'Series XXI-A', 'LinkedIn', 'https://linkedin.com/jobs/1030',
 85, '2024-01-13',
 'NISM Series XXI-A and FRM preferred. Build factor models and risk attribution frameworks for Mirae equity funds. Python (numpy/scipy/statsmodels) expertise required.'),

-- ── Jobs in non-Mumbai cities ──────────────────────────────
('ICICI Securities',
 'Equity Advisor – Branch', '₹4L–₹7L PA', 400000, 700000,
 'Kolkata, West Bengal', 'Kolkata', '1–3 years', 1, 3,
 TRUE, 'Series VIII', 'Naukri', 'https://naukri.com/jobs/1031',
 77, '2024-01-10',
 'NISM Series VIII required. Service retail equity clients at Kolkata branch. Demat account management and portfolio advisory services.'),

('Nippon India Mutual Fund',
 'Area Sales Executive', '₹4.5L–₹7L PA', 450000, 700000,
 'Hyderabad, Telangana', 'Hyderabad', '1–3 years', 1, 3,
 TRUE, 'Series V-A', 'Naukri', 'https://naukri.com/jobs/1032',
 80, '2024-01-11',
 'NISM Series V-A mandatory. Acquire and retain IFA clients across Hyderabad. SIP drive and STP promotions.'),

('Zerodha',
 'Customer Support – Derivatives', '₹3.5L–₹5.5L PA', 350000, 550000,
 'Bangalore, Karnataka', 'Bangalore', '0–2 years', 0, 2,
 TRUE, 'Series VIII', 'Naukri', 'https://naukri.com/jobs/1033',
 68, '2024-01-12',
 'NISM Series VIII required for options and futures support queries. Resolve client escalations on margin calls, expiry, and corporate actions.'),

('Kotak Securities',
 'Branch Relationship Manager', '₹5L–₹9L PA', 500000, 900000,
 'Ahmedabad, Gujarat', 'Ahmedabad', '2–4 years', 2, 4,
 TRUE, 'Series VII', 'Naukri', 'https://naukri.com/jobs/1034',
 78, '2024-01-13',
 'NISM Series VII or VIII required. Handle HNI walk-in clients at Ahmedabad branch. Cross-sell equity, MF, and insurance products.'),

('Groww',
 'Compliance Manager', '₹10L–₹16L PA', 1000000, 1600000,
 'Bangalore, Karnataka', 'Bangalore', '4–7 years', 4, 7,
 TRUE, 'Series VI', 'LinkedIn', 'https://linkedin.com/jobs/1035',
 74, '2024-01-14',
 'NISM Series VI mandatory. Manage SEBI broker registration compliance, audit support, and PMLA obligations. Experience at a stockbroker or AMC required.'),

('Paytm Money',
 'Compliance Associate – AMFI', '₹4L–₹7L PA', 400000, 700000,
 'Bangalore, Karnataka', 'Bangalore', '1–3 years', 1, 3,
 TRUE, 'Series V-A', 'Naukri', 'https://naukri.com/jobs/1036',
 75, '2024-01-08',
 'NISM Series V-A and AMFI registration required. Ensure mutual fund distribution compliance. Handle IAD filings and SEBI correspondence.'),

('HDFC Asset Management',
 'Institutional Sales – Corporates', '₹12L–₹20L PA', 1200000, 2000000,
 'Delhi, NCR', 'Delhi', '5–8 years', 5, 8,
 TRUE, 'Series V-A', 'LinkedIn', 'https://linkedin.com/jobs/1037',
 86, '2024-01-09',
 'NISM Series V-A required. Drive liquid and short-duration MF solutions to treasury teams of corporates, PSUs, and trusts in North India.'),

('Angel One',
 'Financial Planning Analyst', '₹5L–₹9L PA', 500000, 900000,
 'Pune, Maharashtra', 'Pune', '2–4 years', 2, 4,
 TRUE, 'Series X-A', 'LinkedIn', 'https://linkedin.com/jobs/1038',
 83, '2024-01-15',
 'NISM Series X-A and CFP Level 1 preferred. Prepare comprehensive financial plans covering retirement, education corpus, and insurance needs for retail clients.'),

('Mirae Asset',
 'Equity Research Intern (6 months)', '₹2L–₹3L PA', 200000, 300000,
 'Mumbai, Maharashtra', 'Mumbai', 'Fresher', 0, 1,
 FALSE, NULL, 'LinkedIn', 'https://linkedin.com/jobs/1039',
 35, '2024-01-16',
 '6-month research internship. Final year or recent CFA/MBA Finance graduates. Work alongside senior analysts on sector research notes. NISM certification appreciated but not required.'),

('Motilal Oswal Financial',
 'Certified Financial Planner – Mass Affluent', '₹8L–₹13L PA', 800000, 1300000,
 'Bangalore, Karnataka', 'Bangalore', '3–5 years', 3, 5,
 TRUE, 'Series X-A', 'LinkedIn', 'https://linkedin.com/jobs/1040',
 87, '2024-01-10',
 'NISM Series X-A + CFP mandatory. Service 200+ mass-affluent clients with AUM ₹10L–₹50L. Annual review meetings, goal tracking, and rebalancing advisory.'),

-- ── Final 10 jobs ──────────────────────────────────────────
('Nippon India Mutual Fund',
 'Training Manager – IFA Education', '₹8L–₹12L PA', 800000, 1200000,
 'Mumbai, Maharashtra', 'Mumbai', '4–7 years', 4, 7,
 TRUE, 'Series V-A', 'Naukri', 'https://naukri.com/jobs/1041',
 76, '2024-01-11',
 'NISM Series V-A required. Design and deliver training programmes for 5,000+ IFAs across India. Excellent communication and content creation skills needed.'),

('ICICI Securities',
 'Options Strategist', '₹18L–₹28L PA', 1800000, 2800000,
 'Mumbai, Maharashtra', 'Mumbai', '5–8 years', 5, 8,
 TRUE, 'Series VIII', 'LinkedIn', 'https://linkedin.com/jobs/1042',
 91, '2024-01-07',
 'NISM Series VIII mandatory. Design and execute complex multi-leg options strategies for HNI and institutional clients. Experience with SPAN margining and implied volatility surface required.'),

('Zerodha',
 'Financial Content Writer – NISM Topics', '₹5L–₹8L PA', 500000, 800000,
 'Bangalore, Karnataka', 'Bangalore', '1–3 years', 1, 3,
 TRUE, 'Series V-A', 'LinkedIn', 'https://linkedin.com/jobs/1043',
 70, '2024-01-13',
 'NISM Series V-A or VIII preferred. Create investor education content on Zerodha Varsity — articles, videos, quizzes on mutual funds, equity investing, and financial planning.'),

('Kotak Securities',
 'Treasury Dealer – Forex', '₹9L–₹15L PA', 900000, 1500000,
 'Mumbai, Maharashtra', 'Mumbai', '3–5 years', 3, 5,
 TRUE, 'Series VII', 'Indeed', 'https://indeed.com/jobs/1044',
 77, '2024-01-14',
 'NISM Series VII required. Execute forex (USD/INR, cross-currency) and interest rate derivative trades. RBI / FEMA regulatory knowledge essential.'),

('Angel One',
 'Regional Head – South India', '₹20L–₹30L PA', 2000000, 3000000,
 'Chennai, Tamil Nadu', 'Chennai', '8–12 years', 8, 12,
 TRUE, 'Series VII', 'LinkedIn', 'https://linkedin.com/jobs/1045',
 88, '2024-01-05',
 'NISM Series VII mandatory. Lead Angel One''s Southern Region P&L. Manage 50+ branches, 500+ advisors, and ₹5,000Cr+ AUM target. MBA Finance / CA preferred.'),

('Groww',
 'iOS Developer – Investments', '₹18L–₹26L PA', 1800000, 2600000,
 'Bangalore, Karnataka', 'Bangalore', '3–5 years', 3, 5,
 FALSE, NULL, 'LinkedIn', 'https://linkedin.com/jobs/1046',
 28, '2024-01-11',
 'Build Groww iOS app features for mutual fund and stock investments. Swift, UIKit, Combine required. Finance domain knowledge appreciated.'),

('Mirae Asset',
 'FX & Rates Strategy Analyst', '₹10L–₹16L PA', 1000000, 1600000,
 'Mumbai, Maharashtra', 'Mumbai', '3–5 years', 3, 5,
 TRUE, 'Series VIII', 'Naukri', 'https://naukri.com/jobs/1047',
 79, '2024-01-12',
 'NISM Series VIII preferred. Publish daily/weekly FX and rates strategy reports for institutional clients. Bloomberg, REFINITIV experience essential.'),

('Motilal Oswal Financial',
 'Wealth Relationship Manager – Tier 2 Cities', '₹6L–₹10L PA', 600000, 1000000,
 'Nagpur, Maharashtra', 'Nagpur', '2–4 years', 2, 4,
 TRUE, 'Series X-A', 'Naukri', 'https://naukri.com/jobs/1048',
 82, '2024-01-09',
 'NISM Series X-A required. Acquire and manage HNI clients in Nagpur. Drive equity, MF, and PMS products. Excellent growth opportunity in an underserved market.'),

('Nippon India Mutual Fund',
 'Digital Transformation Lead – MF', '₹15L–₹22L PA', 1500000, 2200000,
 'Mumbai, Maharashtra', 'Mumbai', '6–10 years', 6, 10,
 FALSE, NULL, 'LinkedIn', 'https://linkedin.com/jobs/1049',
 42, '2024-01-06',
 'Lead digital channels strategy for Nippon MF (website, app, robo-advisory). Product + technology background required. NISM awareness helpful.'),

('Paytm Money',
 'Head of Compliance – Broking', '₹22L–₹32L PA', 2200000, 3200000,
 'Bangalore, Karnataka', 'Bangalore', '8–12 years', 8, 12,
 TRUE, 'Series VI', 'LinkedIn', 'https://linkedin.com/jobs/1050',
 83, '2024-01-08',
 'NISM Series VI mandatory. Own SEBI broker + DP compliance for Paytm Money. Lead audit responses, PMLA, and regulatory reporting. CS / LLB with SEBI / exchange experience preferred.');


-- ────────────────────────────────────────────────────────────────
-- WEEKLY STATS  (3 weeks of history)
-- ────────────────────────────────────────────────────────────────
INSERT INTO weekly_stats
    (week_start, total_jobs, new_jobs_this_week, total_companies,
     nism_required_jobs, avg_relevance_score,
     top_city, top_position, top_source, high_score_jobs)
VALUES
('2023-12-25', 28, 28, 8, 22, 73.50, 'Mumbai', 'Mutual Fund Advisor', 'LinkedIn', 14),
('2024-01-01', 38, 10, 9, 30, 74.20, 'Mumbai', 'Research Analyst',    'Naukri',  18),
('2024-01-08', 50, 12, 10, 38, 75.10, 'Mumbai', 'Wealth Advisor',      'LinkedIn', 22);


-- ────────────────────────────────────────────────────────────────
-- SAMPLE SCRAPE LOGS
-- ────────────────────────────────────────────────────────────────
INSERT INTO scrape_logs
    (run_id, source, jobs_found, jobs_inserted, jobs_skipped, status, started_at, finished_at)
VALUES
('run-001', 'LinkedIn', 20, 18, 2, 'success', '2024-01-08 08:01:00', '2024-01-08 08:04:30'),
('run-001', 'Naukri',   18, 17, 1, 'success', '2024-01-08 08:05:00', '2024-01-08 08:08:15'),
('run-001', 'Indeed',   15, 15, 0, 'success', '2024-01-08 08:09:00', '2024-01-08 08:11:45');


-- ────────────────────────────────────────────────────────────────
-- VERIFY ROW COUNTS
-- ────────────────────────────────────────────────────────────────
SELECT 'companies'         AS tbl, COUNT(*) AS rows FROM companies   UNION ALL
SELECT 'jobs',                      COUNT(*)         FROM jobs        UNION ALL
SELECT 'weekly_stats',              COUNT(*)         FROM weekly_stats UNION ALL
SELECT 'scrape_logs',               COUNT(*)         FROM scrape_logs;
