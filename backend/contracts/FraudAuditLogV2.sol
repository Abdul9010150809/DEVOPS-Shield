// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title FraudAuditLogV2
 * @dev Enterprise-grade immutable audit trail for cybersecurity fraud detection
 * Enhanced features: event chaining, multi-signature verification, audit reports, escalation tracking
 * Stores security events on blockchain for tamper-proof logging with cryptographic verification
 */
contract FraudAuditLogV2 {
    
    // Severity levels
    enum SeverityLevel { LOW, MEDIUM, HIGH, CRITICAL }
    
    // Event status
    enum EventStatus { PENDING, VERIFIED, ESCALATED, RESOLVED }
    
    // Enhanced security event struct with chaining and verification
    struct SecurityEvent {
        uint256 eventId;
        uint256 timestamp;
        string eventType;
        string severity;
        bytes32 dataHash;
        uint256 riskScore;
        address reporter;
        bool verified;
        bytes32 previousEventHash;        // Event chaining for immutable audit trail
        uint256 signatureCount;           // Multi-signature verification count
        bytes32 reportHash;               // Audit report hash
        EventStatus status;               // Current event status
        string repository;                // Repository identifier
        uint256 mitigationTime;           // Time to mitigation (0 if unresolved)
    }
    
    // Multi-signature verification record
    struct SignatureVerification {
        address signer;
        uint256 timestamp;
        bool verified;
        string signatureHash;
    }
    
    // Audit report struct
    struct AuditReport {
        uint256 reportId;
        uint256 timestamp;
        bytes32 reportHash;
        string reportType;
        uint256[] eventIds;
        uint256 totalRiskScore;
        address approver;
        bool approved;
        string summary;
    }
    
    // Event counter
    uint256 public eventCount = 0;
    uint256 public reportCount = 0;
    
    // Mapping of event ID to SecurityEvent
    mapping(uint256 => SecurityEvent) public securityEvents;
    mapping(bytes32 => SecurityEvent) public eventsByHash;
    
    // Mapping of repository to event IDs
    mapping(string => uint256[]) public repositoryEvents;
    
    // Signature verifications for each event
    mapping(uint256 => SignatureVerification[]) public eventSignatures;
    
    // Audit reports
    mapping(uint256 => AuditReport) public auditReports;
    mapping(string => uint256[]) public reportsByRepository;
    
    // Authorized signers for multi-signature verification
    mapping(address => bool) public authorizedSigners;
    
    // Owner address (fraud detection system)
    address public owner;
    
    // Blockchain configuration
    uint256 public minimumSignaturesRequired = 2;
    
    // Events
    event SecurityEventLogged(
        uint256 indexed eventId,
        string eventType,
        string severity,
        bytes32 dataHash,
        uint256 riskScore,
        address reporter,
        uint256 timestamp,
        bytes32 indexed previousEventHash
    );
    
    event EventVerified(
        uint256 indexed eventId,
        address indexed verifier,
        uint256 signatureCount,
        uint256 timestamp
    );
    
    event EventEscalated(
        uint256 indexed eventId,
        string reason,
        uint256 timestamp
    );
    
    event EventResolved(
        uint256 indexed eventId,
        uint256 mitigationTime,
        uint256 timestamp
    );
    
    event AuditReportGenerated(
        uint256 indexed reportId,
        string reportType,
        bytes32 reportHash,
        uint256 timestamp
    );
    
    event SignerAuthorized(address indexed signer, uint256 timestamp);
    
    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this function");
        _;
    }
    
    modifier onlyAuthorized() {
        require(msg.sender == owner || authorizedSigners[msg.sender], "Only authorized signers");
        _;
    }
    
    constructor() {
        owner = msg.sender;
        authorizedSigners[msg.sender] = true;
    }
    
    /**
     * @dev Log a security event with event chaining
     * @param eventType Type of security event
     * @param severity Severity level as string (low, medium, high, critical)
     * @param dataHash Hash of event data for immutability
     * @param riskScore Risk score (0-100)
     * @param repository Repository identifier
     * @return eventId New event ID
     */
    function logSecurityEvent(
        string memory eventType,
        string memory severity,
        bytes32 dataHash,
        uint256 riskScore,
        string memory repository
    ) external onlyAuthorized returns (uint256) {
        require(riskScore <= 100, "Risk score must be 0-100");
        require(bytes(eventType).length > 0, "Event type required");
        
        uint256 newEventId = eventCount++;
        
        // Calculate chained hash from previous event
        bytes32 previousEventHash = bytes32(0);
        if (newEventId > 0) {
            SecurityEvent storage prevEvent = securityEvents[newEventId - 1];
            previousEventHash = keccak256(
                abi.encodePacked(
                    prevEvent.eventId,
                    prevEvent.timestamp,
                    prevEvent.dataHash
                )
            );
        }
        
        // Create new event with chaining
        SecurityEvent storage newEvent = securityEvents[newEventId];
        newEvent.eventId = newEventId;
        newEvent.timestamp = block.timestamp;
        newEvent.eventType = eventType;
        newEvent.severity = severity;
        newEvent.dataHash = dataHash;
        newEvent.riskScore = riskScore;
        newEvent.reporter = msg.sender;
        newEvent.verified = false;
        newEvent.previousEventHash = previousEventHash;
        newEvent.signatureCount = 0;
        newEvent.status = EventStatus.PENDING;
        newEvent.repository = repository;
        newEvent.mitigationTime = 0;
        
        // Store by hash for quick lookup
        bytes32 eventHash = keccak256(abi.encodePacked(newEventId, block.timestamp, dataHash));
        eventsByHash[eventHash] = newEvent;
        
        // Add to repository event list
        repositoryEvents[repository].push(newEventId);
        
        emit SecurityEventLogged(
            newEventId,
            eventType,
            severity,
            dataHash,
            riskScore,
            msg.sender,
            block.timestamp,
            previousEventHash
        );
        
        return newEventId;
    }
    
    /**
     * @dev Verify an event with multi-signature support
     * @param eventId Event to verify
     * @param signatureHash Hash of verification signature
     */
    function verifyEvent(
        uint256 eventId,
        string memory signatureHash
    ) external onlyAuthorized {
        require(eventId < eventCount, "Invalid event ID");
        
        SecurityEvent storage securityEvent = securityEvents[eventId];
        
        // Record signature verification
        SignatureVerification memory sig = SignatureVerification({
            signer: msg.sender,
            timestamp: block.timestamp,
            verified: true,
            signatureHash: signatureHash
        });
        
        eventSignatures[eventId].push(sig);
        securityEvent.signatureCount++;
        
        // Mark as verified if minimum signatures reached
        if (securityEvent.signatureCount >= minimumSignaturesRequired) {
            securityEvent.verified = true;
            securityEvent.status = EventStatus.VERIFIED;
        }
        
        emit EventVerified(eventId, msg.sender, securityEvent.signatureCount, block.timestamp);
    }
    
    /**
     * @dev Escalate a security event
     * @param eventId Event to escalate
     * @param reason Escalation reason
     */
    function escalateEvent(uint256 eventId, string memory reason) external onlyAuthorized {
        require(eventId < eventCount, "Invalid event ID");
        
        SecurityEvent storage securityEvent = securityEvents[eventId];
        securityEvent.status = EventStatus.ESCALATED;
        
        emit EventEscalated(eventId, reason, block.timestamp);
    }
    
    /**
     * @dev Mark event as resolved
     * @param eventId Event to resolve
     * @param mitigationTime Time taken to mitigate (seconds)
     */
    function resolveEvent(uint256 eventId, uint256 mitigationTime) external onlyOwner {
        require(eventId < eventCount, "Invalid event ID");
        
        SecurityEvent storage securityEvent = securityEvents[eventId];
        securityEvent.status = EventStatus.RESOLVED;
        securityEvent.mitigationTime = mitigationTime;
        
        emit EventResolved(eventId, mitigationTime, block.timestamp);
    }
    
    /**
     * @dev Generate audit report from multiple events
     * @param reportType Type of report (daily, weekly, incident)
     * @param eventIds Array of event IDs to include
     * @param summary Report summary
     * @return reportId New report ID
     */
    function generateAuditReport(
        string memory reportType,
        uint256[] memory eventIds,
        string memory summary
    ) external onlyOwner returns (uint256) {
        require(eventIds.length > 0, "At least one event required");
        
        uint256 newReportId = reportCount++;
        uint256 totalRiskScore = 0;
        
        // Aggregate risk scores from events
        for (uint256 i = 0; i < eventIds.length; i++) {
            require(eventIds[i] < eventCount, "Invalid event ID");
            totalRiskScore += securityEvents[eventIds[i]].riskScore;
        }
        
        // Create report
        bytes32 reportHash = keccak256(
            abi.encodePacked(block.timestamp, reportType, eventIds, totalRiskScore)
        );
        
        AuditReport storage report = auditReports[newReportId];
        report.reportId = newReportId;
        report.timestamp = block.timestamp;
        report.reportHash = reportHash;
        report.reportType = reportType;
        report.eventIds = eventIds;
        report.totalRiskScore = totalRiskScore;
        report.approver = msg.sender;
        report.approved = true;
        report.summary = summary;
        
        // Store in repository reports (use first event's repository)
        if (eventIds.length > 0) {
            string memory repo = securityEvents[eventIds[0]].repository;
            reportsByRepository[repo].push(newReportId);
        }
        
        emit AuditReportGenerated(newReportId, reportType, reportHash, block.timestamp);
        
        return newReportId;
    }
    
    /**
     * @dev Get security event details
     * @param eventId Event ID to retrieve
     * @return event SecurityEvent struct
     */
    function getSecurityEvent(uint256 eventId) 
        external 
        view 
        returns (SecurityEvent memory) 
    {
        require(eventId < eventCount, "Invalid event ID");
        return securityEvents[eventId];
    }
    
    /**
     * @dev Get events by repository
     * @param repository Repository name
     * @return eventIds Array of event IDs for repository
     */
    function getRepositoryEvents(string memory repository) 
        external 
        view 
        returns (uint256[] memory) 
    {
        return repositoryEvents[repository];
    }
    
    /**
     * @dev Get high-risk events (risk score >= threshold)
     * @param threshold Risk score threshold (0-100)
     * @return highRiskEvents Array of high-risk event IDs
     */
    function getHighRiskEvents(uint256 threshold) 
        external 
        view 
        returns (uint256[] memory) 
    {
        require(threshold <= 100, "Threshold must be 0-100");
        
        uint256[] memory result = new uint256[](eventCount);
        uint256 count = 0;
        
        for (uint256 i = 0; i < eventCount; i++) {
            if (securityEvents[i].riskScore >= threshold) {
                result[count] = i;
                count++;
            }
        }
        
        // Resize array to actual count
        uint256[] memory trimmed = new uint256[](count);
        for (uint256 i = 0; i < count; i++) {
            trimmed[i] = result[i];
        }
        
        return trimmed;
    }
    
    /**
     * @dev Get events by severity level
     * @param severity Severity as string (low, medium, high, critical)
     * @return events Array of event IDs with matching severity
     */
    function getEventsBySeverity(string memory severity) 
        external 
        view 
        returns (uint256[] memory) 
    {
        uint256[] memory result = new uint256[](eventCount);
        uint256 count = 0;
        
        for (uint256 i = 0; i < eventCount; i++) {
            if (keccak256(bytes(securityEvents[i].severity)) == keccak256(bytes(severity))) {
                result[count] = i;
                count++;
            }
        }
        
        // Resize array
        uint256[] memory trimmed = new uint256[](count);
        for (uint256 i = 0; i < count; i++) {
            trimmed[i] = result[i];
        }
        
        return trimmed;
    }
    
    /**
     * @dev Get unresolved events
     * @return unresolvedEventIds Array of unresolved event IDs
     */
    function getUnresolvedEvents() 
        external 
        view 
        returns (uint256[] memory) 
    {
        uint256[] memory result = new uint256[](eventCount);
        uint256 count = 0;
        
        for (uint256 i = 0; i < eventCount; i++) {
            if (securityEvents[i].status != EventStatus.RESOLVED) {
                result[count] = i;
                count++;
            }
        }
        
        // Resize array
        uint256[] memory trimmed = new uint256[](count);
        for (uint256 i = 0; i < count; i++) {
            trimmed[i] = result[i];
        }
        
        return trimmed;
    }
    
    /**
     * @dev Get audit report
     * @param reportId Report ID
     * @return report AuditReport struct
     */
    function getAuditReport(uint256 reportId) 
        external 
        view 
        returns (AuditReport memory) 
    {
        require(reportId < reportCount, "Invalid report ID");
        return auditReports[reportId];
    }
    
    /**
     * @dev Get signature verifications for event
     * @param eventId Event ID
     * @return signatures Array of SignatureVerification structs
     */
    function getEventSignatures(uint256 eventId) 
        external 
        view 
        returns (SignatureVerification[] memory) 
    {
        require(eventId < eventCount, "Invalid event ID");
        return eventSignatures[eventId];
    }
    
    /**
     * @dev Authorize a signer for multi-signature verification
     * @param signer Address to authorize
     */
    function authorizeSigner(address signer) external onlyOwner {
        require(signer != address(0), "Invalid signer address");
        authorizedSigners[signer] = true;
        emit SignerAuthorized(signer, block.timestamp);
    }
    
    /**
     * @dev Revoke signer authorization
     * @param signer Address to revoke
     */
    function revokeSigner(address signer) external onlyOwner {
        authorizedSigners[signer] = false;
    }
    
    /**
     * @dev Set minimum signatures required for verification
     * @param minimumSignatures New minimum signature count
     */
    function setMinimumSignatures(uint256 minimumSignatures) external onlyOwner {
        require(minimumSignatures > 0, "Minimum must be at least 1");
        minimumSignaturesRequired = minimumSignatures;
    }
    
    /**
     * @dev Get blockchain statistics
     * @return stats Array with [eventCount, reportCount, blockNumber]
     */
    function getBlockchainStats() 
        external 
        view 
        returns (uint256[] memory stats) 
    {
        stats = new uint256[](3);
        stats[0] = eventCount;
        stats[1] = reportCount;
        stats[2] = block.number;
        return stats;
    }
}
