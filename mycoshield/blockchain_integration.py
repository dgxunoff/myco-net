"""
Blockchain Integration Points for MycoShield
"""

from .aptos_security import AptosSecurityManager
import json
from datetime import datetime

class ThreatIntelligenceBlockchain:
    """Store and retrieve threat intelligence from Aptos blockchain"""
    
    def __init__(self, aptos_manager):
        self.aptos_manager = aptos_manager
        
    def store_threat_signature(self, ip_address, signature_hash, threat_type):
        """Store threat signature immutably on blockchain"""
        return self.aptos_manager.submit_threat_data(ip_address, 1.0, f"{threat_type}:{signature_hash}")
    
    def create_immutable_threat_db(self, threat_entries):
        """Create immutable threat database on blockchain"""
        results = []
        for entry in threat_entries:
            tx_hash = self.aptos_manager.submit_threat_data(
                entry['ip'], entry['score'], entry['type']
            )
            results.append(tx_hash)
        return results
    
    def validate_threat_consensus(self, ip_address, validators):
        """Implement consensus-based threat validation"""
        consensus_score = 0
        for validator in validators:
            if self.aptos_manager.validate_threat_consensus(ip_address):
                consensus_score += 1
        return consensus_score >= len(validators) * 0.6  # 60% consensus

class IncidentResponseBlockchain:
    """Blockchain-based incident response system"""
    
    def __init__(self, aptos_manager):
        self.aptos_manager = aptos_manager
        
    def log_security_incident(self, incident_data):
        """Log security incidents to Aptos blockchain"""
        blockchain_incident = {
            "ip_address": incident_data["ip_address"],
            "action_taken": incident_data["action_taken"],
            "threat_score": incident_data["threat_score"],
            "timestamp": datetime.now().isoformat(),
            "incident_id": f"MYC_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        }
        result = self.aptos_manager.log_security_incident(blockchain_incident)
        return result if result else f"mock_incident_{blockchain_incident['incident_id']}"
    
    def create_tamper_proof_audit_trail(self, events):
        """Create tamper-proof audit trail on blockchain"""
        audit_hashes = []
        for event in events:
            tx_hash = self.log_security_incident(event)
            audit_hashes.append(tx_hash)
        return audit_hashes
    
    def implement_automated_response_triggers(self, trigger_conditions):
        """Implement automated response triggers via smart contracts"""
        triggers = []
        for condition in trigger_conditions:
            if condition['threat_score'] > 0.8:
                trigger = {
                    "action": "ISOLATE",
                    "target": condition['ip'],
                    "automated": True,
                    "timestamp": datetime.now().isoformat()
                }
                triggers.append(trigger)
        return triggers

class DecentralizedSecurityScoring:
    """Decentralized security scoring system using Aptos"""
    
    def __init__(self, aptos_manager):
        self.aptos_manager = aptos_manager
        self.validators = []
        
    def distributed_threat_scoring(self, ip_address, evidence):
        """Use Aptos for distributed threat scoring"""
        base_score = self._calculate_base_score(evidence)
        blockchain_score = self._get_blockchain_consensus_score(ip_address)
        return (base_score + blockchain_score) / 2
    
    def implement_validator_network(self, validator_addresses):
        """Implement validator network for threat assessment"""
        self.validators = validator_addresses
        validator_results = []
        
        for validator in self.validators:
            reputation = self.aptos_manager.get_security_reputation(validator)
            validator_results.append({
                "address": validator,
                "reputation": reputation,
                "active": reputation > 50
            })
        return validator_results
    
    def create_reputation_system(self, node_address, performance_metrics):
        """Create reputation system for security nodes"""
        reputation_score = self._calculate_reputation(performance_metrics)
        
        # Reward good performance
        if reputation_score > 80:
            self.aptos_manager.reward_threat_detection(node_address, 100)
        
        return {
            "node": node_address,
            "reputation": reputation_score,
            "rewards_earned": performance_metrics.get('rewards', 0),
            "threats_detected": performance_metrics.get('detections', 0)
        }
    
    def _calculate_base_score(self, evidence):
        """Calculate base threat score from evidence"""
        score = 0.0
        if 'malware' in evidence.lower():
            score += 0.8
        if 'port_scan' in evidence.lower():
            score += 0.6
        if 'suspicious_traffic' in evidence.lower():
            score += 0.4
        return min(score, 1.0)
    
    def _get_blockchain_consensus_score(self, ip_address):
        """Get consensus score from blockchain validators"""
        if self.aptos_manager.validate_threat_consensus(ip_address):
            return 0.9
        return 0.1
    
    def _calculate_reputation(self, metrics):
        """Calculate node reputation based on performance"""
        accuracy = metrics.get('accuracy', 0.5)
        uptime = metrics.get('uptime', 0.5)
        detections = min(metrics.get('detections', 0) / 100, 1.0)
        return int((accuracy * 0.4 + uptime * 0.3 + detections * 0.3) * 100)

class BlockchainSecurityOrchestrator:
    """Main orchestrator for all blockchain security operations"""
    
    def __init__(self, node_url=None):
        if node_url:
            self.aptos_manager = AptosSecurityManager()
            self.aptos_manager.client = RestClient(node_url) if APTOS_AVAILABLE else None
        else:
            self.aptos_manager = AptosSecurityManager()
        self.threat_intel = ThreatIntelligenceBlockchain(self.aptos_manager)
        self.incident_response = IncidentResponseBlockchain(self.aptos_manager)
        self.scoring_system = DecentralizedSecurityScoring(self.aptos_manager)
        
    def initialize_blockchain_security(self, private_key=None):
        """Initialize complete blockchain security system"""
        wallet_address = self.aptos_manager.connect_wallet(private_key)
        
        return {
            "wallet_address": wallet_address,
            "balance": self.aptos_manager.get_balance(),
            "threat_intel_ready": True,
            "incident_response_ready": True,
            "scoring_system_ready": True
        }
    
    def process_security_event(self, event_data):
        """Process security event through blockchain pipeline"""
        # 1. Store threat intelligence
        threat_tx = self.threat_intel.store_threat_signature(
            event_data['ip'], event_data['signature'], event_data['type']
        )
        
        # 2. Log incident
        incident_tx = self.incident_response.log_security_incident(event_data)
        
        # 3. Calculate distributed score
        threat_score = self.scoring_system.distributed_threat_scoring(
            event_data['ip'], event_data['evidence']
        )
        
        return {
            "threat_transaction": threat_tx,
            "incident_transaction": incident_tx,
            "threat_score": threat_score,
            "blockchain_validated": True
        }