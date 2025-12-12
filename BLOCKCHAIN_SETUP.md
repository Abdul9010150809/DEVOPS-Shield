# Blockchain Setup & Configuration Guide

## Overview

This guide covers setting up blockchain integration for immutable fraud detection audit trails in DevOps Shield.

## Smart Contracts

### FraudAuditLogV2.sol

Enhanced Solidity contract with enterprise features:
- **Event Chaining**: Immutable linked event logs with cryptographic hash chaining
- **Multi-Signature Verification**: Multi-party verification for audit authority
- **Audit Report Generation**: Automated report aggregation and signing
- **Status Tracking**: Event lifecycle (Pending, Verified, Escalated, Resolved)
- **Risk Scoring**: Quantitative risk assessment on-chain

**Location**: `backend/contracts/FraudAuditLogV2.sol`

**Key Functions**:
```solidity
// Log security event with chaining
function logSecurityEvent(
    string memory eventType,
    string memory severity,
    bytes32 dataHash,
    uint256 riskScore,
    string memory repository
) external returns (uint256)

// Verify event with multi-signature
function verifyEvent(uint256 eventId, string memory signatureHash) external

// Escalate critical events
function escalateEvent(uint256 eventId, string memory reason) external

// Generate audit reports
function generateAuditReport(
    string memory reportType,
    uint256[] memory eventIds,
    string memory summary
) external returns (uint256)

// Query events by severity, risk, status
function getEventsBySeverity(string memory severity) external view returns (uint256[])
function getHighRiskEvents(uint256 threshold) external view returns (uint256[])
function getUnresolvedEvents() external view returns (uint256[])
```

## Deployment Options

### Option 1: Testnet Deployment (Recommended for Development)

Deploy to Ethereum testnet (Goerli/Sepolia) using free Infura service.

#### Prerequisites:
- Node.js v16+
- Hardhat or Truffle
- MetaMask or hardware wallet

#### Steps:

1. **Install dependencies**:
```bash
npm install --save-dev hardhat @openzeppelin/contracts ethers
npx hardhat
```

2. **Create deployment script** (`scripts/deploy.js`):
```javascript
async function main() {
  console.log("Deploying FraudAuditLogV2...");
  
  const FraudAuditLogV2 = await ethers.getContractFactory("FraudAuditLogV2");
  const contract = await FraudAuditLogV2.deploy();
  
  await contract.deployed();
  
  console.log("FraudAuditLogV2 deployed to:", contract.address);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
```

3. **Deploy to Sepolia testnet**:
```bash
npx hardhat run scripts/deploy.js --network sepolia
```

4. **Update environment variables**:
```env
BLOCKCHAIN_PROVIDER_URL=https://sepolia.infura.io/v3/YOUR_INFURA_KEY
BLOCKCHAIN_CONTRACT_ADDRESS=0x<deployed_address>
BLOCKCHAIN_NETWORK=sepolia
BLOCKCHAIN_PRIVATE_KEY=0x<deployer_private_key>
BLOCKCHAIN_ENABLED=true
```

### Option 2: Local Development (Ganache)

For local testing without gas costs.

#### Prerequisites:
- Ganache CLI or GUI
- Python web3.py library

#### Steps:

1. **Start Ganache**:
```bash
ganache-cli --deterministic --accounts 10
```

2. **Configure environment**:
```env
BLOCKCHAIN_PROVIDER_URL=http://localhost:8545
BLOCKCHAIN_NETWORK=ganache
BLOCKCHAIN_CONTRACT_ADDRESS=0x<deployed_address>
BLOCKCHAIN_PRIVATE_KEY=0x<ganache_account_key>
BLOCKCHAIN_ENABLED=true
```

3. **Deploy contract locally**:
```bash
# Using hardhat
npx hardhat run scripts/deploy.js --network localhost
```

### Option 3: Production Mainnet (Ethereum)

For production fraud detection on mainnet.

#### Prerequisites:
- Significant ETH for gas fees (varies by network activity)
- Hardware wallet (Ledger/Trezor recommended)
- Audited contract code

