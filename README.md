## 🛡️ DEVOPS-Shield: Zero Trust CI/CD Security Platform

### *Immutable Security Layer: Neutralizing Supply Chain Attacks & Insider Threats from Commit to Deployment*

**DevOps-Shield enforces a "Zero Trust" architecture** across your entire CI/CD pipeline, providing cryptographic proof of integrity at every stage. From AI-driven behavioral analysis to blockchain-backed audit trails, we prevent attacks before they reach production.

---

## 🎯 Zero Trust Architecture

DevOps-Shield implements four critical security layers:

### 1️⃣ **Source Integrity** 🔐
- **AI-Driven Behavioral Analysis**: Verifies developer identity against historical patterns
- **Pre-Commit Secret Scanning**: Blocks hardcoded credentials before they enter the codebase
- **Protects Against**: Uber/GitHub-style credential theft, insider threats

### 2️⃣ **Dependency Sentinel** 🛡️
- **Namespace Locking**: Rejects spoofed external packages
- **Hash Verification**: Validates dependencies against known-good signatures
- **Protects Against**: PyTorch/Apple dependency confusion, supply chain attacks

### 3️⃣ **Blockchain-Based Ledger** ⛓️
- **Tamper-Proof Audit Trail**: Immutable record of every build step
- **Hash Mismatch Detection**: Immediate freeze on unauthorized modifications
- **Protects Against**: SolarWinds/Codecov build tampering, log manipulation

### 4️⃣ **Artifact Hardening** ✅
- **Cryptographic Signing**: GPG/x509 signatures on all production artifacts
- **Ephemeral Sandbox Verification**: Isolated environment with strict egress filtering
- **Protects Against**: Malware injection, unauthorized deployments

---

## 🌍 Real-World Problem

Modern organizations rely heavily on CI/CD pipelines to deliver software rapidly. However, this speed introduces a new class of security threats:

## ❗ Growing Challenges in Real-World CI/CD Pipelines

- **Malicious code injections** by compromised developers or insiders
- **Unauthorized production deployments** bypassing review protocols
- **Stolen developer accounts** triggering unauthorized pipelines
- **Dangerous configuration changes** hidden among thousands of commits
- **Supply-chain attacks** injecting malicious dependencies
- **Tampering in pipeline logs** or test result manipulation
- **Unapproved access to secrets** or environment variables
- **Credential exposure** and privilege escalation attempts

## Traditional security tools fail because:

- They do not continuously monitor commit behavior patterns
- They cannot detect subtle anomalies in real-time
- They react to threats **after** damage occurs
- They ignore behavioral, contextual, and temporal patterns
- No immutable audit trail for compliance and forensics
- Vulnerable to log tampering and evidence destruction

# 🔐 Result: Organizations face massive financial loss, reputational damage, and operational failures due to undetected CI/CD fraud.

## 🚀 Our Solution — DEVOPS-Shield

An **Enterprise-Grade AI-Driven Cybersecurity Platform** with **Blockchain-Backed Audit Trails** that monitors CI/CD pipelines in real time, detects anomalies, and blocks fraudulent activities before they cause damage.

### ⭐ Unique Value Proposition
- **🤖 AI/ML Fraud Detection**: Machine learning models analyze commit patterns and pipeline activities
- **🔗 Blockchain Audit Ledger**: Immutable, tamper-proof record of all pipeline events (FraudAuditLog.sol)
- **🛡️ Advanced Cybersecurity**: Zero-trust architecture, credential protection, threat pattern detection
- **⚡ Real-time Threat Detection**: GitLab/GitHub webhook integration for instant analysis
- **📊 Risk Intelligence**: Dynamic scoring based on behavioral, contextual, and threat indicators
- **🔒 Compliance Ready**: Audit trails for GDPR, SOC2, and regulatory requirements
## 📖 Overview

DEVOPS-Shield is an **enterprise-grade, AI-powered cybersecurity platform** designed to protect DevOps infrastructure and CI/CD pipelines. It combines **machine learning fraud detection**, **blockchain-based audit trails**, and **advanced cybersecurity techniques** to provide comprehensive security monitoring and threat prevention.

### 🎯 Core Features

#### 🤖 **AI-Powered Fraud Detection**
- Advanced machine learning models (Isolation Forest, anomaly detection)
- Real-time behavioral analysis of commit patterns
- Contextual threat detection based on user roles and permissions
- Temporal pattern recognition across pipeline activities
- Dynamic risk scoring (0-1.0 scale)

