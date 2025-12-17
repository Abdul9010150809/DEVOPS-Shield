# Setup & Deployment Guide

## Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- npm or yarn

### Backend Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Run backend
PORT=8000 ../start.sh
```

Backend will be available at `http://localhost:8000`

### Frontend Setup

```bash
cd frontend
npm install

# Configure environment
cp .env.example .env.local
# Ensure REACT_APP_API_URL matches backend URL

# Run frontend
npm start
```

Frontend will be available at `http://localhost:3000`

## Connection Verification

### Test Backend Health
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "DevOps Shield Backend",
  "version": "1.0.0",
  "environment": "development",
  "timestamp": "2025-12-17T...",
  "cors_origins": ["http://localhost:3000"],
  "database": "operational"
}
```

### Test Frontend Connection
1. Open browser console (F12)
2. Go to http://localhost:3000
3. Check console logs for `[API Config] Initialized with base URL: http://localhost:8000`
4. Try navigating to Dashboard - should load without API errors

## Environment Variables

### Backend (.env)
- `PORT` - Server port (default: 8000)
- `ENVIRONMENT` - development/production
- `SECRET_KEY` - JWT secret (change in production)
- `CORS_ORIGINS` - Frontend URLs allowed to connect
- `ALLOWED_HOSTS` - Trusted hosts
- `DB_PATH` - SQLite database path
- `BLOCKCHAIN_ENABLED` - Enable blockchain integration (default: false)

### Frontend (.env.local / .env.production)
- `REACT_APP_API_URL` - Backend API URL

## Pages & Features

All pages should now work properly:
- ✅ Dashboard - Main overview with risk metrics
- ✅ Pipelines - Pipeline management and details
- ✅ Alerts - Alert management and triage
- ✅ Simulation - Attack simulation lab
- ✅ Blockchain Audit - Immutable audit logs
- ✅ Audit - Compliance audit trails
- ✅ Settings - Configuration and integrations
- ✅ GitHub Connect - GitHub integration
- ✅ Societal Impact - Impact metrics

## API Endpoints

All endpoints are prefixed with `/api`:
- `GET /health` - Health check
- `GET /simulate` - Fraud simulation
- `GET /fraud/stats` - Fraud statistics
- `GET /alerts/recent` - Recent alerts
- `POST /alerts/{id}/resolve` - Resolve alert
- `POST /zero-trust/*` - Zero-trust controls
- `POST /blockchain/*` - Blockchain operations

## Docker Deployment

```bash
# Build and run with Docker Compose
docker compose up --build

# Or use Railway
railway up
```

## Troubleshooting

### Frontend can't connect to backend
- Check CORS_ORIGINS in backend .env
- Ensure REACT_APP_API_URL in frontend .env matches backend URL
- Check browser console for API errors
- Verify backend is running: `curl http://localhost:8000/health`

### API endpoints return 404
- Check router loading logs on backend startup
- Ensure all modules import correctly
- Run: `python -c "from src.api import *; print('✓ All imports OK')"`

### Database errors
- Ensure database directory exists: `mkdir -p backend/database`
- Check DB_PATH in .env
- Try: `python backend/scripts/init_db.py`

## Production Deployment

1. Update `.env` with production values
2. Set `ENVIRONMENT=production`
3. Generate strong `SECRET_KEY`
4. Configure `CORS_ORIGINS` for frontend domain
5. Enable HTTPS and security headers
6. Set `BLOCKCHAIN_ENABLED=false` unless configured
7. Use production database (PostgreSQL recommended)
8. Set up monitoring and alerting

## Support

For issues, check:
- Backend logs: `logs/fraud_shield.log`
- Frontend console: Browser Developer Tools
- Docker logs: `docker compose logs`
- API docs: `http://localhost:8000/docs` (when running)
