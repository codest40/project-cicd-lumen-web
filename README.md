
# 1. Project Overview

# Project Name:

Lumen Web – Random Jokes & Celebrity Search API with CI/CD and Monitoring


# Short Description:

Lumen Web is a lightweight Flask-based web API that delivers random jokes and provides celebrity name search functionality. The project demonstrates modern DevOps and backend best practices including:

Async API design with Python + Flask

Containerized deployment with Docker

Multi-service orchestration for monitoring using Prometheus and Grafana

Automated CI/CD deployment on Render using GitHub Actions

Optional PostgreSQL database integration for visitors and health logging


It serves as a practical example for developers and DevOps engineers to learn full-stack backend development, observability, and automated deployment pipelines.


---

# Key Features

1. Random Jokes API

Serves a random joke from a local JSON dataset (jokes.json).

Async design ensures non-blocking operations for high concurrency.



2. Celebrity Name Search

Searches celebrity names from names.json.

Supports case-insensitive and partial matches.

Returns structured JSON responses indicating search results.



3. Visitors & Health Reports (CRUD)

PostgreSQL-backed async endpoints to log visitors and app health reports.

Provides GET, POST, and DELETE operations.

Database is initialized automatically via init_db.py.



4. Monitoring & Observability

Prometheus collects API metrics.

Grafana visualizes response times, API requests, and health logs.



5. Automated CI/CD

GitHub Actions pipeline builds, tests, and deploys the app automatically.

Deploys to Render using API triggers and sends success or failure Notification mails.

Supports skipping deployments via commit messages and skipping entirely if only README.md file is updated



6. Dockerized Architecture

Runs locally or in production using containers.

Multi-service setup allows separation of app, monitoring, and database services.





---

# Use Case / Purpose

Lumen Web is designed to:

Provide a learning platform for DevOps practices like automated CI/CD, monitoring, and container orchestration.

Serve as a template for deploying lightweight Flask APIs with modern DevOps workflows.

Demonstrate asynchronous Python API design and integration with external monitoring tools.

Showcase differences between local Docker Compose orchestration and production deployment on Render, highlighting PaaS-specific behaviors.



# 2. Architecture & System Design

High-Level Architecture

Lumen Web is designed as a modular, containerized, and observability-enabled Flask application. Its architecture separates concerns across application logic, database, and monitoring services.

+----------------+
                |    User/API    |
                +--------+-------+
                         |
                         v
                 +-------+-------+
                 |   Flask App    |
                 | (lumen_web/)   |
                 | - app.py       |
                 | - routes.py    |
                 | - logic.py     |
                 +---+---+-------+
                     |
           +---------+---------+
           |                   |
           v                   v
  +----------------+    +----------------+
  | Local JSON Data|    | PostgreSQL DB  |
  | jokes.json     |    | visitors/health|
  | names.json     |    +----------------+
  +----------------+
                     ^
                     |
         +-----------+-----------+
         | Prometheus Monitoring |
         +-----------+-----------+
                     |
                     v
              +-------------+
              |  Grafana    |
              | Dashboards  |
              +-------------+


# Key Notes:

The Flask app handles all HTTP requests (API + HTML routes).

Local JSON files are the primary data source for jokes and names. PostgreSQL is optional but ready for full CRUD operations.

Prometheus collects metrics from Flask endpoints (/metrics).

Grafana visualizes metrics for observability.




# File / Folder Structure

Here’s a detailed explanation of key folders and files in lumen_web:

File / Folder	Purpose

app.py	Main entry point; initializes Flask, registers routes, and runs DB setup.
logic.py	Core async logic for random jokes retrieval and name search.
routes.py	Defines API endpoints and HTML routes; integrates logic.py and crud.py.
crud.py	Async database operations for visitors and health reports.
models.py	PostgreSQL table schemas (visitors, health_report).
db.py	Async DB connection pool setup (asyncpg).
init_db.py	Initializes tables at app startup.
requirements.txt	Lists Python dependencies.
render.yaml	Deployment configuration for Render.
run_start.sh	Startup script launching Gunicorn.
jokes.json / names.json	Local datasets.
templates/	HTML templates (index.html, test.html).
static/	CSS, JS, images for frontend.



---

# Component Roles

1. Web Application (Flask)

Handles HTTP requests.

Exposes async API endpoints:

/api/get-item → random joke

/api-search → name search

CRUD endpoints for visitors and health


Serves HTML pages (index.html, test.html) for demonstration or dashboard purposes.

Integrates with Prometheus for metrics.


2. Database

PostgreSQL (optional) stores visitors and health reports.

Tables auto-initialize on startup via init_db.py.

Supports future expansion for storing jokes/names in DB.




3. Monitoring

Prometheus scrapes metrics from the Flask app (/metrics endpoint).

Grafana visualizes metrics like API request counts, response times, visitor logs, and health reports.