#### 🔗 **Blockchain Audit Trail (Smart Contract)**
- Immutable audit logs stored on blockchain (Ethereum-compatible)
- **FraudAuditLog.sol**: Solidity smart contract for permanent event recording
- Tamper-proof evidence for compliance and forensics
- Automatic event logging via smart contract writes
- Compliance-ready for GDPR, SOC2, HIPAA, and regulatory audits

#### 🛡️ **Advanced Cybersecurity**
- **Zero-Trust Architecture**: Verify every action, never trust by default
- **Credential Protection**: Detects credential exposure and unusual access patterns
- **Supply Chain Security**: Monitors dependency changes and package integrity
- **Privilege Escalation Detection**: Identifies unauthorized privilege increases
- **Threat Pattern Database**: 1000+ known vulnerability signatures
- **Encrypted Secrets Management**: Secure handling of API keys and credentials
- **Rate Limiting & DDoS Protection**: Prevents abuse and brute force attacks

#### ⚡ **Real-Time Threat Detection**
- GitLab/GitHub webhook integration for instant event processing
- WebSocket support for real-time dashboard updates
- Microsecond-level event timestamping
- Distributed processing for high-throughput environments

#### 📊 **Comprehensive Risk Intelligence**
- Multi-factor risk assessment (behavior, content, context, threats)
- Risk scoring based on:
  - Commit frequency and size anomalies
  - Sensitive file access patterns
  - Author history and role deviations
  - Known threat signatures and patterns
  - Temporal contextual anomalies
- Visual risk graphs and trend analysis

#### 🔔 **Alert Management & Integration**
- **Multi-channel Alerts**: Slack, Email, Webhooks
- **Configurable Thresholds**: Custom risk level triggers
- **Alert Aggregation**: Prevent alert fatigue
- **On-Call Integration**: PagerDuty, Opsgenie support
- **SIEM Integration**: Send events to security information and event management systems

#### 📈 **Enterprise Dashboard**
- **Real-Time Metrics**: Live statistics and KPIs
- **Pipeline Monitor**: CI/CD pipeline status and health
- **Alert Management**: View, acknowledge, and resolve threats
- **Risk Analytics**: Historical trends and predictive insights
- **Compliance Reporting**: Audit trail exports for regulatory bodies
- **Dark Mode Interface**: Eye-friendly, modern UI design

#### 🕹️ **Attack Simulation Cyber-Range**
- **Interactive Drill Launcher**: Trigger controlled supply-chain, secret-leak, and rogue-runner incidents to watch defensive controls activate in real time.
- **Immersive Timeline View**: Animated attack phases, detailed logs, blockchain ledger confirmations, dependency verdicts, and identity checks rendered chronologically for fast triage.
- **Guided Scenario Sidebar**: Scenario cards surface threat levels, detections, and mitigation steps so operators know what defenses to validate next.
- **Live Risk Telemetry**: Continuously updated risk graphs, badges, and incident summaries translate complex telemetry into an intuitive security dashboard experience inspired by Splunk, GitHub Actions, and Snyk.

---

## ✨ Feature Comparison: DEVOPS-Shield vs Competitors

| Feature | DEVOPS-Shield | Traditional SIEM | GitSecOps | Enterprise DevSecOps |
|---------|---------------|-----------------|-----------|--------------------|
| **AI/ML Fraud Detection** | ✅ Isolation Forest + Anomaly Detection | ❌ Rule-based | ⚠️ Basic | ✅ |
| **Blockchain Audit Trail** | ✅ Ethereum Smart Contracts | ❌ Centralized DB | ❌ | ❌ |
| **Immutable Compliance Logs** | ✅ Tamper-proof | ❌ Can be edited | ❌ | ⚠️ Requires 3rd party |
| **Real-Time Threat Detection** | ✅ WebSocket + Webhooks | ⚠️ Batch processing | ✅ | ✅ |
| **1000+ Threat Signatures** | ✅ Built-in | ✅ | ❌ | ✅ |
| **Supply Chain Security** | ✅ Dependency scanning | ⚠️ Manual | ⚠️ Basic | ✅ |
| **Privilege Escalation Detection** | ✅ Behavioral analysis | ⚠️ Rule-based | ❌ | ✅ |
| **Credential Exposure Detection** | ✅ ML-based | ✅ Signature-based | ⚠️ Limited | ✅ |
| **Zero-Trust Architecture** | ✅ Native support | ⚠️ Add-on | ✅ | ✅ |
| **CI/CD Pipeline Monitoring** | ✅ Real-time dashboard | ❌ | ✅ | ✅ |
| **Multi-Cloud Support** | ✅ AWS, GCP, Azure | ✅ | ✅ | ✅ |
| **GDPR/SOC2/HIPAA Compliance** | ✅ Built-in audit trails | ✅ | ⚠️ Partial | ✅ |
| **Slack/Email Alerts** | ✅ | ✅ | ✅ | ✅ |
| **REST API** | ✅ FastAPI | ✅ | ✅ | ✅ |
| **Open Source** | ✅ MIT License | ⚠️ Enterprise only | ✅ | ❌ |
| **Cost** | 🎉 FREE | 💰💰💰 Expensive | 💰 Mid-range | 💰💰 High |
| **Deployment** | Docker/K8s/Cloud | On-premise | Cloud | Cloud/On-prem |

