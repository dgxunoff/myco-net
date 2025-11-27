"""
Tests for Blockchain Integration
"""

import unittest
from unittest.mock import Mock, patch
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mycoshield.blockchain_integration import (
    BlockchainSecurityOrchestrator,
    ThreatIntelligenceBlockchain,
    IncidentResponseBlockchain,
    DecentralizedSecurityScoring
)
from mycoshield.aptos_security import AptosSecurityManager

class TestBlockchainIntegration(unittest.TestCase):
    
    def setUp(self):
        self.orchestrator = BlockchainSecurityOrchestrator()
        
    def test_orchestrator_initialization(self):
        """Test blockchain orchestrator initialization"""
        self.assertIsNotNone(self.orchestrator.aptos_manager)
        self.assertIsNotNone(self.orchestrator.threat_intel)
        self.assertIsNotNone(self.orchestrator.incident_response)
        self.assertIsNotNone(self.orchestrator.scoring_system)
    
    def test_blockchain_security_initialization(self):
        """Test blockchain security system initialization"""
        result = self.orchestrator.initialize_blockchain_security()
        
        self.assertIn('wallet_address', result)
        self.assertIn('balance', result)
        self.assertIn('threat_intel_ready', result)
        self.assertIn('incident_response_ready', result)
        self.assertIn('scoring_system_ready', result)
    
    def test_security_event_processing(self):
        """Test security event processing through blockchain pipeline"""
        event_data = {
            'ip': '192.168.1.100',
            'ip_address': '192.168.1.100',
            'signature': 'test_hash',
            'type': 'malware',
            'evidence': 'test evidence',
            'action_taken': 'ISOLATED',
            'threat_score': 0.85,
            'timestamp': '2024-01-01T12:00:00'
        }
        
        result = self.orchestrator.process_security_event(event_data)
        
        self.assertIn('threat_transaction', result)
        self.assertIn('incident_transaction', result)
        self.assertIn('threat_score', result)
        self.assertIn('blockchain_validated', result)

class TestThreatIntelligenceBlockchain(unittest.TestCase):
    
    def setUp(self):
        self.aptos_manager = AptosSecurityManager()
        self.threat_intel = ThreatIntelligenceBlockchain(self.aptos_manager)
    
    def test_store_threat_signature(self):
        """Test storing threat signature on blockchain"""
        result = self.threat_intel.store_threat_signature(
            '192.168.1.100', 'hash123', 'malware'
        )
        self.assertIsNotNone(result)
    
    def test_create_immutable_threat_db(self):
        """Test creating immutable threat database"""
        threat_entries = [
            {'ip': '192.168.1.1', 'score': 0.9, 'type': 'malware'},
            {'ip': '192.168.1.2', 'score': 0.7, 'type': 'port_scan'}
        ]
        
        results = self.threat_intel.create_immutable_threat_db(threat_entries)
        self.assertEqual(len(results), 2)

class TestIncidentResponseBlockchain(unittest.TestCase):
    
    def setUp(self):
        self.aptos_manager = AptosSecurityManager()
        self.incident_response = IncidentResponseBlockchain(self.aptos_manager)
    
    def test_log_security_incident(self):
        """Test logging security incident to blockchain"""
        incident_data = {
            'ip_address': '192.168.1.100',
            'action_taken': 'ISOLATED',
            'threat_score': 0.85
        }
        
        result = self.incident_response.log_security_incident(incident_data)
        self.assertIsNotNone(result)
    
    def test_create_tamper_proof_audit_trail(self):
        """Test creating tamper-proof audit trail"""
        events = [
            {'ip_address': '192.168.1.1', 'action_taken': 'BLOCKED', 'threat_score': 0.9},
            {'ip_address': '192.168.1.2', 'action_taken': 'MONITORED', 'threat_score': 0.6}
        ]
        
        audit_hashes = self.incident_response.create_tamper_proof_audit_trail(events)
        self.assertEqual(len(audit_hashes), 2)

class TestDecentralizedSecurityScoring(unittest.TestCase):
    
    def setUp(self):
        self.aptos_manager = AptosSecurityManager()
        self.scoring_system = DecentralizedSecurityScoring(self.aptos_manager)
    
    def test_distributed_threat_scoring(self):
        """Test distributed threat scoring"""
        score = self.scoring_system.distributed_threat_scoring(
            '192.168.1.100', 'malware detected'
        )
        self.assertIsInstance(score, float)
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)
    
    def test_implement_validator_network(self):
        """Test validator network implementation"""
        validators = ['0x123', '0x456', '0x789']
        results = self.scoring_system.implement_validator_network(validators)
        
        self.assertEqual(len(results), 3)
        for result in results:
            self.assertIn('address', result)
            self.assertIn('reputation', result)
            self.assertIn('active', result)
    
    def test_create_reputation_system(self):
        """Test reputation system creation"""
        performance_metrics = {
            'accuracy': 0.92,
            'uptime': 0.98,
            'detections': 150,
            'rewards': 500
        }
        
        result = self.scoring_system.create_reputation_system('0x123', performance_metrics)
        
        self.assertIn('node', result)
        self.assertIn('reputation', result)
        self.assertIn('rewards_earned', result)
        self.assertIn('threats_detected', result)

if __name__ == '__main__':
    unittest.main()