4. CI/CD Pipeline With GitHub Actions Workflow

Located at .github/workflows/deploy.yml

Stage Description Build & Test Spins up PostgreSQL in CI → installs dependencies → lints code → verifies DB connection Docker Build Builds the Docker image for the Flask app Deploy to Render On successful build/test, triggers a Render deploy via API using stored secrets and sends Email Notificatuons

Secrets used:

RENDER_API_KEY

RENDER_SERVICE_ID

Trigger: On push or PR to the main branch.


5. Docker & Networking

Locally orchestrated using Docker Compose:

Shared network (lumen_net) for inter-service communication.

Volume (grafana_data) for Grafana persistence.


On Render, each service runs independently; inter-service communication is handled via public/external URLs.



---

# Local vs Render Deployment Architecture

Aspect	Local Docker Compose	Render (PaaS)

Service startup	Single command (docker-compose up)	Services run independently; separate containers
Networking	Shared Docker network (lumen_net)	Inter-service communication via URLs/env variables
Database	Local Postgres container	Render-managed Postgres or external DB
Metrics scraping	Prometheus scrapes container IP	Prometheus scrapes public app URL
Dashboard persistence	Docker volume (grafana_data)	Use Render persistent storage (if configured)
CI/CD	Manual trigger for local build	GitHub Actions triggers Render deployment




# 3. Tech Stack

Lumen Web uses a combination of Python backend frameworks, containerization tools, monitoring solutions, and deployment platforms to provide a fully-featured, DevOps-ready web application.


---

# Programming Language & Framework

Technology	Purpose

Python 3.11	Core programming language for the backend. Chosen for async support and lightweight scripting.
Flask (async-capable, v3.1.1)	Web framework used to build the API and serve HTML templates. Async support ensures non-blocking operations for high-concurrency endpoints.
Flask-CORS	Enables cross-origin requests for frontend API interactions.
HTTPX	Async HTTP client used if external API calls are needed in the future.



---

# Containerization & Orchestration

Technology	Purpose

Docker	Packages the Flask app and dependencies into a container for consistent runtime.
Docker Compose	Orchestrates multi-container environments locally (Flask app, PostgreSQL, Prometheus, Grafana).
Docker Network	Provides isolated communication between containers (lumen_net).
Docker Volumes	Persists Grafana dashboards and configurations across container restarts.



---

# CI/CD Tools

Technology	Purpose

GitHub Actions	Automates the build, test, and deployment pipeline.
Render API	Deploys the application to Render automatically after successful pipeline runs.
push.sh	Helper script to standardize Git commits and push to trigger CI/CD workflows.





# Database

Technology	Purpose

PostgreSQL	Optional database for storing visitors and health reports. Supports async access using asyncpg.
asyncpg	Async Python driver for PostgreSQL, ensuring non-blocking DB operations.
SQLAlchemy (ready)	Database models are compatible with future SQLAlchemy integration for ORM functionality.



---

# Monitoring & Observability

Technology	Purpose

Prometheus	Collects metrics from the Flask app (/metrics endpoint). Monitors API performance and health.
Grafana	Visualizes metrics from Prometheus. Provides dashboards for response times, API usage, visitor stats, and health logs.
Prometheus-Flask-Exporter	Integrates Prometheus scraping with Flask app endpoints for metrics collection.



---

# Deployment Platform

Technology	Purpose

Render	Cloud PaaS for hosting the web app and database. Handles automatic scaling, container management, and public access.
Gunicorn	Production-grade WSGI server used to run Flask app on Render (run_start.sh).



---

# Utilities & Supporting Libraries

Technology	Purpose

Python-dotenv	Loads environment variables from .env for local development.
Requests	Standard HTTP client for synchronous requests (used if needed).
Uvicorn	Optional ASGI server for async testing or local development.



---

# Summary

The stack was chosen to provide:

Asynchronous performance (Flask async + asyncpg + HTTPX)

Containerized consistency across local and cloud environments

Automated CI/CD with GitHub Actions + Render

Observability via Prometheus + Grafana

Flexibility to evolve from file-based JSON data to fully DB-backed architecture




# 4. Setup & Installation

Lumen Web can be run locally for development and testing on Linux server or deployed to Render, AWS etc for production. This section explains all steps for both scenarios.


---

#Prerequisites

Before setting up the project, ensure you have the following installed:

Git – For cloning the repository.

Python 3.11 – Required for local development and dependency management.

Docker & Docker Compose – For building and running multi-service containers.

Optional: PostgreSQL locally (if you want to test DB-backed visitors and health endpoints).


Check versions:

git --version
python3 --version
docker --version
docker-compose --version


---

#Environment Configuration

The project uses environment variables to configure the application and database.

1. Create a .env file in lumen_web/:



# Database connection string (PostgreSQL)
DB_URL_EXTERNAL=postgres://user:password@localhost:5432/lumen_db