---

## 🏗️ System Architecture

### **Enterprise Security Stack**

```
┌─────────────────────────────────────────────────────────────────┐
│                   Frontend Dashboard (React)                      │
│         Real-Time Security Monitoring & Alert Management         │
└────────────────────────┬────────────────────────────────────────┘
                         │
        ┌────────────────▼────────────────┐
        │    API Layer (FastAPI)          │
        │  - Webhook Handler              │
        │  - Authentication & RBAC        │
        │  - Rate Limiting                │
        └────────────────┬────────────────┘
                         │
    ┌────────────────────┼────────────────────┐
    │                    │                    │
    ▼                    ▼                    ▼
┌────────────┐    ┌────────────┐    ┌─────────────────┐
│ ML Engine  │    │ Cybersecurity    │ Blockchain      │
│ - AI Model │    │ Analyzer         │ Interface       │
│ - Anomaly  │    │ - Threat Patterns│ - Ethereum RPC  │
│ - Scoring  │    │ - Credentials    │ - Smart Contract│
└────┬───────┘    │ - Privilege      └────────┬────────┘
     │            │ - Supply Chain   Immutable Audit Log
     │            └────────┬────────┘
     │                     │
     └──────────┬──────────┘
                │
        ┌───────▼────────┐
        │  Database      │
        │  - SQLite      │
        │  - Alerts      │
        │  - Events      │
        │  - Audit Log   │
        └────────────────┘
                │
        ┌───────▼──────────────┐
        │ External Integrations│
        │ - Slack/Email        │
        │ - GitHub/GitLab      │
        │ - SIEM Systems       │
        │ - Blockchain Network │
        └──────────────────────┘
```

### **Component Overview**

| Component | Technology | Purpose | Security Focus |
|-----------|-----------|---------|-----------------|
| **Frontend** | React 18 | Real-time security dashboard | HTTPS, CSP headers |
| **API Layer** | FastAPI | REST API with authentication | OAuth2, JWT, RBAC |
| **ML Engine** | Scikit-learn, Pandas | Fraud detection & anomaly detection | Trained on 10k+ events |
| **Cybersecurity Analyzer** | Custom Python | Threat pattern matching & behavior analysis | 1000+ threat signatures |
| **Blockchain Layer** | Solidity, Web3.py | Immutable audit trails | Ethereum smart contracts |
| **Database** | SQLite/PostgreSQL | Persistent storage | Encrypted at rest |
| **Message Queue** | Redis (optional) | Event streaming | Secure pub/sub |
| **Webhooks** | FastAPI Webhooks | Real-time event ingestion | HMAC signature verification |

## 🔄 Fraud Detection Workflow (End-to-End Security Flow)

### **Complete Attack Prevention Cycle**

