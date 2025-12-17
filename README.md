# DevOps Shield

DevOps Shield is a zero-trust security layer for CI/CD pipelines. The platform combines a FastAPI backend, a React dashboard, threat intelligence modules, and optional blockchain-backed attestations to surface fraud and supply-chain risks from commit to release.

## 🏆 Hackathon Project

**Event:** MindSprint 2K25 Hackathon  
**Team Members:**
- Shaik. Muzkeer
- Shaik. Abdul Sammed
- Suhail. B. K

---

## Key Capabilities

- **Attack Simulation Lab** – Launch supply-chain, secret-leak, and rogue-runner drills from the UI. The frontend can run entirely offline by replaying deterministic fallbacks when the API is unreachable.
- **Zero-Trust Controls** – Source integrity scoring, dependency whitelisting, runner verification, and blockchain ledgering exposed through `/api/zero-trust/*` routes.
- **Risk Intelligence** – AI/ML heuristics (`backend/src/core/`) combine anomaly detection, rules, and threat signatures to produce risk scores and alerts.
- **Immutable Auditing** – Blockchain services store to an Ethereum-compatible network when `BLOCKCHAIN_ENABLED=true`; otherwise they fall back to signed local logs.
- **Observability First** – Centralized logging (`backend/start.sh`, `src/utils/logger.py`), rate limiting middleware, and REST/WebSocket APIs power the React telemetry views.

---

## Architecture Snapshot

```
frontend/ (React 18)
  src/
    pages/Simulation.jsx           <- Simulation lab (uses fallbacks if API offline)
    api/zeroTrustService.js        <- Health, dependency, ledger, artifact calls
    services/apiClient.js          <- Fetch wrapper with logging
backend/ (FastAPI)
  main.py                          <- Entrypoint; patches sys.path for src imports
  start.sh                         <- Activates venv, exports PYTHONPATH, starts Uvicorn
  src/
    api/                           <- REST routers (simulate, fraud, alerts, zero-trust, etc.)
    core/                          <- AI analyzers and fraud engine
    security/                      <- Zero-trust orchestrator & pipeline controls
    services/                      <- Blockchain, database, email, slack integrations
    middleware/rate_limiter.py     <- DoS protection middleware
    utils/                         <- Config loader, logger, validators, threat signatures
infra/
  docker/backend.Dockerfile        <- Backend container definition
  docker/frontend.Dockerfile       <- Frontend container definition
  docker-compose.yml               <- Local multi-container setup
railway.toml                       <- Production start command (calls ./start.sh)
Dockerfile                         <- All-in-one container for Railway/Nixpacks
```

---

## Repository Layout

```
backend/           FastAPI service (see backend/README_BACKEND.md)
frontend/          React dashboard (see frontend/README_FRONTEND.md)
contracts/         Solidity contract(s) for immutable audit logging
docs/              Extended documentation (API, threat model, runbooks)
infra/             Dockerfiles, Kubernetes, Terraform scaffolding
ml/                Datasets, models, and notebooks for anomaly detection
scripts/           Helper scripts (deploy, seed data, training data generation)
security/          Threat patterns, secure coding guidelines, dependency blocklists
start.sh           Shared launcher used by Railway/Nixpacks and local demos
Dockerfile         Single-image build that runs ./start.sh (backend + libs)
railway.toml       Railway deploy configuration (start command & builder)
```

---

## Quick Start

For detailed setup and deployment instructions, see [SETUP_GUIDE.md](SETUP_GUIDE.md).

### Prerequisites

- Python 3.10+
- Node.js 18+
- npm or yarn
- (Optional) Docker 24+ if using containers

### Backend

```bash
# install
cd backend
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# run (defaults to port 8080; override with PORT)
PORT=8000 ../start.sh
```

`start.sh` ensures `backend/` is on `PYTHONPATH`, activates any existing virtual environment, and starts Uvicorn with the correct host/port. When running locally keep the process attached so logs stream to the console.

### Frontend