#### Steps:

1. **Professional security audit**:
   - Use firms like OpenZeppelin, Trail of Bits, Consensys Diligence
   - Address vulnerabilities before deployment

2. **Deploy with deployment service**:
```bash
npx hardhat run scripts/deploy.js --network mainnet
```

3. **Verify contract on Etherscan**:
```bash
npx hardhat verify --network mainnet <contract_address> \
  --constructor-args arguments.js
```

4. **Update production env**:
```env
BLOCKCHAIN_PROVIDER_URL=https://eth-mainnet.alchemyapi.io/v2/YOUR_ALCHEMY_KEY
BLOCKCHAIN_NETWORK=mainnet
BLOCKCHAIN_CONTRACT_ADDRESS=0x<mainnet_address>
BLOCKCHAIN_PRIVATE_KEY=0x<production_key>
BLOCKCHAIN_ENABLED=true
```

## Backend Integration

### Environment Configuration

**File**: `backend/.env`

```env
# Blockchain Settings
BLOCKCHAIN_ENABLED=true
BLOCKCHAIN_PROVIDER_URL=https://sepolia.infura.io/v3/YOUR_INFURA_KEY
BLOCKCHAIN_NETWORK=sepolia
BLOCKCHAIN_CONTRACT_ADDRESS=0x<deployed_contract_address>
BLOCKCHAIN_PRIVATE_KEY=0x<account_private_key>
```

### BlockchainAuditService

Python service for blockchain interaction:
- Located: `backend/src/services/blockchain_service_v2.py`
- Handles Web3 connection, contract calls, event logging
- Automatic fallback to local storage if blockchain unavailable

**Usage Example**:
```python
from src.services.blockchain_service_v2 import BlockchainAuditService

# Initialize service
blockchain = BlockchainAuditService()

# Log fraud event
event_data = {
    'event_type': 'credential_compromise',
    'risk_score': 0.85,
    'repository': 'production-api',
    'rule_violations': ['suspicious_commit', 'unauthorized_deploy']
}

result = blockchain.log_fraud_event(event_data, repository='production-api')
# Returns: {'transaction_hash': '0x...', 'block_number': 12345, ...}

# Get audit trail
audit_events = blockchain.get_audit_trail(
    repository='production-api',
    severity='high',
    risk_threshold=70
)

# Get blockchain stats
stats = blockchain.get_blockchain_stats()
```

### API Endpoints

**Blockchain Controller**: `backend/src/api/blockchain_controller.py`

Endpoints:

```
POST   /api/blockchain/events
       - Log security event on blockchain
       
POST   /api/blockchain/events/verify
       - Verify event with multi-signature
       
GET    /api/blockchain/audit-trail
       - Retrieve audit trail with filtering
       
GET    /api/blockchain/events/{event_id}
       - Get specific event details
       
GET    /api/blockchain/stats
       - Get blockchain statistics
       
GET    /api/blockchain/health
       - Check blockchain service health
       
POST   /api/blockchain/test-connection
       - Test blockchain provider connection
```

**Example Usage**:
```bash
# Log event
curl -X POST http://localhost:8000/api/blockchain/events \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "fraud_detected",
    "risk_score": 0.85,
    "repository": "production-app",
    "rule_violations": ["suspicious_commit"],
    "message": "Credential compromise detected"
  }'

# Get audit trail
curl http://localhost:8000/api/blockchain/audit-trail?severity=high

# Check health
curl http://localhost:8000/api/blockchain/health
```

## Frontend Integration

### BlockchainDashboard Component

React component for blockchain UI:
- Location: `frontend/src/components/BlockchainDashboard.jsx`
- Displays: blockchain stats, audit trail, event verification, contract status
- Features: event filtering, real-time refresh, immutable log display