```
Step 1: Event Detection
├─ Developer pushes code or creates merge request
├─ GitHub/GitLab sends webhook event
└─ HMAC signature verified (webhook authentication)

Step 2: Event Ingestion & Validation
├─ Backend receives webhook payload
├─ Metadata validated against threat database
└─ Event stored in audit trail

Step 3: Multi-Factor Risk Assessment
├─ 🤖 ML Analysis
│  ├─ Isolation Forest anomaly detection
│  ├─ Behavioral pattern matching
│  └─ Feature extraction
├─ 🛡️ Cybersecurity Analysis
│  ├─ Threat signature matching
│  ├─ Privilege escalation detection
│  ├─ Credential exposure check
│  └─ Supply chain vulnerability scan
└─ 🔗 Context Enrichment
   ├─ User role verification
   ├─ Historical behavior analysis
   └─ Temporal pattern recognition

Step 4: Risk Scoring
├─ Combine ML anomaly score (0-1.0)
├─ Add cybersecurity threat score
├─ Apply rule-based security policies
└─ Generate final risk score (0-1.0)

Step 5: Decision Making
├─ If risk >= CRITICAL threshold (>0.9)
│  ├─ Block deployment (optional)
│  ├─ Send emergency alerts
│  └─ Notify security team
├─ If risk >= HIGH threshold (>0.7)
│  ├─ Flag for review
│  ├─ Send alerts
│  └─ Log to blockchain
└─ If risk < LOW threshold (<0.3)
   └─ Allow with monitoring

Step 6: Blockchain Audit Logging
├─ Write immutable event record to blockchain
├─ Store event hash + metadata on Ethereum
├─ Generate audit trail certificate
└─ Enable compliance reporting

Step 7: Multi-Channel Alerting
├─ Slack notifications to security channel
├─ Email alerts to security team
├─ SIEM system integration
├─ Dashboard real-time updates
└─ Webhook notifications to external systems

Step 8: Incident Response & Forensics
├─ Security team reviews in dashboard
├─ Access immutable blockchain audit trail
├─ Generate compliance reports
└─ Prevent future similar attacks
```

### **Attack Prevention Example**

**Scenario**: Compromised developer account attempts to inject malware

```
Event: git push --force to main branch

ML Detection:
  ✗ Unusual time of commit (3 AM)
  ✗ Large file changes (10MB+ added)
  ✗ Sensitive file modification (credentials.json)
  ✗ Anomalous commit frequency
  → ML Risk Score: 0.92

Cybersecurity Detection:
  ✗ Credential exposure detected
  ✗ Privilege escalation attempt
  ✗ Known malware signatures matched
  ✗ Supply chain dependency modified
  → Threat Risk Score: 0.95

Combined Risk: 0.94 (CRITICAL)

Actions Taken:
  ✓ Deployment blocked
  ✓ Emergency alert sent to security team
  ✓ Event logged immutably on blockchain
  ✓ Slack notification: "🚨 CRITICAL: Potential malware injection detected"
  ✓ Compromised developer account flagged
  ✓ Audit trail generated for compliance
```

### Project Structure

```
├── backend/                          # Python FastAPI Backend
│   ├── src/
│   │   ├── api/
│   │   │   ├── fraud_controller.py  # Fraud detection endpoints
│   │   │   ├── alerts_controller.py # Alert management
│   │   │   ├── pipelines_controller.py # CI/CD pipeline monitoring
│   │   │   ├── webhook_handler.py   # GitLab/GitHub webhook ingestion
│   │   │   ├── simulate_routes.py   # Simulation for testing
│   │   │   └── websocket_handler.py # Real-time updates
│   │   ├── core/
│   │   │   ├── fraud_engine.py      # Core fraud detection logic
│   │   │   ├── ai_analyzer.py       # Machine learning analysis
│   │   │   ├── cybersecurity_analyzer.py # Threat detection & compliance
│   │   │   ├── risk_scorer.py       # Risk calculation engine
│   │   │   └── rule_engine.py       # Custom security rules
│   │   ├── services/
│   │   │   ├── blockchain_service.py # Ethereum/smart contract integration
│   │   │   ├── db_service.py        # Database operations
│   │   │   ├── gitlab_service.py    # GitLab API integration
│   │   │   ├── slack_service.py     # Slack notifications
│   │   │   └── email_service.py     # Email alerts
│   │   ├── middleware/
│   │   │   └── rate_limiter.py      # DDoS protection & rate limiting
│   │   └── utils/
│   │       ├── config.py            # Configuration management
│   │       ├── logger.py            # Logging setup
│   │       ├── threat_signatures.py # 1000+ threat patterns
│   │       └── validator.py         # Input validation & sanitization
│   ├── contracts/
│   │   └── FraudAuditLog.sol        # Blockchain smart contract for audit logs
│   ├── database/
│   │   └── schema.sql               # Database schema
│   ├── tests/
│   │   ├── unit/                    # Unit tests
│   │   └── integration/             # Integration tests
│   └── requirements.txt             # Python dependencies
│
├── frontend/                         # React.js Frontend Dashboard
│   ├── src/
│   │   ├── api/
│   │   │   ├── fraudController.js
│   │   │   ├── pipelineController.js
│   │   │   ├── simulateController.js
│   │   │   └── alertsController.js
│   │   ├── components/
│   │   │   ├── Dashboard.jsx        # Real-time security dashboard
│   │   │   ├── PipelineMonitor.jsx  # CI/CD pipeline status
│   │   │   ├── Alerts.jsx           # Alert management UI
│   │   │   ├── RiskGraph.jsx        # Risk trend visualization
│   │   │   └── Navigation.jsx       # UI navigation
│   │   ├── services/
│   │   │   └── apiClient.js         # API communication layer
│   │   └── App.jsx                  # Main application component
│   ├── public/                      # Static assets
│   └── package.json                 # Node.js dependencies
│
├── infra/                            # Infrastructure & Deployment
│   ├── docker/
│   │   ├── backend.Dockerfile       # Backend container
│   │   ├── frontend.Dockerfile      # Frontend container
│   │   └── docker-compose.yml       # Multi-container orchestration
│   ├── k8s/                         # Kubernetes manifests
│   └── terraform/                   # Infrastructure as Code
│
├── ml/                               # Machine Learning Models
│   ├── models/                      # Pre-trained ML models
│   ├── datasets/                    # Training datasets
│   └── notebooks/                   # Jupyter notebooks for analysis
│
├── contracts/                        # Smart Contracts (Blockchain)
│   └── FraudAuditLog.sol            # Solidity contract for immutable logs
│
├── security/                         # Security Configuration
│   ├── threat_patterns.json         # 1000+ threat signatures
│   ├── secure_coding_guidelines.md  # Security best practices
│   └── dependency_blacklist.txt     # Blocked vulnerable packages
│
├── docs/                             # Documentation
│   ├── 04_API_Documentation.md
│   ├── 05_Threat_Model.md
│   └── architecture/
│
├── scripts/                          # Utility Scripts
│   ├── generate_training_data.py    # Generate 1000-10000 training events
│   ├── deploy.sh                    # Deployment automation
│   └── seed_data.py                 # Database initialization
│
└── README.md                         # This file
```

