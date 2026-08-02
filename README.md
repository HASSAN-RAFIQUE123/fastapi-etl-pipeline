# API Generator and API ETL

This project is a small but realistic example of a data-driven web application. It combines a FastAPI backend, a SQLite database, a simple dashboard, and an ETL workflow so that raw API data can be transformed into cleaner analytical datasets.

## Overview

The application is designed to demonstrate how to:
- build a REST API with FastAPI
- model business data with SQLAlchemy
- seed large volumes of dummy data
- expose that data through JSON endpoints
- serve a browser-based dashboard
- run an extract, transform, and load workflow with notebooks

## Main features

- Health and database checks via the /health and /tables endpoints
- Dummy data generation through /seed/dummy-data
- REST endpoints for customers, products, orders, feedback, and sentiments
- A simple interactive dashboard at the root URL
- ETL notebooks for extracting data from the API and loading cleaned results into SQLite
- Regression tests covering the core seeding and retrieval flow

## Project structure

```text
app/
  config.py              # Application configuration and environment settings
  db.py                  # SQLAlchemy models and database helpers
  main.py                # FastAPI app and route definitions
ETL/
  extract.ipynb          # Pulls API data into staging files
  transform.ipynb        # Cleans and enriches the data
  load.ipynb             # Loads transformed data into SQLite
dummy_data_generator/
  generate_dummy_data.py # Generates the seeded business records
templates/
  index.html             # Browser dashboard UI
requirements.txt        # Python dependencies
app/api_generator.py    # Helper to inspect the registered API routes
run.sh                  # Convenience script to run the app locally
tests/
  test_api.py            # Regression tests for the API
```

## Technology stack

- Python 3.10+
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- pytest
- Jupyter notebooks for ETL steps

## Prerequisites

Make sure Python 3.10 or newer is available on your machine.

## Setup

1. Create and activate a virtual environment:

```bash
cd /Users/hassan/Projects/mydatabase-fastapi-api
python3 -m venv .venv
source .venv/bin/activate
```

2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. If you want to run the ETL notebooks, also install notebook-related packages:

```bash
pip install pandas requests nbformat jupyter
```

4. Start the application:

```bash
./run.sh
```

Or run it directly:

```bash
uvicorn app.main:app --reload
```

5. Open the app in a browser:

```text
http://127.0.0.1:8000/
```

The FastAPI Swagger UI is also available at:

```text
http://127.0.0.1:8000/docs
```

## API endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| GET | / | Serves the dashboard HTML page |
| GET | /health | Checks that the app and database are reachable |
| GET | /tables | Lists the available database tables |
| POST | /seed/dummy-data | Seeds the database with dummy records |
| GET | /customers | Returns customer records |
| GET | /products | Returns product records |
| GET | /orders | Returns order records |
| GET | /feedback | Returns feedback records |
| GET | /sentiments | Returns sentiment records |
| GET | /analytics/feedback-summary | Returns a small feedback analytics summary |
| POST | /query | Executes a raw SQL query |

## Data model

The database includes these main entities:
- Customer
- Product
- Payment
- Order
- Feedback
- Sentiment

These are defined in [app/db.py](app/db.py) and are created automatically when the app starts.

## ETL workflow

The ETL flow is split into three notebooks:
- [ETL/extract.ipynb](ETL/extract.ipynb): pulls data from the API endpoints into staging files
- [ETL/transform.ipynb](ETL/transform.ipynb): cleans and enriches the raw data and computes simple KPIs
- [ETL/load.ipynb](ETL/load.ipynb): loads the cleaned results into a SQLite database

Suggested workflow:
1. Start the FastAPI server.
2. Run the cells in [ETL/extract.ipynb](ETL/extract.ipynb).
3. Run the cells in [ETL/transform.ipynb](ETL/transform.ipynb).
4. Run the cells in [ETL/load.ipynb](ETL/load.ipynb).

## Testing

Run the regression tests with:

```bash
pytest -q
```

## Configuration

Configuration values are loaded from [app/config.py](app/config.py). The default database URL is:

```text
sqlite:///./app.db
```

You can override it with the DATABASE_URL environment variable if you want to use a different database.

## Notes

- The project uses SQLite by default for simplicity and local development.
- The root dashboard lets you seed data and browse records directly in the browser.
- The app is intentionally lightweight so it can be used as a teaching example or a starting point for a larger product.
