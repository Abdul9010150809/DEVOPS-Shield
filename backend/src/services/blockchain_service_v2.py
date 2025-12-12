"""
Enhanced Blockchain Service for Immutable Audit Trail
Integrates Web3, smart contract interaction, event chaining, and multi-signature verification
"""
import hashlib
import json
import time
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List, Tuple
from enum import Enum

try:
    from web3 import Web3  # type: ignore
    from eth_account import Account  # type: ignore
    HAS_WEB3 = True
except ImportError:
    Web3 = None  # type: ignore
    Account = None  # type: ignore
    HAS_WEB3 = False

from ..utils.logger import get_logger
import os

logger = get_logger(__name__)


class EventStatus(str, Enum):
    """Event lifecycle status"""
    PENDING = "pending"
    VERIFIED = "verified"
    ESCALATED = "escalated"
    RESOLVED = "resolved"


class SeverityLevel(str, Enum):
    """Severity levels for security events"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class BlockchainAuditService:
    """
    Enterprise-grade blockchain integration for cybersecurity audit trails.
    Features:
    - Event logging with immutable chaining
    - Multi-signature verification
    - Audit report generation
    - Event filtering and retrieval
    - Fallback local storage for offline operation
    """
    
    def __init__(
        self,
        provider_url: str = None,
        contract_address: str = None,
        contract_abi: List[Dict] = None
    ):
        """
        Initialize blockchain service
        
        Args:
            provider_url: Web3 provider URL (Infura, Alchemy, Ganache, etc.)
            contract_address: Deployed smart contract address
            contract_abi: Contract ABI (uses default if not provided)
        """
        self.provider_url = provider_url or os.getenv(
            "BLOCKCHAIN_PROVIDER_URL", "http://localhost:8545"
        )
        self.contract_address = contract_address or os.getenv(
            "BLOCKCHAIN_CONTRACT_ADDRESS"
        )
        self.private_key = os.getenv("BLOCKCHAIN_PRIVATE_KEY")
        self.network_name = os.getenv("BLOCKCHAIN_NETWORK", "local")
        
        # Initialize Web3
        if not HAS_WEB3:
            logger.warning(
                "Web3 dependencies not installed; blockchain operations will use local fallback"
            )
            self.connected = False
            self.w3 = None
        else:
            try:
                self.w3 = Web3(Web3.HTTPProvider(self.provider_url))
                self.connected = self.w3.is_connected()
                
                if self.connected:
                    logger.info(f"✅ Connected to blockchain at {self.provider_url}")
                    logger.info(f"Chain ID: {self.w3.eth.chain_id}, Block: {self.w3.eth.block_number}")
                else:
                    logger.warning(
                        f"❌ Failed to connect to blockchain at {self.provider_url}"
                    )
                    
            except Exception as e:
                logger.error(f"Blockchain initialization error: {e}")
                self.connected = False
                self.w3 = None
        
        # Contract ABI for FraudAuditLogV2 smart contract
        self.contract_abi = contract_abi or self._get_default_abi()
        
        # Initialize contract if address provided
        self.contract = None
        if self.connected and self.contract_address and self.w3:
            try:
                self.contract = self.w3.eth.contract(
                    address=Web3.to_checksum_address(self.contract_address),
                    abi=self.contract_abi
                )
                logger.info(f"✅ Smart contract loaded at {self.contract_address}")
            except Exception as e:
                logger.error(f"Failed to load smart contract: {e}")
                self.contract = None
    
    @staticmethod
    def _get_default_abi() -> List[Dict]:
        """Get default FraudAuditLogV2 contract ABI"""
        return [
            {
                "inputs": [
                    {"name": "eventType", "type": "string"},
                    {"name": "severity", "type": "string"},
                    {"name": "dataHash", "type": "bytes32"},
                    {"name": "riskScore", "type": "uint256"},
                    {"name": "repository", "type": "string"}
                ],
                "name": "logSecurityEvent",
                "outputs": [{"name": "", "type": "uint256"}],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [{"name": "eventId", "type": "uint256"}],
                "name": "getSecurityEvent",
                "outputs": [
                    {"name": "eventId", "type": "uint256"},
                    {"name": "timestamp", "type": "uint256"},
                    {"name": "eventType", "type": "string"},
                    {"name": "severity", "type": "string"},
                    {"name": "dataHash", "type": "bytes32"},
                    {"name": "riskScore", "type": "uint256"},
                    {"name": "reporter", "type": "address"},
                    {"name": "verified", "type": "bool"},
                    {"name": "previousEventHash", "type": "bytes32"},
                    {"name": "signatureCount", "type": "uint256"},
                    {"name": "reportHash", "type": "bytes32"},
                    {"name": "status", "type": "uint8"},
                    {"name": "repository", "type": "string"},
                    {"name": "mitigationTime", "type": "uint256"}
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [
                    {"name": "eventId", "type": "uint256"},
                    {"name": "signatureHash", "type": "string"}
                ],
                "name": "verifyEvent",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [
                    {"name": "eventId", "type": "uint256"},
                    {"name": "reason", "type": "string"}
                ],
                "name": "escalateEvent",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [
                    {"name": "eventId", "type": "uint256"},
                    {"name": "mitigationTime", "type": "uint256"}
                ],
                "name": "resolveEvent",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [
                    {"name": "reportType", "type": "string"},
                    {"name": "eventIds", "type": "uint256[]"},
                    {"name": "summary", "type": "string"}
                ],
                "name": "generateAuditReport",
                "outputs": [{"name": "", "type": "uint256"}],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [{"name": "severity", "type": "string"}],
                "name": "getEventsBySeverity",
                "outputs": [{"name": "", "type": "uint256[]"}],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [{"name": "threshold", "type": "uint256"}],
                "name": "getHighRiskEvents",
                "outputs": [{"name": "", "type": "uint256[]"}],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "getUnresolvedEvents",
                "outputs": [{"name": "", "type": "uint256[]"}],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "getBlockchainStats",
                "outputs": [{"name": "stats", "type": "uint256[]"}],
                "stateMutability": "view",
                "type": "function"
            }
        ]
    
    def calculate_data_hash(self, data: Dict[str, Any]) -> str:
        """
        Calculate cryptographic hash of fraud detection data
        
        Args:
            data: Fraud analysis data
            
        Returns:
            SHA256 hash as hex string
        """
        try:
            # Normalize data for consistent hashing
            normalized = {
                'repository': data.get('repository', ''),
                'timestamp': data.get('timestamp', time.time()),
                'risk_score': round(data.get('risk_score', 0.0), 3),
                'violations': sorted(data.get('rule_violations', [])),
                'event_type': data.get('event_type', 'fraud_detection'),
            }
            
            data_string = json.dumps(normalized, sort_keys=True)
            hash_object = hashlib.sha256(data_string.encode())
            return hash_object.hexdigest()
            
        except Exception as e:
            logger.error(f"Error calculating data hash: {e}")
            return hashlib.sha256(str(data).encode()).hexdigest()
    
    def log_fraud_event(
        self,
        event_data: Dict[str, Any],
        repository: str = "default"
    ) -> Optional[Dict[str, Any]]:
        """
        Log fraud detection event on blockchain
        
        Args:
            event_data: Fraud analysis result
            repository: Repository identifier
            
        Returns:
            Transaction receipt or None
        """
        if not self.connected or not self.contract or not self.private_key:
            logger.warning("Blockchain not available, storing event locally")
            return self._store_locally(event_data, "fraud_log")
        
        try:
            # Extract event details
            event_type = event_data.get('event_type', 'fraud_detection')
            risk_score = float(event_data.get('risk_score', 0.0))
            severity = self._map_risk_to_severity(risk_score)
            risk_score_int = int(risk_score * 100)  # Convert to integer percentage
            
            # Calculate data hash
            data_hash = self.calculate_data_hash(event_data)
            data_hash_bytes = bytes.fromhex(data_hash)
            
            # Get account from private key
            account = Account.from_key(self.private_key)
            
            # Build and send transaction
            nonce = self.w3.eth.get_transaction_count(account.address)
            
            transaction = self.contract.functions.logSecurityEvent(
                event_type,
                severity,
                data_hash_bytes,
                risk_score_int,
                repository
            ).build_transaction({
                'from': account.address,
                'nonce': nonce,
                'gas': 300000,
                'gasPrice': self.w3.eth.gas_price,
            })
            
            # Sign and send
            signed_txn = self.w3.eth.account.sign_transaction(transaction, self.private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            # Wait for receipt
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
            
            logger.info(f"✅ Fraud event logged on blockchain: {tx_hash.hex()}")
            
            return {
                'transaction_hash': tx_hash.hex(),
                'block_number': tx_receipt['blockNumber'],
                'gas_used': tx_receipt['gasUsed'],
                'status': 'success' if tx_receipt['status'] == 1 else 'failed',
                'data_hash': data_hash,
                'timestamp': time.time(),
                'storage_method': 'blockchain'
            }
            
        except Exception as e:
            logger.error(f"Error logging event on blockchain: {e}", exc_info=True)
            return self._store_locally(event_data, "fraud_log")
    
    def verify_event_on_chain(
        self,
        event_id: int,
        signature_hash: str
    ) -> Optional[Dict[str, Any]]:
        """
        Verify event with multi-signature on blockchain
        
        Args:
            event_id: Event ID on blockchain
            signature_hash: Verification signature hash
            
        Returns:
            Verification result
        """
        if not self.connected or not self.contract or not self.private_key:
            logger.warning("Blockchain not available")
            return None
        
        try:
            account = Account.from_key(self.private_key)
            nonce = self.w3.eth.get_transaction_count(account.address)
            
            transaction = self.contract.functions.verifyEvent(
                event_id,
                signature_hash
            ).build_transaction({
                'from': account.address,
                'nonce': nonce,
                'gas': 200000,
                'gasPrice': self.w3.eth.gas_price,
            })
            
            signed_txn = self.w3.eth.account.sign_transaction(transaction, self.private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
            
            logger.info(f"✅ Event verified on blockchain: {tx_hash.hex()}")
            
            return {
                'transaction_hash': tx_hash.hex(),
                'block_number': tx_receipt['blockNumber'],
                'status': 'verified',
                'timestamp': time.time()
            }
            
        except Exception as e:
            logger.error(f"Error verifying event: {e}", exc_info=True)
            return None
    
    def get_audit_trail(
        self,
        repository: str = None,
        severity: str = None,
        risk_threshold: int = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve audit trail from blockchain with optional filtering
        
        Args:
            repository: Filter by repository name
            severity: Filter by severity level
            risk_threshold: Filter by minimum risk score
            
        Returns:
            List of audit events
        """
        if not self.connected or not self.contract:
            logger.warning("Blockchain not available, returning local fallback")
            return self._load_local_audit_trail(repository)
        
        try:
            events = []
            
            # Get events by severity if specified
            if severity:
                event_ids = self.contract.functions.getEventsBySeverity(severity).call()
                for event_id in event_ids:
                    event = self._fetch_event(event_id)
                    if event and (not repository or event.get('repository') == repository):
                        events.append(event)
            
            # Get high-risk events if threshold specified
            if risk_threshold is not None:
                event_ids = self.contract.functions.getHighRiskEvents(risk_threshold).call()
                for event_id in event_ids:
                    event = self._fetch_event(event_id)
                    if event and (not repository or event.get('repository') == repository):
                        if event not in events:  # Avoid duplicates
                            events.append(event)
            
            # Get unresolved events
            if not severity and risk_threshold is None:
                event_ids = self.contract.functions.getUnresolvedEvents().call()
                for event_id in event_ids:
                    event = self._fetch_event(event_id)
                    if event and (not repository or event.get('repository') == repository):
                        events.append(event)
            
            # Sort by timestamp descending
            events.sort(key=lambda x: x.get('timestamp', 0), reverse=True)
            
            logger.info(f"Retrieved {len(events)} audit trail events")
            return events
            
        except Exception as e:
            logger.error(f"Error retrieving audit trail: {e}", exc_info=True)
            return self._load_local_audit_trail(repository)
    
    def _fetch_event(self, event_id: int) -> Optional[Dict[str, Any]]:
        """Fetch single event from blockchain"""
        try:
            event_data = self.contract.functions.getSecurityEvent(event_id).call()
            return {
                'event_id': event_data[0],
                'timestamp': event_data[1],
                'event_type': event_data[2],
                'severity': event_data[3],
                'data_hash': event_data[4].hex() if event_data[4] else None,
                'risk_score': event_data[5],
                'reporter': event_data[6],
                'verified': event_data[7],
                'previous_event_hash': event_data[8].hex() if event_data[8] else None,
                'signature_count': event_data[9],
                'report_hash': event_data[10].hex() if event_data[10] else None,
                'status': self._status_to_string(event_data[11]),
                'repository': event_data[12],
                'mitigation_time': event_data[13]
            }
        except Exception as e:
            logger.error(f"Error fetching event {event_id}: {e}")
            return None
    
    def get_blockchain_stats(self) -> Dict[str, Any]:
        """Get blockchain connection and contract statistics"""
        if not self.connected or not self.w3:
            return {
                'connected': False,
                'provider': self.provider_url,
                'network': self.network_name,
                'status': 'disconnected'
            }
        
        try:
            stats = {}
            
            # Connection stats
            stats['connected'] = True
            stats['provider'] = self.provider_url
            stats['network'] = self.network_name
            stats['chain_id'] = self.w3.eth.chain_id
            stats['block_number'] = self.w3.eth.block_number
            stats['gas_price'] = str(self.w3.eth.gas_price)
            stats['status'] = 'connected'
            
            # Contract stats
            if self.contract:
                try:
                    blockchain_stats = self.contract.functions.getBlockchainStats().call()
                    stats['event_count'] = blockchain_stats[0]
                    stats['report_count'] = blockchain_stats[1]
                    stats['contract_address'] = self.contract_address
                    stats['contract_status'] = 'deployed'
                except Exception as e:
                    logger.warning(f"Error getting contract stats: {e}")
                    stats['contract_status'] = 'error'
            else:
                stats['contract_status'] = 'not_loaded'
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting blockchain stats: {e}")
            return {
                'connected': False,
                'error': str(e),
                'network': self.network_name
            }
    
    @staticmethod
    def _map_risk_to_severity(risk_score: float) -> str:
        """Map risk score (0-1) to severity level"""
        if risk_score >= 0.9:
            return "critical"
        elif risk_score >= 0.7:
            return "high"
        elif risk_score >= 0.5:
            return "medium"
        else:
            return "low"
    
    @staticmethod
    def _status_to_string(status_code: int) -> str:
        """Convert event status code to string"""
        status_map = {
            0: "pending",
            1: "verified",
            2: "escalated",
            3: "resolved"
        }
        return status_map.get(status_code, "unknown")
    
    def _store_locally(self, event_data: Dict[str, Any], event_type: str) -> Dict[str, Any]:
        """
        Fallback local storage when blockchain is unavailable
        
        Args:
            event_data: Event data to store
            event_type: Type of event for file organization
            
        Returns:
            Local storage receipt
        """
        try:
            data_hash = self.calculate_data_hash(event_data)
            
            # Create audit log file
            log_dir = "logs/blockchain_fallback"
            os.makedirs(log_dir, exist_ok=True)
            
            audit_file = os.path.join(log_dir, f"{event_type}_{datetime.now().date()}.jsonl")
            
            record = {
                'timestamp': time.time(),
                'data_hash': data_hash,
                'event_type': event_type,
                'event_data': event_data,
                'storage_method': 'local_fallback'
            }
            
            # Append to file
            with open(audit_file, 'a') as f:
                f.write(json.dumps(record) + '\n')
            
            logger.info(f"✅ Event stored locally (blockchain unavailable)")
            
            return {
                'storage_method': 'local',
                'data_hash': data_hash,
                'timestamp': time.time(),
                'status': 'pending_sync'
            }
            
        except Exception as e:
            logger.error(f"Error in local storage fallback: {e}")
            return {'storage_method': 'memory', 'status': 'error'}
    
    def _load_local_audit_trail(self, repository: str = None) -> List[Dict[str, Any]]:
        """Load audit trail from local fallback files"""
        try:
            events = []
            log_dir = "logs/blockchain_fallback"
            
            if not os.path.exists(log_dir):
                return []
            
            # Load all fallback files
            for filename in os.listdir(log_dir):
                if filename.startswith('fraud_log_'):
                    with open(os.path.join(log_dir, filename), 'r') as f:
                        for line in f:
                            try:
                                record = json.loads(line)
                                event_data = record.get('event_data', {})
                                if not repository or event_data.get('repository') == repository:
                                    events.append({
                                        'timestamp': record['timestamp'],
                                        'data_hash': record['data_hash'],
                                        'event_data': event_data,
                                        'source': 'local_fallback'
                                    })
                            except json.JSONDecodeError:
                                continue
            
            # Sort by timestamp descending
            events.sort(key=lambda x: x['timestamp'], reverse=True)
            return events
            
        except Exception as e:
            logger.error(f"Error loading local audit trail: {e}")
            return []