### Technology Stack - Enterprise Security Edition

| Category | Technology | Usage | Security Component |
|----------|-----------|-------|-------------------|
| **Backend** | Python 3.12+ | Core framework | -  |
| **API Framework** | FastAPI 0.124 | High-performance REST APIs | Built-in security headers |
| **Async Processing** | Uvicorn | ASGI server | HTTPS support |
| **ML/AI** | Scikit-learn | Isolation Forest, anomaly detection | Fraud detection engine |
| **Data Processing** | Pandas, NumPy | Feature engineering | Data analysis |
| **Testing** | Pytest | Unit and integration testing | Code quality assurance |
| **Database** | SQLite/PostgreSQL | Persistent data storage | Encrypted at rest support |
| **Blockchain** | **Solidity** | **Smart contracts for audit logs** | **🔗 FraudAuditLog.sol** |
| **Web3** | **Web3.py 7.14** | **Ethereum interaction** | **Blockchain integration** |
| **Cryptography** | **cryptography 46+** | **Data encryption** | **Secure credential storage** |
| **Eth-Account** | **eth-account 0.13** | **Ethereum account management** | **Wallet/signing support** |
| **Webhooks** | FastAPI + HMAC | Secure event ingestion | Signature verification |
| **Frontend** | React 18.3 | Component-based UI | Modern security practices |
| **HTTP Client** | Axios | API communication | Request/response handling |
| **Visualization** | Recharts 2.12 | Data visualization | Risk analytics charts |
| **WebSocket** | Socket.io | Real-time updates | Live dashboard feeds |
| **Containerization** | Docker 25+ | Application deployment | Isolation & security |
| **Orchestration** | Kubernetes 1.28+ | Container orchestration | High availability |
| **Infrastructure** | Terraform | Infrastructure as Code | Cloud security |
| **CI/CD** | GitHub Actions | Automated testing & deployment | Pipeline security |
| **Secret Management** | Environment variables | Credential handling | Secure config |
| **Rate Limiting** | Custom middleware | DDoS protection | Abuse prevention |
| **Logging** | Python logging | Event tracking | Audit trail generation |
| **Monitoring** | CloudWatch/Prometheus | System metrics | Performance monitoring |

### **Key Security Technologies**

| Security Feature | Technology | Implementation |
|------------------|-----------|------------------|
| **Blockchain Audit Logs** | Solidity + Web3.py | Immutable event recording on Ethereum |
| **Threat Intelligence** | Custom threat database | 1000+ vulnerability signatures |
| **ML Anomaly Detection** | Isolation Forest | Unsupervised fraud pattern detection |
| **Credential Protection** | cryptography library | Encrypted storage and transmission |
| **Zero-Trust Auth** | JWT + OAuth2 | Role-based access control (RBAC) |
| **Rate Limiting** | Custom middleware | DDoS prevention & brute force protection |
| **HMAC Verification** | Python hmac | Webhook authentication |
| **Encryption** | Fernet + AES | Data encryption at rest & transit |
| **Input Validation** | Pydantic | Secure input sanitization |
| **Supply Chain Security** | Dependency scanning | Malicious package detection |