**Integration in App.jsx**:
```jsx
import BlockchainDashboard from './components/BlockchainDashboard.jsx';

// Add to VIEWS and navItems
const VIEWS = { ..., BLOCKCHAIN: 'blockchain' };
const navItems = [..., { id: VIEWS.BLOCKCHAIN, label: 'Blockchain Audit' }];

// Add switch case
case VIEWS.BLOCKCHAIN:
  content = <BlockchainDashboard />;
  break;
```

## Testing Blockchain Integration

### Unit Tests

**File**: `backend/tests/unit/test_blockchain_service.py`

```python
import pytest
from src.services.blockchain_service_v2 import BlockchainAuditService

def test_calculate_data_hash():
    service = BlockchainAuditService()
    data = {'event_type': 'test', 'risk_score': 0.5}
    hash_result = service.calculate_data_hash(data)
    assert len(hash_result) == 64  # SHA256 hex length
    assert isinstance(hash_result, str)

def test_blockchain_stats():
    service = BlockchainAuditService()
    stats = service.get_blockchain_stats()
    assert 'connected' in stats
    assert 'provider' in stats
```

### Integration Tests

**File**: `backend/tests/integration/test_blockchain_integration.py`

```python
import pytest
import asyncio
from fastapi.testclient import TestClient
from backend.main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_blockchain_health(client):
    response = client.get("/api/blockchain/health")
    assert response.status_code == 200
    assert "healthy" in response.json()

def test_log_security_event(client):
    event_data = {
        "event_type": "fraud_detected",
        "risk_score": 0.8,
        "repository": "test-repo"
    }
    response = client.post("/api/blockchain/events", json=event_data)
    assert response.status_code == 200
    assert "transaction_hash" in response.json() or "data_hash" in response.json()
```

### Run Tests

```bash
# Unit tests
pytest backend/tests/unit/test_blockchain_service.py -v

# Integration tests
pytest backend/tests/integration/test_blockchain_integration.py -v

# All blockchain tests
pytest backend/tests -k blockchain -v
```

## Security Best Practices

### Private Key Management

❌ **DO NOT**:
- Commit private keys to version control
- Use same key for multiple networks
- Share keys via unencrypted channels
- Store keys in plaintext files

✅ **DO**:
- Use environment variables or secrets vault
- Rotate keys regularly
- Use hardware wallets for production
- Implement key encryption at rest
- Use separate accounts per environment

### Contract Deployment Security

1. **Code Audit**: Get professional security audit before mainnet
2. **Testnet Validation**: Deploy to testnet first, test thoroughly
3. **Gradual Rollout**: Start with low transaction volume
4. **Monitoring**: Watch contract for unusual activity
5. **Upgrade Path**: Design for contract upgrades (proxy pattern)

### Event Logging Security

1. **Data Privacy**: Hash sensitive data before on-chain logging
2. **Access Control**: Implement proper authorization checks
3. **Rate Limiting**: Prevent spam/DOS through transaction limits
4. **Event Archival**: Archive old events off-chain while keeping proof on-chain

## Troubleshooting

### "Failed to connect to blockchain"
- Check BLOCKCHAIN_PROVIDER_URL is correct
- Verify network connectivity to provider
- Check API key/quota limits (Infura, Alchemy, etc.)

### "Insufficient gas"
- Increase GAS_PRICE in environment
- Use efficient contract operations
- Consider batch operations for multiple events

### "Contract not found at address"
- Verify CONTRACT_ADDRESS is correct
- Check contract is deployed on correct network
- Ensure ABI matches contract version

### "Transaction reverted"
- Check account has sufficient ETH for gas
- Verify function parameters are valid
- Check contract state and authorization

## Resources

- **Solidity**: https://docs.soliditylang.org/
- **Web3.py**: https://web3py.readthedocs.io/
- **Hardhat**: https://hardhat.org/docs
- **Infura**: https://infura.io/
- **OpenZeppelin**: https://docs.openzeppelin.com/

## Support

For blockchain integration issues:
1. Check blockchain service logs: `logs/blockchain_fallback/`
2. Test connection: `POST /api/blockchain/test-connection`
3. Check health: `GET /api/blockchain/health`
4. Review contract events on Etherscan (if using public network)
