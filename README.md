# 🛡️ VulnWatch: Defensive Vulnerability Intelligence & Web Scraping Platform

[![Python Version](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-Flask%203.0-lightgrey.svg)](https://flask.palletsprojects.com/)
[![Database](https://img.shields.io/badge/Database-SQLite%20(WAL%20Mode)-green.svg)](https://www.sqlite.org/)
[![Machine Learning](https://img.shields.io/badge/ML-Scikit--Learn%20(74.5%25%20Acc)-orange.svg)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-19%2F19%20Passing-brightgreen.svg)]()
[![Offline First](https://img.shields.io/badge/Architecture-Offline--First%20(Air--Gap)-success.svg)]()

> **VulnWatch** is an offline-first defensive threat intelligence platform and automated web-scraping dashboard. It is engineered to ingest, parse, and normalize massive vulnerability datasets (>290,000 advisories), scrape real-time security disclosures directly from web pages, track granular field-level mutations (web diffing), and classify threat weaknesses using an offline Supervised Natural Language Processing (NLP) model.

---

## 📌 Table of Contents
1. [Screenshots](#-screenshots)
2. [Core Features](#-core-features)
3. [Why VulnWatch?](#-why-vulnwatch-the-web-scraping--security-problem)
4. [System Architecture & Data Flow](#-system-architecture--data-flow)
5. [Platform Statistics & Metrics](#-real-platform-statistics--metrics)
6. [Machine Learning Performance](#-machine-learning-performance-cwe-classifier)
7. [Technology Stack](#-technology-stack)
8. [Project Structure](#-project-structure)
9. [Installation & Quick Start](#-installation--quick-start-windows-powershell)
10. [Usage & Dashboard Tour](#-usage--dashboard-tour)
11. [Running Automated Tests](#-running-automated-tests)
12. [Security & Defensive Hardening](#-security--defensive-hardening)
13. [Troubleshooting](#-troubleshooting)
14. [Author](#-author)

---

## 🖼️ Screenshots

### Executive Dashboard
![VulnWatch Dashboard](docs/screenshots/dashboard.png)

### Recently Observed Vulnerabilities
![Recent Vulnerabilities](docs/screenshots/recent-vulnerabilities.png)

### Running Locally (`python app.py`)
![Terminal Output](docs/screenshots/terminal-run.png)

---

## ✨ Core Features

- 🕷️ **Web Scraping & Entity Extraction**:
  - Live HTML web scraper (`services/web_scraper.py`) that crawls live security advisory listings (GitHub Security Advisory Database) without requiring paid APIs.
  - Named Entity Recognition (NER) regex engines that mine CVE IDs (`CVE-YYYY-NNNN`), GHSA IDs, and affected software package names from unstructured scraped web text.
- ⚡ **High-Throughput Chunked Ingestion**:
  - Streams and indexes massive datasets (>100 MB, 280k+ rows) in safe transactions of **5,000 records per batch** with automatic database rollback protection.
- 🔍 **Granular Web Diffing & Change History**:
  - Detects field-level mutations across 5 key attributes: `severity`, `cvss_score`, `affected_product`, `description`, and `last_modified`.
  - Zero false-positive diff engine: normalizes whitespace, canonicalizes floats (`7` vs `7.0`), and canonicalizes multi-value product sets.
- 🛑 **Baseline Ingestion Rule (Alert Flood Suppression)**:
  - First-time baseline loads tag records as `Baseline` and generate a single summary notification, preventing a flood of 280,000 individual alerts.
- 🤖 **Offline Supervised ML Classifier**:
  - Pre-trained TF-IDF + Multi-class Logistic Regression pipeline that predicts the most probable Common Weakness Enumeration (CWE) class from raw vulnerability descriptions with **74.49% accuracy** across 30 distinct classes.
- 📊 **100% Offline Visualizations (Air-Gap Ready)**:
  - Vendored local Chart.js (v4.4.1) and system fonts for zero CDN reliance, rendering interactive severity doughnuts and publication timeline trends offline.
- 🔒 **Defensive Web Hardening**:
  - CSRF protection across all forms and AJAX endpoints via `Flask-WTF`, strict Content Security Policy (CSP), clickjacking prevention (`X-Frame-Options: DENY`), and parameterised SQL injection defenses.

---

## 🎯 Why VulnWatch? (The Web Scraping & Security Problem)

1. **Mutation Blindness in Threat Intel**: Security advisories are rarely static. When vendors escalate a vulnerability's severity or discover new affected software packages, conventional databases overwrite the old record, destroying the evolutionary audit trail. VulnWatch logs every mutation in `change_history`.
2. **Handling Raw, Unstructured Web-Scraped Feeds**: Threat data scraped from forums or GitHub advisories often arrives with messy HTML whitespace (`forghost(npm)`), missing columns, and mixed date formats. VulnWatch's normalizers automatically clean and standardize incoming feeds.
3. **Air-Gap Operational Requirements**: Defense networks and corporate SOCs often operate in air-gapped environments without internet access. VulnWatch works 100% offline by default, only reaching out to the web when explicitly requested by the analyst.

---

## 🏗️ System Architecture & Data Flow

```
[ Ingestion Sources ]
  ├── data/*.csv (Static Scraped Datasets)
  ├── Web Uploads (Multi-format CSV)
  └── Live Web Scraper (services/web_scraper.py)
            │
            ▼
   [ services/dataset_importer.py ] ──► Chunked Streaming (5k rows/transaction)
            │
            ▼
   [ services/normalizers.py ] ──────► Regex Entity Extraction & Casing Normalization
            │
            ▼
   [ services/change_detector.py ] ──► Compares: Severity, CVSS, Products, Desc, Date
            │
            ├─────────────────────────────────────────┐
            ▼                                         ▼
   [ SQLite: instance/app.db ]             [ services/notification_service.py ]
     - vulnerabilities (Catalog)               - Deduplicated Alert Queue
     - vulnerability_products (CPE)            - Severity Escalation Warnings
     - change_history (Granular Diffs)         - Baseline Flood Suppression
     - import_history & errors
            │
            ▼
   [ services/vulnerability_service.py ] ◄─── [ services/ml_service.py ]
     - Parameterised Search & Facets            - Offline Scikit-Learn NLP Pipeline
     - Aggregated Stats & Analytics             - 30-Class CWE Predictor
            │
            ▼
   [ Presentation Layer (Flask + Jinja2) ]
     ├── Responsive WCAG AA Dark Cybersecurity Theme
     ├── Offline Vendored Chart.js Visualizations
     └── Browser Local Timezone Client Utilities
```

---

## 📈 Real Platform Statistics & Metrics

The following metrics reflect the actual populated state of the database and verified system runs:

| Metric | Verified Value | Description |
|---|---|---|
| **Total Ingested Vulnerabilities** | **293,086** | Unified catalog of CVE and GHSA advisories |
| **Normalized Software Products** | **4,672** | Distinct packages indexed in `vulnerability_products` |
| **Observed Field Mutations** | **11,020** | Audit records stored in `change_history` |
| **Deduplicated Security Alerts** | **11,242** | Notifications created in `notifications` |
| **Baseline Dataset Ingestion** | **280,694 rows** | Ingested from `data/CVE_CWE_2025.csv` (~88s) |
| **Scraped Web Feed Ingestion** | **3,350 rows** | Ingested from `data/Security Vulnerabilities.csv` |
| **Automated Test Suite** | **19 / 19 Passed** | Pytest unit and integration tests |

### Severity Breakdown Across Catalog (at the time of the README run)
- **Critical (CVSS 9.0 - 10.0)**: 30,183 (10.3%)
- **High (CVSS 7.0 - 8.9)**: 116,776 (39.8%)
- **Medium / Moderate (CVSS 4.0 - 6.9)**: 132,664 (45.3%)
- **Low (CVSS 0.1 - 3.9)**: 10,763 (3.7%)
- **Unknown / Unavailable**: 2,673 (0.9%)
- **None (CVSS 0.0)**: 27 (<0.1%)

---

## 🧠 Machine Learning Performance (CWE Classifier)

VulnWatch incorporates an offline supervised machine learning model that classifies natural language vulnerability descriptions into Common Weakness Enumeration (CWE) categories.

- **Pipeline Architecture**: Scikit-Learn `Pipeline` combining sublinear `TfidfVectorizer` (15,000 word n-grams: 1-2) with a multi-class `LogisticRegression` (SAGA solver).
- **Data Hygiene**: Exact-duplicate descriptions and empty strings were eliminated prior to vectorization to guarantee zero data leakage. The TF-IDF matrix was fitted strictly on the training partition.
- **Sample Distribution**: 95,197 samples across 30 real-world CWE classes (80% train / 20% test stratified split).
- **Overall Model Accuracy**: **`74.49%`**

### Sample Class Evaluation (`models/metrics.json`):
| CWE Identifier | Weakness Name | Precision | Recall | F1-Score |
|---|---|---|---|---|
| **CWE-89** | SQL Injection | 95.5% | 94.6% | **95.0%** |
| **CWE-79** | Cross-Site Scripting (XSS) | 89.4% | 93.9% | **91.6%** |
| **CWE-22** | Path Traversal | 87.8% | 88.5% | **88.1%** |
| **CWE-78** | OS Command Injection | 86.8% | 86.1% | **86.4%** |
| **CWE-352** | Cross-Site Request Forgery (CSRF) | 88.2% | 89.0% | **88.6%** |

*Note: In compliance with defensive AI ethics, every prediction rendered in the UI includes the disclaimer: `"Model-generated prediction, not verified"`.*

---

## 💻 Technology Stack

- **Backend**: Python 3.11, Flask 3.0.3, Werkzeug 3.1.9, Flask-WTF 1.2.1
- **Database**: SQLite 3 with Foreign Key constraints and Write-Ahead Logging (`WAL` mode)
- **Data Processing**: Pandas 2.2.2, Requests 2.32.3
- **Machine Learning**: Scikit-Learn 1.5.0, Joblib 1.4.2
- **Testing**: Pytest 8.2.2
- **Frontend**: Jinja2, Vanilla CSS (Dark Theme), Vanilla JavaScript (ES6)
- **Charts**: Chart.js v4.4.1 (Locally vendored, zero external CDN)

---

## 📁 Project Structure

```text
VulnWatch/
├── app.py                  # Flask application factory, routes, security headers
├── config.py               # Environment-driven configuration
├── db.py                   # SQLite connection helper (WAL, foreign keys)
├── requirements.txt        # Runtime dependencies
├── requirements-dev.txt    # Development / test dependencies (pytest)
├── .env.example            # Sample environment variables
├── data/                   # Datasets (CSV)
├── database/               # schema.sql
├── docs/                   # Documentation and screenshots
├── instance/               # Runtime DB, logs, uploads (git-ignored)
├── models/                 # Trained CWE classifier + metrics.json
├── scripts/                # init_db.py, import_dataset.py
├── services/
│   ├── change_detector.py
│   ├── dataset_importer.py
│   ├── ml_service.py
│   ├── normalizers.py
│   ├── notification_service.py
│   ├── nvd_client.py
│   ├── refresh_service.py
│   ├── vulnerability_service.py
│   └── web_scraper.py
├── static/
│   ├── css/style.css
│   └── js/ (common.js, dashboard.js, vendor/chart.umd.js)
├── templates/              # Jinja2 pages (dashboard, history, import, ML, alerts...)
└── tests/                  # pytest suite (19 tests)
```

---

## 🚀 Installation & Quick Start (Windows PowerShell)

### 1. Clone the Repository
```powershell
git clone https://github.com/<your-username>/VulnWatch.git
cd VulnWatch
```

### 2. Set Up Virtual Environment
```powershell
# If script execution is restricted on Windows:
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```powershell
pip install -r requirements.txt -r requirements-dev.txt
```

### 4. Configure Environment
```powershell
Copy-Item .env.example .env
```
*(Optional)* You can set `NVD_API_KEY=your_key_here` in `.env` for higher rate limits during live synchronizations.

### 5. Initialize Database & Ingest Datasets
```powershell
# Initialize SQLite database schema
python scripts/init_db.py

# Ingest primary baseline dataset
python scripts/import_dataset.py --file data/CVE_CWE_2025.csv

# (Optional) Ingest additional web-scraped dataset
python scripts/import_dataset.py --file "data/Security Vulnerabilities.csv"
```

### 6. Run the Application
```powershell
python app.py
```
Open your browser and navigate to: **`http://127.0.0.1:5000`**

---

## 🖥️ Usage & Dashboard Tour

| View | Route | Description |
|---|---|---|
| **Executive Dashboard** | `/` | Total advisories, Critical/High counts, 30-day newly detected vs updated cards, severity doughnut, and timeline bar charts. |
| **Vulnerability Explorer** | `/vulnerabilities` | Parameterized search across CVEs, titles, and descriptions with multi-facet filters (severity, product, date, sorting). |
| **Advisory Details** | `/vulnerabilities/<id>` | Full vulnerability description, CVSS metrics, product mappings, and item-specific mutation audit trail. |
| **Change History Log** | `/history` | Platform-wide audit trail displaying the latest 100 field modifications (Old vs New values, detection vs source timestamps). |
| **Dataset Ingestion Hub** | `/import` | Ingest datasets via file upload (max 150 MB) or from the local `data/` directory, complete with error logs. |
| **Live Sync & Web Scraper** | `/status` | Monitor data freshness, view previous sync runs, and trigger the live web scraper / NVD synchronizer. |
| **Security Alerts** | `/notifications` | Deduplicated alert queue for Critical/High threat disclosures and severity escalations. |
| **ML Weakness Classifier** | `/ml` | Input raw vulnerability text to predict the most probable CWE category using the local NLP model. |

---

## 🧪 Running Automated Tests

VulnWatch includes a comprehensive test suite covering normalizers, change detection idempotency, chunked importer error handling, NVD mock client backoff, security headers, and route responses.

```powershell
# Run the full pytest suite
python -m pytest -v
```

Output:
```text
============================= test session starts =============================
collected 19 items

tests/test_change_detector.py::test_baseline_and_new_records PASSED      [  5%]
tests/test_change_detector.py::test_idempotent_reimport_produces_zero_history PASSED [ 10%]
tests/test_change_detector.py::test_mutation_creates_history_record PASSED [ 15%]
tests/test_importer.py::test_importer_valid_and_duplicate PASSED         [ 21%]
tests/test_importer.py::test_importer_rejected_row_logged PASSED         [ 26%]
tests/test_normalizers.py::test_normalize_cve_id PASSED                  [ 31%]
tests/test_normalizers.py::test_normalize_severity PASSED                [ 36%]
tests/test_normalizers.py::test_normalize_cvss_score PASSED              [ 42%]
tests/test_normalizers.py::test_normalize_date PASSED                    [ 47%]
tests/test_normalizers.py::test_derive_published_date PASSED             [ 52%]
tests/test_normalizers.py::test_normalize_whitespace PASSED              [ 57%]
tests/test_normalizers.py::test_split_products PASSED                    [ 63%]
tests/test_nvd_client.py::test_host_allowlist_validation PASSED          [ 68%]
tests/test_nvd_client.py::test_mocked_successful_fetch PASSED            [ 73%]
tests/test_nvd_client.py::test_mocked_timeout_handling PASSED            [ 78%]
tests/test_routes.py::test_routes_empty_db_return_200 PASSED             [ 84%]
tests/test_routes.py::test_security_headers_present PASSED               [ 89%]
tests/test_routes.py::test_not_found_returns_404 PASSED                  [ 94%]
tests/test_routes.py::test_search_and_filter_api PASSED                  [100%]

============================= 19 passed in ~22s ===============================
```

---

## 🛡️ Security & Defensive Hardening

- **Strictly Defensive Scope**: The system contains no offensive exploit code, scanners, or denial-of-service tools.
- **CSRF Token Verification**: Universal CSRF validation on all state-changing endpoints via `Flask-WTF`.
- **Hardened HTTP Response Headers**:
  - `Content-Security-Policy`: Restricted strictly to `'self'` for scripts, fonts, and assets.
  - `X-Frame-Options: DENY`: Complete protection against clickjacking.
  - `X-Content-Type-Options: nosniff`: Prevents MIME-type confusion attacks.
  - `Referrer-Policy: strict-origin-when-cross-origin`: Mitigates referrer leakage.
- **SQL Injection Defenses**: All database queries use parameterized SQL with escaped wildcards (`%` and `_`).
- **Safe External Links**: Links only render if using `http://` or `https://` with `rel="noopener noreferrer"` and `target="_blank"`. Untrusted protocols (`javascript:`) are rendered as inert text.

---

## ❓ Troubleshooting

### 1. PowerShell Script Execution Error
```text
File ...\Activate.ps1 cannot be loaded because running scripts is disabled on this system.
```
**Fix**: Open PowerShell and run:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

### 2. Database Locked Error
If a database locked error appears during concurrent testing:
```text
sqlite3.OperationalError: database is locked
```
**Fix**: VulnWatch already enables `PRAGMA journal_mode = WAL;`. Ensure background batch scripts have finished before attempting manual SQLite edits.

### 3. Port 5000 Already in Use
**Fix**: Specify a custom port when launching the application:
```powershell
flask run --port 5001
```

---

## 📄 License
This project is developed as an academic capstone and is released under the [MIT License](LICENSE).