For more details, see [GitLab Tools Used](docs/07_GitLab_Tools_Used.pdf).

## 🚀 Quick Start

### Prerequisites
- **Docker & Docker Compose** 25+
- **Python** 3.12+
- **Node.js** 18+
- **Ethereum Network Access** (for blockchain audit logging)
  - Testnet (Sepolia/Goerli) or
  - Local (Ganache) for development
- **Web3 Wallet** (MetaMask, hardhat, etc.)

### Installation & Setup

#### 1. Clone the Repository
```bash
git clone https://github.com/Abdul9010150809/DEVOPS-Shield.git
cd DEVOPS-Shield
```

#### 2. Configure Environment
```bash
# Backend configuration
cp backend/.env.example backend/.env
# Edit with your settings:
# - ETHEREUM_RPC_URL (e.g., https://sepolia.infura.io/v3/YOUR_KEY)
# - SLACK_WEBHOOK_URL (optional)
# - EMAIL_CONFIG (optional)

# Frontend configuration
cp frontend/.env.example frontend/.env
# Set REACT_APP_API_URL=http://localhost:8000
```

#### 3. Deploy Smart Contract (Optional for Blockchain Audit)
```bash
cd backend/contracts
npm install -g hardhat
npx hardhat compile
npx hardhat deploy --network sepolia
# Save the FraudAuditLog contract address in .env
```

#### 4. Start All Services
```bash
# Option A: Using Docker Compose (Recommended)
docker-compose up -d

# Option B: Manual setup
cd backend && pip install -r requirements.txt && python -m uvicorn main:app --host 0.0.0.0 --port 8000 &
cd frontend && npm install && npm start
```

#### 5. Access Dashboard
```
Frontend:  http://localhost:3000
API Docs:  http://localhost:8000/docs
Backend:   http://localhost:8000
```

## ☁️ Deploying on Render

This repository includes a `render.yaml` blueprint so you can spin up both the FastAPI backend and the React frontend on Render with a single Blueprint deploy.

1. **Push your latest branch** to GitHub (Render syncs from the remote repository).
2. **Create a Render Blueprint** and point it at this repo. The preview will list two services defined in `render.yaml`:
  - `devops-shield-backend` (Python web service). Installs `backend/requirements.txt`, mounts a 1 GB persistent disk at `/var/data`, and starts Uvicorn bound to the platform `$PORT`.
  - `devops-shield-frontend` (static React site). Runs `npm install && npm run build` inside `frontend/` and publishes `frontend/build`.
3. **Review environment variables** before provisioning:
  - `ALLOWED_HOSTS` defaults to `localhost,127.0.0.1,*.onrender.com`, matching the FastAPI `TrustedHostMiddleware` update.
  - `CORS_ORIGINS` defaults to `https://devops-shield-frontend.onrender.com,http://localhost:3000`; adjust if you rename the static site.
  - `NODE_VERSION` pins the frontend build to Node 18 so Render uses a predictable toolchain.
  - `REACT_APP_API_BASE_URL` should reference the backend URL Render assigns (update after the first deploy if needed).
4. **Launch the blueprint.** The backend will populate `/var/data/fraud_logs.db` on the attached disk, preserving drills and alerts across redeploys, while the frontend immediately serves the built dashboard against the Render-hosted API.

### Render Troubleshooting

- `400 Invalid host header` → add your Render hostname to `ALLOWED_HOSTS` or use `*` temporarily.
- Secret rotation (Slack, GitLab, etc.) happens through Render’s dashboard—no code changes required.
- The SQLite file lives on the `fraud-logs` disk. Remove or resize the disk in Render if you need to reset state.

### Generate Training Data
```bash
# Generate 1,000 realistic fraud events for testing
python scripts/generate_training_data.py --events 1000

# Generate 5,000+ events for ML model training
python scripts/generate_training_data.py --events 5000
```

### Local Development Setup
- **Backend**: See [backend/README_BACKEND.md](backend/README_BACKEND.md)
- **Frontend**: See [frontend/README_FRONTEND.md](frontend/README_FRONTEND.md)
- **Blockchain**: See [contracts/README.md](contracts/README.md) for smart contract deployment

## 🚀 Production Deployment

The application is designed for enterprise deployment with complete blockchain audit trail support.