# Prometheus metrics path
METRICS_PATH=/metrics

2. Notes on environment variables:



Variable	Purpose

DB_URL_EXTERNAL	URL to connect to PostgreSQL. Used by asyncpg in db.py.
METRICS_PATH	Path where Prometheus scrapes Flask metrics (/metrics).
PORT	Port for Render deployment. Local Docker defaults to 5000.



Local Development Setup (Docker Compose)

The project uses Docker Compose to orchestrate:

1. Flask web app


2. Prometheus monitoring


3. Grafana dashboards



Steps:

1. Build and start services:



docker-compose up --build

2. Access services:



Service	URL (local)

Flask App / API	http://localhost:5000
Prometheus UI	http://localhost:9090
Grafana UI	http://localhost:3000 (login: admin/admin)


3. Stop services:



docker-compose down

Notes:

The Flask container reads .env for DB connection and metrics path.

Grafana dashboards are persisted in the named volume grafana_data.

Prometheus scrapes metrics from Flask’s /metrics endpoint automatically.



---

Running Locally Without Docker (Optional)

For development without containers:

# Install dependencies
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r lumen_web/requirements.txt

# Initialize database tables
python lumen_web/init_db.py

# Start Flask app
python lumen_web/app.py

Access the API at http://127.0.0.1:5000.



#Render Deployment

1. Render requires each service to run independently; shared Docker networks do not exist.


2. Deployment steps:



Configure environment variables on Render dashboard or use render.yaml.

Build command:


pip install --upgrade pip
pip install -r requirements.txt

Start command:


./run_start.sh

Render automatically assigns a port via ${PORT}. run_start.sh ensures Gunicorn binds to the correct port.

Prometheus and Grafana should be deployed as separate services if required (or monitored externally).



#Testing the Setup

1. Test Flask API:



curl http://localhost:5000/api/get-item

2. Test name search:



curl -X POST -H "Content-Type: application/json" -d '{"name":"Trump"}' http://localhost:5000/api-search

3. Visit Grafana at http://localhost:3000 to verify dashboards.




# 5. Application Functionality


#5.1 Core Features

✔ Random Jokes API

Reads from jokes.json

Returns 1 random joke per request

Non-blocking async function

Provides simple JSON output


Example Response

{
  "joke": "Why don’t programmers like nature? It has too many bugs."
}


---

✔ Celebrity Name Search API

Uses names.json, a list of known celebrities.

Supported Features:

Case-insensitive search

Partial substring search
e.g., "tr" → matches "Trump", "Trevor Noah"


Example Request

{
  "name": "Trump"
}

Example Response

{
  "searched": "Trump",
  "found": true,
  "matches": ["Donald Trump"]
}

If no match is found:

{
  "searched": "xxxx",
  "found": false,
  "matches": []
}




# Render Free Tier Limitations (Observed in This Project)

Below are the constraints that affected architecture, CI/CD, worker logic, and deployment strategy.


---

# 1. Only Web & Static Web Are Free

Render Free tier supports only 2 service types for free:

Web Service (runs via HTTP)

Static Web


Not Free (Paid only):

Background Worker Service

Cron Jobs

Private Services

Deploy hooks with workers


Impact:
The intention is to monitor the Flask app with worker_dir as a background but it cannot run 100% as a real worker.

Workaround: 
Deploy it as a separate Web Service and call the main app using its external public URL.



---

# 2. Web Services Sleep / Suspend Easily

All Free-tier services:

Sleep after a few minutes of inactivity

Cold start on first request (10–30 sec delay)

Do not guarantee continuous uptime

Can momentarily stop during internal rebalancing


Impact:

The “worker_dir service” stops tracking the app health whenever Render suspends it

Cron-like or monitoring loops become unreliable

Metrics become inconsistent (Prometheus scrapers time out)


Workaround:

Workers must:

Use external heartbeat endpoints

Attempt retries & exponential backoff

Not rely on strict timing (e.g., every second)

Expect downtime/restarts


# 3. Free Postgres Has Expiration & Size Limits

Render’s free PostgreSQL has:

30-day expiration

Shared, low-performance CPU

very small disk quota (~100MB)

connection caps (max 10 active)

slow cold-start query response


Impact:

Long-term persistent data (jokes, names, metrics) could be lost

Worker timeouts can occur when DB is slow

Migrations restart because DB sleeps


Workaround:
Use JSON files inside the repo for long-lived, read-heavy data.
This avoids database expiration and cold-start slowness.


---

# 4. No Docker, No Compose, No Multi-Container Networking

Render Free tier does not support:

docker-compose

multi-container builds

shared private networks between services


Impact:
Your local setup has:

Flask + Prometheus + Grafana (docker-compose)

But Render cannot replicate this.

Workaround:

Deploy each service separately

Connect via public URLs

Configure Prometheus scrape targets using Render’s domain names

Grafana dashboards must be manually set up per deployment






