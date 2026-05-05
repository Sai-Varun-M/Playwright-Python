# 🎭 Playwright Python Test Framework

> Production-grade end-to-end test automation framework using **Python + Playwright + pytest** with a CI/CD pipeline and an interactive reporting dashboard.

---

## ✨ Features

| Feature | Details |
|---|---|
| **Framework** | Playwright for Python + pytest |
| **Design Pattern** | Page Object Model (POM) |
| **Test Suites** | Smoke · E2E (login, navigation, forms) · API |
| **Browsers** | Chromium · Firefox · WebKit (Safari) |
| **CI Pipeline** | GitHub Actions with smoke gate → multi-browser matrix |
| **Reporting** | pytest-html + JSON output + custom dashboard |
| **Dashboard** | Dark-mode HTML dashboard with Chart.js |

---

## 📁 Project Structure

```
playwright-framework/
├── .github/workflows/playwright.yml  # CI pipeline
├── pages/                            # Page Object Models
│   ├── base_page.py
│   ├── home_page.py
│   ├── login_page.py
│   └── form_page.py
├── tests/
│   ├── smoke/test_smoke.py           # Fast sanity suite
│   ├── e2e/test_login.py             # Auth flows
│   ├── e2e/test_navigation.py        # Link traversal
│   ├── e2e/test_forms.py             # Form interactions
│   └── api/test_api.py               # REST API tests
├── utils/
│   ├── helpers.py                    # Shared utilities
│   └── test_data.py                  # Static test data
├── scripts/generate_report.py        # Merges JSON → dashboard
├── dashboard/                        # HTML reporting dashboard
│   ├── index.html
│   ├── dashboard.css
│   └── dashboard.js
├── conftest.py                       # Fixtures & hooks
├── pytest.ini                        # pytest config
└── requirements.txt
```

---

## 🚀 Quick Start

### 1. Create & activate a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
```

### 2. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 3. Install Playwright browsers
```bash
playwright install --with-deps
```

### 4. (Optional) Copy environment config
```bash
cp .env.example .env
```

---

## 🧪 Running Tests

| Command | Description |
|---|---|
| `pytest` | Run the full test suite |
| `pytest tests/smoke/` | Smoke tests only |
| `pytest tests/e2e/` | All E2E tests |
| `pytest tests/api/` | API tests only |
| `pytest -m login` | Tests tagged `@login` |
| `pytest --browser firefox` | Run with Firefox |
| `pytest --headed` | Run with browser visible |
| `pytest --browser chromium --browser firefox` | Multi-browser |
| `pytest -n 4` | Parallel execution (4 workers) |

---

## 📊 Reporting

### View the built-in pytest-html report
```bash
# After running tests:
open playwright-report/report.html
```

### Open the custom dashboard
```bash
python scripts/generate_report.py
open dashboard/index.html
```

The dashboard shows:
- ✅ Pass / ❌ Fail / ⏭️ Skip KPIs with animated counters
- 🍩 Pass rate donut chart
- 📊 Results breakdown by suite and browser
- ⏱️ Top 20 slowest tests bar chart
- 🔍 Filterable & searchable test results table with failure details modal

---

## 🔄 CI Pipeline

The GitHub Actions workflow (`.github/workflows/playwright.yml`) runs on every push/PR to `main` or `develop`:

```
push / pull_request
       │
       ▼
  🔥 Smoke Tests  ──── (gates the full suite)
       │
  ┌────┴────────────────────┐
  ▼                         ▼
🧪 E2E (Chromium)     🌐 API Tests
🧪 E2E (Firefox)
🧪 E2E (WebKit)
  │
  └────────────────────────┐
                           ▼
                    📊 Generate Dashboard
                    (upload as artifact)
```

You can also trigger the pipeline manually and choose which suite to run via `workflow_dispatch`.

---

## 🏷️ Test Markers

Add markers to your tests to categorise them:

```python
@pytest.mark.smoke      # Quick sanity checks
@pytest.mark.e2e        # Full user flows
@pytest.mark.api        # API tests
@pytest.mark.login      # Login-related
@pytest.mark.navigation # Navigation tests
@pytest.mark.forms      # Form interaction tests
```

---

## 🔧 Configuration

Edit `pytest.ini` to adjust reporters, log level, or add new markers.

Edit `conftest.py` to add new fixtures or modify the base URL.

Set `BASE_URL` in your `.env` to point the framework at a different target application.

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `playwright` | Browser automation |
| `pytest-playwright` | pytest integration |
| `pytest-html` | HTML test reports |
| `pytest-json-report` | JSON output for dashboard |
| `pytest-xdist` | Parallel test execution |
| `python-dotenv` | Environment variable loading |
| `faker` | Random test data generation |