### Deployment Architecture

| Service | Deployment Platform | Status | Features |
|---------|-------------------|--------|----------|
| **Frontend Dashboard** | Render, Vercel, or CloudFront | Production | Real-time security monitoring |
| **Backend API** | Render, AWS Lambda, or K8s | Production | ML-powered fraud detection |
| **Blockchain Node** | Ethereum Mainnet/Testnet | Optional | Immutable audit logging |
| **Database** | PostgreSQL or Cloud SQL | Production | Encrypted persistence |
| **Redis Cache** | ElastiCache or Memorystore | Optional | Event queue & caching |

### Deployment Steps

#### 1. Backend Deployment
```bash
# Build Docker image
docker build -f infra/docker/backend.Dockerfile -t devops-shield-backend .

# Push to registry (e.g., Docker Hub, ECR)
docker push your-registry/devops-shield-backend:latest

# Deploy to Kubernetes, ECS, or Cloud Run
kubectl apply -f infra/k8s/backend-deployment.yaml
```

#### 2. Frontend Deployment
```bash
# Build React application
cd frontend && npm run build

# Deploy to CDN or static hosting
# GitHub Pages: npm run deploy
# Vercel: vercel deploy
# AWS S3: aws s3 sync build/ s3://your-bucket/
```

#### 3. Blockchain Configuration
```bash
# Deploy FraudAuditLog smart contract
cd backend/contracts
npx hardhat deploy --network mainnet

# Update environment with contract address
export FRAUD_AUDIT_CONTRACT=0x...
```

### Deployment Details
- **Frontend**: Served globally via CDN with API proxying
- **Backend**: Stateless FastAPI services for auto-scaling
- **Database**: PostgreSQL with encrypted backups and replication
- **Blockchain**: Ethereum mainnet/testnet integration for immutable records
- **Security**: TLS 1.3, CORS, rate limiting, CSRF protection
- **CI/CD**: Automated GitHub Actions pipeline with security checks

### Environment Variables
```env
# Ethereum Configuration
ETHEREUM_RPC_URL=https://mainnet.infura.io/v3/YOUR_KEY
FRAUD_AUDIT_CONTRACT=0x...
PRIVATE_KEY=your_wallet_private_key

# Database
DATABASE_URL=postgresql://user:pass@host/dbname
DATABASE_ENCRYPTION_KEY=your_key_here

# Notifications
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
EMAIL_FROM=security@company.com
SMTP_SERVER=smtp.gmail.com

# Security
JWT_SECRET=your_jwt_secret
API_RATE_LIMIT=100/hour
```

## 📚 Documentation

### Core Documentation
- [📋 API Documentation](docs/04_API_Documentation.md) - Complete REST API reference
- [🏛️ Architecture Overview](docs/01_Overview.pdf) - System design and components
- [⚠️ Threat Model](docs/05_Threat_Model.md) - Security threats and mitigations
- [🔄 CI/CD Flow](docs/06_CI_CD_Flow.pdf) - Pipeline automation details

### Security & Blockchain Documentation
- [🔗 Blockchain Integration Guide](BLOCKCHAIN_CYBERSECURITY_INTEGRATION.md) - Smart contract setup and Ethereum integration
- [🛡️ Cybersecurity Features](docs/cybersecurity/) - Threat detection, compliance, and security controls
- [📖 Real Data Integration Guide](REAL_DATA_INTEGRATION_GUIDE.md) - Live data generation and simulation
- [🔐 Security Best Practices](security/secure_coding_guidelines.md) - Secure development guidelines
- [📊 Threat Signatures Database](security/threat_patterns.json) - 1000+ vulnerability patterns

### Development Guides
- [🔧 Backend Development](backend/README_BACKEND.md) - Python/FastAPI setup and structure
- [⚛️ Frontend Development](frontend/README_FRONTEND.md) - React.js component architecture
- [⛓️ Smart Contract Development](contracts/README.md) - Solidity and blockchain deployment

## 🧪 Testing & Validation

### Unit & Integration Tests
```bash
# Backend tests with coverage
cd backend
python -m pytest tests/ -v --cov=src

# Frontend tests
cd frontend
npm test -- --coverage

# Integration tests
python -m pytest tests/integration/ -v
```

### Fraud Detection Testing
```bash
# Test ML model with simulated fraud events
python scripts/generate_training_data.py --events 1000
python scripts/test_fraud_engine.py

# Test API endpoints
curl http://localhost:8000/api/simulate/  # Generate fraud event
curl http://localhost:8000/api/fraud/stats  # Get statistics
curl http://localhost:8000/api/pipelines?limit=10  # Get pipelines
```