```bash
cd frontend
npm install
npm start
```

The React app expects `REACT_APP_API_URL` (defaults to `http://localhost:8000`). Update `.env` if the backend runs elsewhere.

### Docker Compose (optional)

```bash
docker compose up --build
```

This uses `infra/docker/backend.Dockerfile` and `infra/docker/frontend.Dockerfile` to run both services. SQLite data is mounted from `backend/database/` so local runs persist state.

---

## Simulation Lab

`frontend/src/pages/Simulation.jsx` drives the Attack Simulation page. The workflow:

1. Performs a health probe via `zeroTrustService.healthCheck()`.
2. Invokes `/api/simulate` for a fraud event preview (`backend/src/api/simulate_routes.py`).
3. Executes zero-trust checks (dependency sentinel, ledger recording, source integrity, artifact verification).

If any backend call fails (offline demo, network hiccup) the frontend returns realistic fallback payloads so the user experience continues without console errors. To exercise the live API, keep the backend running on the URL configured in `REACT_APP_API_URL`.

---

## API Highlights

| Endpoint | Description |
|----------|-------------|
| `GET /health` | Liveness check used by the UI and Railway |
| `GET /api/simulate` | Generates a mock fraud event for the simulation lab |
| `POST /api/zero-trust/source/verify` | Source integrity scoring (stubbed if module missing) |
| `POST /api/zero-trust/deps/check` | Dependency whitelist / namespace guard |
| `POST /api/zero-trust/ledger/record` | Blockchain-backed audit logging (local fallback when disabled) |
| `POST /api/zero-trust/artifact/verify` | Artifact signing + sandbox verification |
| `GET /api/fraud/stats` | High-level fraud metrics |
| `GET /api/alerts/recent` | Recent alerts for the dashboard |

Full request/response schemas are documented in `docs/04_API_Documentation.md` and FastAPI generates live docs at `/docs` when running.

---

## Configuration

| Variable | Default | Purpose |
|----------|---------|---------|
| `PORT` | `8080` | Backend listen port (`start.sh` respects overrides) |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1,*.onrender.com` | TrustedHostMiddleware whitelist |
| `CORS_ORIGINS` | `http://localhost:3000` | Allowed origins for the React app |
| `DB_PATH` | `database/fraud_logs.db` | SQLite location; use `DATABASE_URL` for Postgres |
| `LOG_LEVEL` | `INFO` | Backend logging level |
| `BLOCKCHAIN_ENABLED` | `false` | Toggle Web3 integration; requires provider + keys when true |
| `BLOCKCHAIN_PROVIDER_URL` | _empty_ | RPC endpoint (set when enabling blockchain) |
| `SLACK_WEBHOOK_URL` | _empty_ | Enable Slack alerts |
| `SMTP_*` | _varies_ | Email alert configuration |

Copy `.env.example` files (where available) or create your own `.env` and export variables before launching.

---

## Deployment Notes

### Railway

- `railway.toml` points the deploy command to `./start.sh` so PYTHONPATH is set automatically.
- Nixpacks uses the root `Dockerfile`, which installs backend requirements and runs the same script.
- Ensure `BLOCKCHAIN_ENABLED` remains `false` unless a Web3 provider is configured; otherwise the service uses local fallback storage and suppresses noisy warnings.

### Dockerfile (root)

The root `Dockerfile` builds a single-image backend:

1. Installs Python 3.10 slim dependencies and `backend/requirements.txt`.
2. Copies the entire repository to `/app`.
3. Marks `start.sh` executable and sets `PYTHONPATH=/app/backend`.
4. Runs `./start.sh` on container start.

Use this for Railway, Render, or any platform that expects a single command.

---

## Testing

```bash
# backend unit tests
cd backend
pytest

# frontend lint/tests
cd frontend
npm test
```

Additional scenario scripts live in `scripts/` and notebooks in `ml/notebooks/` for experimentation.

---

## Licensing

DevOps Shield is released under the MIT License. See `LICENSE` for details.
