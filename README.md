# 🛡️ DevOps Shield - AI-Powered Security Platform

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18+-61DAFB.svg)](https://reactjs.org/)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-2496ED.svg)](https://www.docker.com/)
[![Blockchain](https://img.shields.io/badge/Blockchain-Ethereum-627EEA.svg)](https://ethereum.org/)
[![Security](https://img.shields.io/badge/Security-Zero--Trust-red.svg)]()

---

## 🏆 Hackathon Excellence

**Event:** MindSprint 2K25 Hackathon  
**Team:** DevOps Security Experts  
**Achievement:** 🥇 **First Place - Security Innovation**

**Team Members:**
- **Shaik. Muzkeer** - Backend & Security Architecture
- **Shaik. Abdul Sammed** - Frontend & UI/UX Design
- **Suhail. B. K** - Blockchain & Integration

---

## 🎯 Project Overview

DevOps Shield is a **zero-trust security layer** for CI/CD pipelines that combines advanced AI-powered threat detection with blockchain-backed immutability. The platform provides real-time fraud detection, supply chain security, and comprehensive risk intelligence from commit to release.

### 🌟 Key Features

#### 🤖 AI-Powered Threat Intelligence
- **Machine Learning Models** for anomaly detection and pattern recognition
- **Real-time Risk Scoring** with configurable thresholds
- **Behavioral Analysis** for identifying suspicious activities
- **Predictive Analytics** for proactive threat prevention

#### 🔒 Zero-Trust Security Architecture
- **Source Integrity Scoring** with cryptographic verification
- **Dependency Whitelisting** and vulnerability scanning
- **Runner Verification** and secure execution environments
- **Multi-Layer Authentication** and access controls

#### ⛓️ Blockchain-Backed Auditing
- **Immutable Ledger** for security events and transactions
- **Smart Contract Integration** for automated compliance
- **Cryptographic Proofs** for data integrity verification
- **Decentralized Storage** for audit trails

#### 🧪 Advanced Simulation Lab
- **Attack Scenarios** including supply-chain, secret-leak, and rogue-runner drills
- **Offline Capability** with deterministic fallbacks
- **Custom Threat Models** and simulation parameters
- **Performance Benchmarking** and stress testing

#### 📊 Comprehensive Observability
- **Real-time Dashboards** with interactive visualizations
- **Centralized Logging** with structured data format
- **WebSocket Streaming** for live updates
- **Performance Metrics** and health monitoring

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    🌐 Frontend (React 18)                        │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐   │
│  │   Dashboard     │  │  Simulation Lab │  │  Security UI   │   │
│  │   - Real-time   │  │  - Attack Sims  │  │  - Risk Scores  │   │
│  │   - Analytics   │  │  - Threat Models│  │  - Zero Trust   │   │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                   🔧 Backend (FastAPI)                           │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐   │
│  │   API Gateway   │  │  Security Core  │  │  AI/ML Engine    │   │
│  │  - REST APIs    │  │  - Zero Trust   │  │  - Anomaly Det. │   │
│  │  - WebSocket    │  │  - Risk Engine  │  │  - Pattern Rec. │   │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘   │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐   │
│  │   Middleware    │  │   Services      │  │   Utils         │   │
│  │  - Rate Limiter │  │  - Blockchain   │  │  - Logger       │   │
│  │  - Auth         │  │  - Database     │  │  - Validators   │   │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                   🗄️ Infrastructure Layer                        │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐   │
│  │   Blockchain     │  │   Database       │  │   Storage        │   │
│  │  - Ethereum      │  │  - PostgreSQL    │  │  - File System   │   │
│  │  - Smart Contracts│  │  - Redis Cache   │  │  - Cloud Storage │   │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
devops-shield/
├── 📁 frontend/                    # React 18 Frontend Application
│   ├── 📁 public/
│   │   ├── 📄 index.html          # Enhanced HTML with SEO & Accessibility
│   │   ├── 📄 manifest.json       # PWA Manifest
│   │   └── 📁 assets/              # Static assets (icons, images)
│   ├── 📁 src/
│   │   ├── 📄 App.jsx              # Main React application
│   │   ├── 📁 pages/               # Application pages
│   │   │   ├── 📄 Dashboard.jsx     # Security dashboard
│   │   │   ├── 📄 Simulation.jsx    # Attack simulation lab
│   │   │   ├── 📄 Security.jsx      # Security configuration
│   │   │   └── 📄 Analytics.jsx      # Analytics and reporting
│   │   ├── 📁 components/          # Reusable UI components
│   │   │   ├── 📄 SecurityCard.jsx  # Security metric cards
│   │   │   ├── 📄 ThreatChart.jsx   # Threat visualization
│   │   │   └── 📄 AlertPanel.jsx    # Alert management
│   │   ├── 📁 services/            # API and business logic
│   │   │   ├── 📄 apiClient.js      # HTTP client with error handling
│   │   │   ├── 📄 zeroTrustService.js # Zero-trust API integration
│   │   │   └── 📄 websocketService.js # Real-time updates
│   │   └── 📁 utils/               # Utility functions
│   ├── 📄 package.json             # Frontend dependencies
│   └── 📄 Dockerfile               # Frontend container
│
├── 📁 backend/                     # FastAPI Backend Application
│   ├── 📄 main.py                   # Application entry point
│   ├── 📄 start.sh                  # Startup script
│   ├── 📄 requirements.txt          # Python dependencies
│   ├── 📁 src/
│   │   ├── 📁 api/                  # API routers
│   │   │   ├── 📄 simulate.py       # Attack simulation endpoints
│   │   │   ├── 📄 fraud.py          # Fraud detection endpoints
│   │   │   ├── 📄 alerts.py         # Alert management
│   │   │   ├── 📄 zero_trust.py     # Zero-trust controls
│   │   │   └── 📄 analytics.py      # Analytics and reporting
│   │   ├── 📁 core/                 # Core security logic
│   │   │   ├── 📄 fraud_engine.py   # Fraud detection engine
│   │   │   ├── 📄 anomaly_detector.py # ML-based anomaly detection
│   │   │   ├── 📄 risk_scorer.py    # Risk scoring algorithms
│   │   │   └── 📄 threat_models.py   # Threat modeling
│   │   ├── 📁 security/             # Security orchestrator
│   │   │   ├── 📄 zero_trust.py     # Zero-trust implementation
│   │   │   ├── 📄 pipeline_guard.py  # Pipeline security
│   │   │   └── 📄 access_control.py  # Access management
│   │   ├── 📁 services/             # External services
│   │   │   ├── 📄 blockchain.py      # Blockchain integration
│   │   │   ├── 📄 database.py       # Database operations
│   │   │   ├── 📄 email.py          # Email notifications
│   │   │   └── 📄 slack.py          # Slack integration
│   │   ├── 📁 middleware/           # Custom middleware
│   │   │   ├── 📄 rate_limiter.py    # DoS protection
│   │   │   ├── 📄 auth.py           # Authentication
│   │   │   └── 📄 logging.py        # Request logging
│   │   └── 📁 utils/                # Utilities
│   │       ├── 📄 config.py         # Configuration management
│   │       ├── 📄 logger.py         # Structured logging
│   │       ├── 📄 validators.py     # Input validation
│   │       └── 📄 threat_signatures.py # Threat patterns
│   └── 📄 Dockerfile               # Backend container
│
├── 📁 infra/                        # Infrastructure as Code
│   ├── 📁 docker/
│   │   ├── 📄 backend.Dockerfile    # Backend container definition
│   │   ├── 📄 frontend.Dockerfile   # Frontend container definition
│   │   └── 📄 docker-compose.yml    # Multi-container setup
│   ├── 📄 railway.toml              # Railway deployment config
│   └── 📄 Dockerfile                # All-in-one container
│
├── 📁 docs/                         # Documentation
│   ├── 📄 API.md                   # API documentation
│   ├── 📄 SECURITY.md              # Security architecture
│   ├── 📄 DEPLOYMENT.md            # Deployment guide
│   └── 📄 CONTRIBUTING.md          # Contributing guidelines
│
├── 📄 README.md                     # Project documentation
├── 📄 .gitignore                    # Git ignore rules
└── 📄 LICENSE                       # MIT License
```

---

## 🚀 Quick Start Guide

### 📋 Prerequisites
- **Docker** & **Docker Compose**
- **Node.js** 16+ for frontend development
- **Python** 3.9+ for backend development
- **Ethereum** wallet (for blockchain features)

### 🔧 Local Development Setup

1. **🔽 Clone Repository**
   ```bash
   git clone https://github.com/yourusername/devops-shield.git
   cd devops-shield
   ```

2. **🐳 Docker Compose Setup**
   ```bash
   # Start all services
   docker-compose up -d
   
   # View logs
   docker-compose logs -f
   
   # Stop services
   docker-compose down
   ```

3. **🔧 Manual Setup (Optional)**
   ```bash
   # Backend setup
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ./start.sh
   
   # Frontend setup (new terminal)
   cd frontend
   npm install
   npm start
   ```

### 🌐 Access Points

- **Frontend Dashboard**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/health

---

## 🔧 Configuration

### 🌍 Environment Variables

#### Backend Configuration
```bash
# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/devops_shield
REDIS_URL=redis://localhost:6379

# Security Configuration
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key
BLOCKCHAIN_ENABLED=true
ETHEREUM_RPC_URL=https://mainnet.infura.io/v3/YOUR-PROJECT-ID

# External Services
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK
EMAIL_SMTP_HOST=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_USERNAME=your-email@gmail.com
EMAIL_PASSWORD=your-app-password

# Development Settings
DEBUG=false
LOG_LEVEL=INFO
RATE_LIMIT_PER_MINUTE=100
```

#### Frontend Configuration
```bash
# API Configuration
REACT_APP_API_URL=http://localhost:8000
REACT_APP_WS_URL=ws://localhost:8000/ws

# Feature Flags
REACT_APP_ENABLE_BLOCKCHAIN=true
REACT_APP_ENABLE_SIMULATIONS=true
REACT_APP_ENABLE_ANALYTICS=true

# UI Configuration
REACT_APP_THEME=dark
REACT_APP_REFRESH_INTERVAL=5000
```

---

## 🔐 Security Features

### 🛡️ Zero-Trust Architecture

#### Source Integrity Verification
```python
# Cryptographic hash verification for source code
def verify_source_integrity(commit_hash: str, expected_hash: str) -> bool:
    calculated_hash = sha256(commit_hash.encode()).hexdigest()
    return calculated_hash == expected_hash
```

#### Dependency Security Scanning
```python
# Automated vulnerability scanning for dependencies
def scan_dependencies(dependencies: List[str]) -> SecurityReport:
    vulnerabilities = []
    for dep in dependencies:
        vuln = check_vulnerability_database(dep)
        if vuln.severity >= Severity.MEDIUM:
            vulnerabilities.append(vuln)
    return SecurityReport(vulnerabilities)
```

#### Pipeline Security Controls
```python
# Multi-factor authentication for pipeline execution
def authenticate_pipeline_execution(pipeline_id: str, credentials: Credentials) -> bool:
    # Verify multiple authentication factors
    return verify_api_key(credentials.api_key) and \
           verify_jwt_token(credentials.jwt_token) and \
           verify_blockchain_signature(credentials.signature)
```

### 🤖 AI-Powered Threat Detection

#### Anomaly Detection
```python
# Machine learning-based anomaly detection
class AnomalyDetector:
    def __init__(self):
        self.model = IsolationForest(contamination=0.1)
        self.scaler = StandardScaler()
    
    def detect_anomalies(self, metrics: List[Dict]) -> List[Anomaly]:
        features = self.extract_features(metrics)
        scaled_features = self.scaler.transform(features)
        predictions = self.model.predict(scaled_features)
        
        anomalies = []
        for i, pred in enumerate(predictions):
            if pred == -1:  # Anomaly detected
                anomalies.append(Anomaly(
                    timestamp=metrics[i]['timestamp'],
                    severity=self.calculate_severity(metrics[i]),
                    description=self.generate_description(metrics[i])
                ))
        return anomalies
```

#### Risk Scoring Algorithm
```python
# Comprehensive risk scoring system
def calculate_risk_score(event: SecurityEvent) -> RiskScore:
    factors = {
        'severity': event.severity * 0.3,
        'frequency': event.frequency * 0.2,
        'impact': event.impact * 0.25,
        'likelihood': event.likelihood * 0.15,
        'mitigation': event.mitigation * 0.1
    }
    
    base_score = sum(factors.values())
    
    # Apply contextual modifiers
    if event.source == 'external':
        base_score *= 1.2
    if event.time_of_day in ['night', 'weekend']:
        base_score *= 1.1
    
    return RiskScore(
        score=min(base_score, 100),
        level=determine_risk_level(base_score),
        recommendations=generate_recommendations(event)
    )
```

---

## ⛓️ Blockchain Integration

### 🔗 Smart Contract Implementation

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract DevOpsShield {
    struct SecurityEvent {
        uint256 timestamp;
        string eventType;
        address source;
        bytes32 dataHash;
        uint8 severity;
        bool resolved;
    }
    
    mapping(bytes32 => SecurityEvent) public events;
    mapping(address => uint256) public reputationScores;
    
    event SecurityEventLogged(
        bytes32 indexed eventId,
        string eventType,
        address indexed source,
        uint8 severity
    );
    
    function logSecurityEvent(
        string memory eventType,
        bytes32 dataHash,
        uint8 severity
    ) public returns (bytes32) {
        bytes32 eventId = keccak256(
            abi.encodePacked(block.timestamp, msg.sender, dataHash)
        );
        
        events[eventId] = SecurityEvent({
            timestamp: block.timestamp,
            eventType: eventType,
            source: msg.sender,
            dataHash: dataHash,
            severity: severity,
            resolved: false
        });
        
        emit SecurityEventLogged(eventId, eventType, msg.sender, severity);
        return eventId;
    }
    
    function verifyEventIntegrity(
        bytes32 eventId,
        bytes memory data
    ) public view returns (bool) {
        SecurityEvent memory event = events[eventId];
        bytes32 computedHash = keccak256(data);
        return event.dataHash == computedHash;
    }
}
```

### 📊 Blockchain Analytics

```python
# Blockchain transaction monitoring
class BlockchainMonitor:
    def __init__(self, web3_provider: str):
        self.web3 = Web3(HTTPProvider(web3_provider))
        self.contract = self.web3.eth.contract(
            address=CONTRACT_ADDRESS,
            abi=CONTRACT_ABI
        )
    
    def get_security_events(self, from_block: int, to_block: int) -> List[Dict]:
        events = self.contract.events.SecurityEventLogged.get_logs(
            fromBlock=from_block,
            toBlock=to_block
        )
        
        return [
            {
                'eventId': event.args.eventId.hex(),
                'eventType': event.args.eventType,
                'source': event.args.source,
                'severity': event.args.severity,
                'timestamp': event.args.timestamp
            }
            for event in events
        ]
    
    def verify_chain_integrity(self) -> bool:
        latest_block = self.web3.eth.block_number
        block_hash = self.web3.eth.get_block(latest_block)['hash']
        
        # Verify block hash against expected value
        return self.verify_expected_hash(block_hash.hex())
```

---

## 📊 Analytics & Monitoring

### 📈 Real-time Dashboard Features

#### Security Metrics
- **Threat Detection Rate**: Real-time monitoring of identified threats
- **False Positive Rate**: Accuracy measurement of detection algorithms
- **Response Time**: Average time from detection to resolution
- **Risk Distribution**: Visualization of risk levels across components

#### Performance Metrics
- **API Response Time**: Latency monitoring for all endpoints
- **Database Performance**: Query optimization and indexing effectiveness
- **Blockchain Sync Time**: Time to record and retrieve blockchain data
- **System Resource Usage**: CPU, memory, and network utilization

### 🔍 Advanced Analytics

#### Trend Analysis
```python
# Security trend analysis
class SecurityAnalytics:
    def analyze_trends(self, time_range: str) -> TrendReport:
        data = self.get_security_data(time_range)
        
        return TrendReport(
            threat_trends=self.calculate_threat_trends(data),
            vulnerability_trends=self.calculate_vulnerability_trends(data),
            compliance_trends=self.calculate_compliance_trends(data),
            recommendations=self.generate_trend_recommendations(data)
        )
    
    def predict_future_threats(self) -> ThreatPrediction:
        historical_data = self.get_historical_data(days=90)
        model = self.train_prediction_model(historical_data)
        
        return model.predict_next_period()
```

#### Compliance Reporting
```python
# Automated compliance reporting
class ComplianceReporter:
    def generate_compliance_report(self, standard: str) -> ComplianceReport:
        requirements = self.get_compliance_requirements(standard)
        current_state = self.assess_current_state(requirements)
        
        return ComplianceReport(
            standard=standard,
            compliance_score=self.calculate_compliance_score(current_state),
            gaps=self.identify_compliance_gaps(requirements, current_state),
            remediation_plan=self.generate_remediation_plan(gaps),
            audit_trail=self.generate_audit_trail()
        )
```

---

## 🧪 Attack Simulation Lab

### 🎯 Simulation Scenarios

#### Supply Chain Attack Simulation
```python
class SupplyChainSimulator:
    def simulate_dependency_compromise(self, target_dependency: str) -> SimulationResult:
        # Simulate compromised dependency
        compromised_package = self.create_malicious_package(target_dependency)
        
        # Test detection capabilities
        detection_result = self.test_detection(compromised_package)
        
        return SimulationResult(
            scenario="Dependency Compromise",
            detection_time=detection_result.time_to_detect,
            impact_assessment=self.assess_impact(compromised_package),
            mitigation_effectiveness=self.test_mitigation(compromised_package)
        )
```

#### Secret Leak Simulation
```python
class SecretLeakSimulator:
    def simulate_secret_exposure(self, secret_type: str) -> SimulationResult:
        # Simulate exposed secrets
        exposed_secrets = self.generate_exposed_secrets(secret_type)
        
        # Test detection and response
        detection_result = self.test_secret_detection(exposed_secrets)
        response_result = self.test_incident_response(exposed_secrets)
        
        return SimulationResult(
            scenario="Secret Leak",
            secrets_exposed=len(exposed_secrets),
            detection_rate=detection_result.detection_rate,
            response_time=response_result.response_time,
            data_breach_risk=self.assess_breach_risk(exposed_secrets)
        )
```

---

## 🚀 Deployment Guide

### 🐳 Docker Deployment

#### Multi-Container Setup
```yaml
# docker-compose.yml
version: '3.8'

services:
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=http://backend:8000
    depends_on:
      - backend
    networks:
      - devops-shield-network

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:5432/devops_shield
      - REDIS_URL=redis://redis:6379
      - BLOCKCHAIN_ENABLED=true
    depends_on:
      - postgres
      - redis
    networks:
      - devops-shield-network

  postgres:
    image: postgres:15
    environment:
      - POSTGRES_DB=devops_shield
      - POSTGRES_USER=devops
      - POSTGRES_PASSWORD=secure_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - devops-shield-network

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    networks:
      - devops-shield-network

volumes:
  postgres_data:

networks:
  devops-shield-network:
    driver: bridge
```

#### Production Deployment
```bash
# Production deployment with Railway
railway up

# Or with Docker Swarm
docker swarm init
docker stack deploy -c docker-compose.yml devops-shield
```

### ☁️ Cloud Deployment

#### AWS Deployment
```bash
# Deploy to AWS ECS
aws ecs create-cluster --cluster-name devops-shield
aws ecs register-task-definition --cli-input-json task-definition.json
aws ecs create-service --cluster devops-shield --service-name devops-shield-api
```

#### Kubernetes Deployment
```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: devops-shield-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: devops-shield
  template:
    metadata:
      labels:
        app: devops-shield
    spec:
      containers:
      - name: backend
        image: devops-shield/backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: devops-shield-secrets
              key: database-url
```

---

## 🧪 Testing & Quality Assurance

### 🧪 Unit Tests
```python
# Test fraud detection engine
class TestFraudEngine(unittest.TestCase):
    def setUp(self):
        self.engine = FraudEngine()
    
    def test_anomaly_detection(self):
        # Test with known anomaly patterns
        anomalous_data = self.generate_anomalous_data()
        result = self.engine.detect_fraud(anomalous_data)
        
        self.assertTrue(result.is_fraud)
        self.assertGreater(result.confidence, 0.8)
    
    def test_normal_behavior(self):
        # Test with normal behavior patterns
        normal_data = self.generate_normal_data()
        result = self.engine.detect_fraud(normal_data)
        
        self.assertFalse(result.is_fraud)
        self.assertLess(result.confidence, 0.3)
```

### 🔍 Integration Tests
```python
# Test API integration
class TestAPIIntegration(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
    
    def test_security_endpoint(self):
        response = self.client.post('/api/security/scan', 
                                  json={'pipeline_id': 'test-123'})
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('risk_score', response.json())
    
    def test_blockchain_integration(self):
        response = self.client.post('/api/blockchain/log-event',
                                  json={'event_type': 'test', 'data': 'test-data'})
        
        self.assertEqual(response.status_code, 201)
        self.assertIn('transaction_hash', response.json())
```

### 📊 Performance Testing
```python
# Load testing with Locust
class SecurityAPILoadTest(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        self.client.post('/api/auth/login', json={
            'username': 'test_user',
            'password': 'test_password'
        })
    
    @task
    def scan_pipeline(self):
        self.client.get('/api/security/scan/pipeline-123')
    
    @task
    def check_threats(self):
        self.client.get('/api/threats/active')
```

---

## 📞 Support & Community

### 🐛 Issue Reporting
- **Bug Reports**: [GitHub Issues](https://github.com/yourusername/devops-shield/issues)
- **Feature Requests**: [GitHub Discussions](https://github.com/yourusername/devops-shield/discussions)
- **Security Issues**: security@devops-shield.com (private, for security vulnerabilities)

### 📚 Documentation
- **API Documentation**: [https://docs.devops-shield.com/api](https://docs.devops-shield.com/api)
- **Security Guide**: [https://docs.devops-shield.com/security](https://docs.devops-shield.com/security)
- **Deployment Guide**: [https://docs.devops-shield.com/deployment](https://docs.devops-shield.com/deployment)

### 🤝 Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **MindSprint 2K25 Hackathon** for the opportunity and platform
- **FastAPI Team** for the excellent web framework
- **React Community** for the amazing UI library
- **Ethereum Foundation** for blockchain infrastructure
- **Open Source Contributors** for tools and libraries

---

<div align="center">

## 🛡️ Securing DevOps Pipelines with AI & Blockchain 🛡️

**Zero-Trust Security • Real-time Detection • Immutable Auditing**

*Empowering organizations with next-generation security for CI/CD pipelines*

[**🚀 Live Demo**](https://devops-shield.example.com) • 
[**📚 Documentation**](https://docs.devops-shield.com) • 
[**💻 Source Code**](https://github.com/yourusername/devops-shield)

### 🎯 Our Mission
*"Building the future of DevOps security through AI-powered threat detection and blockchain-backed immutability."*

</div>

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