### Blockchain Contract Testing
```bash
# Test smart contract locally
cd backend/contracts
npx hardhat test

# Deploy to testnet
npx hardhat deploy --network sepolia

# Verify contract on Etherscan
npx hardhat verify --network sepolia DEPLOYED_ADDRESS
```

### Security Testing
```bash
# Dependency vulnerability scanning
pip install safety && safety check

# OWASP dependency check
npm audit

# Code security analysis
pip install bandit && bandit -r src/

# Smart contract security audit
npm install -g slither-analyzer
slither contracts/FraudAuditLog.sol
```

### Load & Performance Testing
```bash
# Load test the API
pip install locust
locust -f tests/load_test.py --host=http://localhost:8000

# Blockchain transaction throughput
python tests/blockchain/test_throughput.py
```

## 🔄 CI/CD

The project uses GitHub Actions for continuous integration and deployment. The CI pipeline includes:

- Automated testing for backend (Python/pytest) and frontend (React/Jest)
- Docker image builds for containerized deployment
- Linting and code quality checks

See [.github/workflows/ci.yml](.github/workflows/ci.yml) for the complete workflow configuration.

## 🤝 Contributing

We welcome security researchers and developers to contribute!

### Contribution Guidelines
1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/your-feature`)
3. **Follow** our [secure coding guidelines](security/secure_coding_guidelines.md)
4. **Write tests** for new features
5. **Run security checks** (bandit, safety, dependency scanning)
6. **Submit** a pull request with detailed description

### Security Contributions
- Report vulnerabilities via [SECURITY.md](SECURITY.md)
- Submit threat signatures for pattern database
- Help improve ML model accuracy with datasets
- Contribute smart contract audits or improvements

### Development Standards
- **Code**: Python 3.12+, FastAPI, React 18+
- **Testing**: 80%+ code coverage required
- **Security**: All PRs must pass security scanning
- **Documentation**: Update docs for new features
- **Commits**: Use conventional commit messages

## 🏆 Project Achievements

- **Enterprise-Grade Security**: Multi-layer threat detection system
- **Blockchain Innovation**: Immutable audit trails on Ethereum
- **AI-Powered Detection**: ML models trained on 10,000+ fraud events
- **Real-Time Monitoring**: WebSocket support for live dashboards
- **Compliance Ready**: GDPR, SOC2, HIPAA audit trail support
- **Production Deployment**: Running on enterprise infrastructure

## 📜 License

MIT License - see [LICENSE](LICENSE) file for details.

### License Highlights
- ✅ Free for commercial use
- ✅ Modify and distribute
- ✅ Use in private projects
- ℹ️ Include license copy
- ℹ️ Maintain copyright notice

---

## 🎓 References & Credits

### Original Project
This project was developed as part of the **GitLab Hackathon** conducted by **IIT Bombay**.

### Key Contributors
- **Lead Developer**: Abdul9010150809
- **Security Advisors**: Cybersecurity team
- **Blockchain Integration**: Web3 developers
- **ML/AI Team**: Data scientists and ML engineers

### Research & Inspiration
- [GitLab DevSecOps Best Practices](https://about.gitlab.com/solutions/devsecops/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [Ethereum Smart Contract Security](https://ethereum.org/en/developers/docs/smart-contracts/security/)
- [ML Fraud Detection Papers](https://arxiv.org/)

---

## 📞 Support & Contact

### Get Help
- **Documentation**: Check [docs/](docs/) folder
- **Issues**: Report bugs on [GitHub Issues](https://github.com/Abdul9010150809/DEVOPS-Shield/issues)
- **Discussions**: Join [GitHub Discussions](https://github.com/Abdul9010150809/DEVOPS-Shield/discussions)
- **Email**: security@devops-shield.io

### Stay Updated
- ⭐ Star the repository
- 👁️ Watch for updates
- 🔔 Subscribe to releases

---

## 🎯 Roadmap

### Coming Soon
- [ ] Advanced ML models (LSTM, GRU for temporal patterns)
- [ ] Multi-blockchain support (Polygon, Arbitrum)
- [ ] Enhanced SIEM integration
- [ ] Mobile app for alerts
- [ ] Custom threat rule builder UI
- [ ] Advanced analytics and reporting
- [ ] Federated learning for privacy-preserving training

---

**🛡️ DEVOPS-Shield: Protecting DevOps from the Inside**

*Enterprise Security. AI-Powered. Blockchain-Backed.*
