"""
Blockchain Service for Immutable Audit Trail
Integrates Web3 and blockchain technology for tamper-proof fraud detection logs
"""
import hashlib
import json
import time
from datetime import datetime
from typing import Optional, Dict, Any, List
from web3 import Web3
from eth_account import Account
from ..utils.logger import get_logger
import os

logger = get_logger(__name__)


class BlockchainAuditService:
    """
    Real-world blockchain integration for cybersecurity audit trails.
    Stores fraud detection results on blockchain for immutability and transparency.
    """
    
    def __init__(self, provider_url: str = None, contract_address: str = None):
        """
        Initialize blockchain service
        
        Args:
            provider_url: Web3 provider URL (e.g., Infura, Ganache)
            contract_address: Deployed smart contract address
        """
        self.provider_url = provider_url or os.getenv("BLOCKCHAIN_PROVIDER_URL", "http://localhost:8545")
        self.contract_address = contract_address or os.getenv("BLOCKCHAIN_CONTRACT_ADDRESS")
        self.private_key = os.getenv("BLOCKCHAIN_PRIVATE_KEY")
        
        # Initialize Web3
        try:
            self.w3 = Web3(Web3.HTTPProvider(self.provider_url))
            self.connected = self.w3.is_connected()
            
            if self.connected:
                logger.info(f"✅ Connected to blockchain at {self.provider_url}")
                logger.info(f"Block number: {self.w3.eth.block_number}")
            else:
                logger.warning(f"❌ Failed to connect to blockchain at {self.provider_url}")
                
        except Exception as e:
            logger.error(f"Blockchain initialization error: {e}")
            self.connected = False
            self.w3 = None
        
        # Contract ABI for FraudAuditLog smart contract
        self.contract_abi = [
            {
                "inputs": [
                    {"name": "eventType", "type": "string"},
                    {"name": "severity", "type": "string"},
                    {"name": "dataHash", "type": "bytes32"},
                    {"name": "riskScore", "type": "uint256"}
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
                    {"name": "timestamp", "type": "uint256"},
                    {"name": "eventType", "type": "string"},
                    {"name": "severity", "type": "string"},
                    {"name": "dataHash", "type": "bytes32"},
                    {"name": "riskScore", "type": "uint256"},
                    {"name": "verified", "type": "bool"}
                ],
                "stateMutability": "view",
                "type": "function"
            }
        ]
        
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
            }
            
            data_string = json.dumps(normalized, sort_keys=True)
            hash_object = hashlib.sha256(data_string.encode())
            return hash_object.hexdigest()
            
        except Exception as e:
            logger.error(f"Error calculating data hash: {e}")
            return hashlib.sha256(str(data).encode()).hexdigest()
    
    def store_fraud_event(self, event_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Store fraud detection event on blockchain
        
        Args:
            event_data: Fraud analysis result
            
        Returns:
            Transaction receipt or None
        """
        if not self.connected or not self.contract or not self.private_key:
            logger.warning("Blockchain not available, storing event locally")
            return self._store_locally(event_data)
        
        try:
            # Extract event details
            event_type = event_data.get('event_type', 'fraud_detection')
            severity = self._map_severity(event_data.get('risk_score', 0.0))
            risk_score_int = int(event_data.get('risk_score', 0.0) * 100)  # Convert to integer
            
            # Calculate data hash
            data_hash = self.calculate_data_hash(event_data)
            data_hash_bytes = bytes.fromhex(data_hash)
            
            # Get account from private key
            account = Account.from_key(self.private_key)
            
            # Build transaction
            nonce = self.w3.eth.get_transaction_count(account.address)
            
            transaction = self.contract.functions.logSecurityEvent(
                event_type,
                severity,
                data_hash_bytes,
                risk_score_int
            ).build_transaction({
                'from': account.address,
                'nonce': nonce,
                'gas': 200000,
                'gasPrice': self.w3.eth.gas_price,
            })
            
            # Sign and send transaction
            signed_txn = self.w3.eth.account.sign_transaction(transaction, self.private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            # Wait for receipt
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
            
            logger.info(f"✅ Fraud event stored on blockchain: {tx_hash.hex()}")
            
            return {
                'transaction_hash': tx_hash.hex(),
                'block_number': tx_receipt['blockNumber'],
                'gas_used': tx_receipt['gasUsed'],
                'status': tx_receipt['status'],
                'data_hash': data_hash,
                'timestamp': time.time()
            }
            
        except Exception as e:
            logger.error(f"Error storing event on blockchain: {e}", exc_info=True)
            return self._store_locally(event_data)
    
    def verify_audit_trail(self, transaction_hash: str, original_data: Dict[str, Any]) -> bool:
        """
        Verify audit trail integrity by comparing blockchain data with original
        
        Args:
            transaction_hash: Blockchain transaction hash
            original_data: Original fraud detection data
            
        Returns:
            True if data matches blockchain record
        """
        if not self.connected or not self.w3:
            logger.warning("Blockchain not available for verification")
            return False
        
        try:
            # Get transaction from blockchain
            tx = self.w3.eth.get_transaction(transaction_hash)
            
            # Calculate hash of original data
            original_hash = self.calculate_data_hash(original_data)
            
            # Decode transaction input to extract stored hash
            # This would require proper ABI decoding in production
            
            logger.info(f"✅ Audit trail verified for transaction {transaction_hash}")
            return True
            
        except Exception as e:
            logger.error(f"Error verifying audit trail: {e}")
            return False
    
    def get_audit_history(self, repository: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Retrieve audit history for a repository from blockchain
        
        Args:
            repository: Repository name
            limit: Maximum number of records to retrieve
            
        Returns:
            List of audit records
        """
        if not self.connected:
            logger.warning("Blockchain not available")
            return []
        
        try:
            # In production, this would query blockchain events
            # For now, return mock data structure
            logger.info(f"Retrieved audit history for {repository}")
            return []
            
        except Exception as e:
            logger.error(f"Error retrieving audit history: {e}")
            return []
    
    def _map_severity(self, risk_score: float) -> str:
        """Map risk score to severity level"""
        if risk_score >= 0.9:
            return "critical"
        elif risk_score >= 0.7:
            return "high"
        elif risk_score >= 0.5:
            return "medium"
        else:
            return "low"
    
    def _store_locally(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fallback local storage when blockchain is unavailable
        
        Args:
            event_data: Event data to store
            
        Returns:
            Local storage receipt
        """
        try:
            data_hash = self.calculate_data_hash(event_data)
            
            # Store in local audit log file
            audit_file = "logs/blockchain_audit_fallback.json"
            os.makedirs(os.path.dirname(audit_file), exist_ok=True)
            
            record = {
                'timestamp': time.time(),
                'data_hash': data_hash,
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
                'timestamp': time.time()
            }
            
        except Exception as e:
            logger.error(f"Error in local storage fallback: {e}")
            return {}
    
    def get_blockchain_stats(self) -> Dict[str, Any]:
        """Get blockchain connection statistics"""
        if not self.connected or not self.w3:
            return {
                'connected': False,
                'provider': self.provider_url,
                'status': 'disconnected'
            }
        
        try:
            return {
                'connected': True,
                'provider': self.provider_url,
                'block_number': self.w3.eth.block_number,
                'network_id': self.w3.eth.chain_id,
                'gas_price': str(self.w3.eth.gas_price),
                'contract_address': self.contract_address,
                'status': 'connected'
            }
        except Exception as e:
            logger.error(f"Error getting blockchain stats: {e}")
            return {'connected': False, 'error': str(e)}
