 PROJECT: LUMEN_WEB - AUTOMATED CI/CD & MONITORING SETUP

Overview

Lumen Web is a lightweight Flask web application containerized with Docker and deployed automatically to Render using a GitHub Actions CI/CD pipeline.
The project demonstrates real-world DevOps practices — including multi-service orchestration, database integration, pipeline automation, and monitoring using Prometheus + Grafana.

 System Architecture
project-root/
│
├── lumen_web/                 # Flask backend app
│   ├── app.py                 # Main application logic
│   ├── db.py                  # PostgreSQL DB connection handler
│   ├── templates/             # HTML templates
│   ├── Dockerfile             # App Docker build
│   ├── render.yaml            # Render deployment config
│   ├── requirements.txt       # Python dependencies
│   └── run_start.sh           # Gunicorn startup script
│
├── prometheus/                # Prometheus configuration
│   └── prometheus.yml
│
├── grafana/grafana.yaml                   # Grafana dashboards/configs
│
├── .github/workflows/deploy.yml  # CI/CD pipeline definition
├── docker-compose.yml         # Multi-service local setup
├── .env                       # Environment variables
└── README.md

 CI/CD Pipeline Overview
GitHub Actions Workflow

Located at .github/workflows/deploy.yml

Stage	Description
 Build & Test	Spins up PostgreSQL in CI → installs dependencies → lints code → verifies DB connection
 Docker Build	Builds the Docker image for the Flask app
 Deploy to Render	On successful build/test, triggers a Render deploy via API using stored secrets

Secrets used:

RENDER_API_KEY

RENDER_SERVICE_ID

Trigger: On push or PR to the main branch.


 Docker Compose Orchestration

The docker-compose.yml defines a 3-container setup for local development:

Service	Description	Port
web	Flask backend connected to PostgreSQL	5000
prometheus	Collects metrics from the app	9090
grafana	Visualizes metrics from Prometheus	3000

Run locally:

docker-compose up --build


 Monitoring Stack

Prometheus scrapes /metrics endpoint from Flask container.

Grafana visualizes performance and uptime metrics.

Metrics path configured via METRICS_PATH=/metrics environment variable.


 Render Deployment

Configured using render.yaml.
Automatically built via pip install -r requirements.txt and started using Gunicorn:

exec gunicorn app:app --bind "0.0.0.0:${PORT:-5000}" --workers 4


 Tech Stack
Category	Tools
Language / Framework	Python (Flask)
CI/CD	GitHub Actions
Containerization	Docker, Docker Compose
Deployment	Render
Monitoring	Prometheus, Grafana
Database	PostgreSQL
Automation	Shell scripting (run_start.sh)

 Testing / Verification

Linting via flake8

DB connectivity test inside CI pipeline

Build verification via docker build

Auto-deploy skipped with commit message containing skip deploy


 Key Achievements

Automated build → test → deploy pipeline on Render

Integrated Prometheus & Grafana for live app monitoring

Used multi-environment DB config (Local, CI, Render)

Deployed via Render API trigger through GitHub Actions

Applied environment-driven config (.env, os.getenv, dotenv)

