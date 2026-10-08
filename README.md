# Provider Data Change Monitoring — React + FastAPI + Databricks Apps

This starter implements the v6 UI as a React/Vite frontend with a Python FastAPI backend. The production React build is served by FastAPI, so Databricks Apps runs one application process.

## Local

Prerequisites: Python 3.11+, Node.js 22+, npm.

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
npm install
npm run build
uvicorn backend.main:app --reload --port 8000
```

For frontend hot reload, use two terminals:

```bash
uvicorn backend.main:app --reload --port 8000
npm run dev
```

Open http://localhost:5173.

## Databricks Apps

Create a custom Databricks App and deploy this project. Databricks detects `package.json`, installs Node dependencies, runs the `build` script, installs Python dependencies, then starts the command in `app.yaml`.

`app.yaml` uses `${DATABRICKS_APP_PORT}` so the FastAPI server listens on the port supplied by Databricks Apps.

Typical CLI sync:

```bash
databricks auth login
databricks sync . /Workspace/Users/<your-user>/provider-monitoring-app
```

Then use the deployment command shown on the Databricks App page, or configure the app directly against a Git repository.

## API

- GET `/api/health`
- GET `/api/metrics`
- GET `/api/providers`
- GET `/api/providers/{id}`
- POST `/api/providers/{id}/submit`
- POST `/api/reviewer/bulk-approve`
- GET `/api/source-health`
- POST `/api/source-health/{source}/refresh`

## Production integration

`backend/service.py` is a mock repository so the application runs immediately. Replace it with a repository layer backed by Databricks SQL/Delta Gold tables. The UI should never query Delta directly.

Recommended production tables:
- `gold.payer_provider_master`
- `gold.provider_change_event`
- `gold.provider_change_summary`
- `gold.provider_cross_source_discrepancy`
- `gold.provider_identity_crosswalk`

Keep source weights configurable in a table/configuration layer rather than hard-coded in React. Demo values currently shown are NPPES 0.95, PECOS 0.88 and Client Provider Master Roster 0.55.

For production Databricks access, configure the app's resources/authorization and use the Databricks SQL connector or SDK from the backend. Do not put tokens or secrets in React.
