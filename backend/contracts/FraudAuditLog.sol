// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title FraudAuditLog
 * @dev Smart contract for immutable fraud detection audit trail
 * Real-world blockchain solution for cybersecurity event logging
 */
contract FraudAuditLog {
    
    struct SecurityEvent {
        uint256 timestamp;
        string eventType;
        string severity;
        bytes32 dataHash;
        uint256 riskScore;
        address reporter;
        bool verified;
    }
    
    // Event counter
    uint256 public eventCount = 0;
    
    // Mapping of event ID to SecurityEvent
    mapping(uint256 => SecurityEvent) public securityEvents;
    
    // Mapping of repository to event IDs
    mapping(string => uint256[]) public repositoryEvents;
    
    // Owner address (fraud detection system)
    address public owner;
    
    // Events
    event SecurityEventLogged(
        uint256 indexed eventId,
        string eventType,
        string severity,
        bytes32 dataHash,
        uint256 riskScore,
        uint256 timestamp
    );
    
    event EventVerified(uint256 indexed eventId, address verifier);
    
    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this function");
        _;
    }
    
    constructor() {
        owner = msg.sender;
    }
    
    /**
     * @dev Log a security event to the blockchain
     * @param eventType Type of security event (e.g., "fraud_detection", "suspicious_commit")
     * @param severity Severity level (low, medium, high, critical)
     * @param dataHash SHA256 hash of the event data
     * @param riskScore Risk score (0-100)
     * @return eventId ID of the logged event
     */
    function logSecurityEvent(
        string memory eventType,
        string memory severity,
        bytes32 dataHash,
        uint256 riskScore
    ) public returns (uint256) {
        require(riskScore <= 100, "Risk score must be between 0 and 100");
        
        eventCount++;
        
        securityEvents[eventCount] = SecurityEvent({
            timestamp: block.timestamp,
            eventType: eventType,
            severity: severity,
            dataHash: dataHash,
            riskScore: riskScore,
            reporter: msg.sender,
            verified: false
        });
        
        emit SecurityEventLogged(
            eventCount,
            eventType,
            severity,
            dataHash,
            riskScore,
            block.timestamp
        );
        
        return eventCount;
    }
    
    /**
     * @dev Get security event details
     * @param eventId ID of the event
     * @return timestamp Event timestamp
     * @return eventType Type of event
     * @return severity Severity level
     * @return dataHash Data hash
     * @return riskScore Risk score
     * @return verified Verification status
     */
    function getSecurityEvent(uint256 eventId) 
        public 
        view 
        returns (
            uint256 timestamp,
            string memory eventType,
            string memory severity,
            bytes32 dataHash,
            uint256 riskScore,
            bool verified
        ) 
    {
        require(eventId > 0 && eventId <= eventCount, "Invalid event ID");
        
        SecurityEvent memory evt = securityEvents[eventId];
        
        return (
            evt.timestamp,
            evt.eventType,
            evt.severity,
            evt.dataHash,
            evt.riskScore,
            evt.verified
        );
    }
    
    /**
     * @dev Verify a security event (can only be done once)
     * @param eventId ID of the event to verify
     */
    function verifyEvent(uint256 eventId) public onlyOwner {
        require(eventId > 0 && eventId <= eventCount, "Invalid event ID");
        require(!securityEvents[eventId].verified, "Event already verified");
        
        securityEvents[eventId].verified = true;
        
        emit EventVerified(eventId, msg.sender);
    }
    
    /**
     * @dev Get total count of security events
     * @return count Total number of events
     */
    function getEventCount() public view returns (uint256) {
        return eventCount;
    }
    
    /**
     * @dev Get events by severity
     * @param severity Severity level to filter
     * @return eventIds Array of event IDs matching severity
     */
    function getEventsBySeverity(string memory severity) 
        public 
        view 
        returns (uint256[] memory) 
    {
        uint256[] memory tempEvents = new uint256[](eventCount);
        uint256 count = 0;
        
        for (uint256 i = 1; i <= eventCount; i++) {
            if (keccak256(bytes(securityEvents[i].severity)) == keccak256(bytes(severity))) {
                tempEvents[count] = i;
                count++;
            }
        }
        
        // Create properly sized array
        uint256[] memory result = new uint256[](count);
        for (uint256 i = 0; i < count; i++) {
            result[i] = tempEvents[i];
        }
        
        return result;
    }
    
    /**
     * @dev Get high-risk events (risk score >= 70)
     * @return eventIds Array of high-risk event IDs
     */
    function getHighRiskEvents() public view returns (uint256[] memory) {
        uint256[] memory tempEvents = new uint256[](eventCount);
        uint256 count = 0;
        
        for (uint256 i = 1; i <= eventCount; i++) {
            if (securityEvents[i].riskScore >= 70) {
                tempEvents[count] = i;
                count++;
            }
        }
        
        uint256[] memory result = new uint256[](count);
        for (uint256 i = 0; i < count; i++) {
            result[i] = tempEvents[i];
        }
        
        return result;
    }
}
