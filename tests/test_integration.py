"""
Integration tests for MycoShield components
"""

import unittest
import torch
import json
from unittest.mock import Mock, patch
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mycoshield import (MyceliumGNN, NetworkProcessor, ThreatDetector, 
                       SecurityEnforcer, TrafficParser, MyceliumRLAgent)

class TestMycoShieldIntegration(unittest.TestCase):
    
    def setUp(self):
        """Set up integration test environment"""
        self.model = MyceliumGNN(input_dim=6)
        self.processor = NetworkProcessor()
        self.enforcer = SecurityEnforcer()
        self.detector = ThreatDetector(self.model, self.enforcer)
        self.parser = TrafficParser()
        self.rl_agent = MyceliumRLAgent(input_dim=6)
        
        # Sample network flows
        self.sample_flows = [
            {
                'orig_h': '192.168.1.1',
                'resp_h': '192.168.1.2',
                'duration': 10.0,
                'orig_bytes': 1024,
                'resp_bytes': 512,
                'orig_p': 80,
                'resp_p': 443,
                'proto': 'tcp'
            },
            {
                'orig_h': '192.168.1.2',
                'resp_h': '192.168.1.3',
                'duration': 5.0,
                'orig_bytes': 2048,
                'resp_bytes': 1024,
                'orig_p': 443,
                'resp_p': 80,
                'proto': 'tcp'
            }
        ]
    
    def test_end_to_end_detection_pipeline(self):
        """Test complete detection pipeline"""
        # 1. Parse network data
        graph_data, node_list, G = self.parser.create_graph(self.sample_flows, feature_dim=6)
        
        # 2. Process with network processor
        for flow in self.sample_flows:
            self.processor.update_graph(flow)
        
        processed_data, processed_nodes = self.processor.get_graph_data()
        
        # 3. Run threat detection
        with patch.object(self.model, 'forward') as mock_forward:
            # Mock high threat scores
            mock_forward.return_value = torch.tensor([[0.9], [0.8], [0.3]])
            
            anomalies = self.detector.detect_anomalies(
                processed_data, processed_nodes, threshold=0.7
            )
        
        # 4. Verify results
        self.assertGreater(len(anomalies), 0)
        self.assertGreater(len(self.detector.isolated_nodes), 0)
    
    @patch('subprocess.run')
    def test_security_enforcement_integration(self, mock_subprocess):
        """Test security enforcement integration"""
        mock_subprocess.return_value = Mock(returncode=0)
        
        # Create threat scenario
        graph_data, node_list, G = self.parser.create_graph(self.sample_flows, feature_dim=6)
        
        with patch.object(self.model, 'forward') as mock_forward:
            # Mock critical threat
            mock_forward.return_value = torch.tensor([[0.95], [0.85], [0.2]])
            
            # Run detection (should trigger enforcement)
            anomalies = self.detector.detect_anomalies(
                graph_data, node_list, threshold=0.7
            )
        
        # Verify enforcement was triggered
        self.assertGreater(len(self.enforcer.blocked_ips), 0)
        self.assertGreater(len(self.enforcer.incident_log), 0)
    
    def test_rl_agent_integration(self):
        """Test RL agent integration with detection system"""
        # Create graph data
        graph_data, node_list, G = self.parser.create_graph(self.sample_flows, feature_dim=6)
        
        # Get RL agent actions
        actions = self.rl_agent.select_action(graph_data, [0, 1, 2])
        
        # Simulate rewards based on actions
        rewards = {}
        for node_idx, action in actions.items():
            if action == 2:  # ISOLATE
                rewards[node_idx] = 1.0  # Good action
            elif action == 1:  # MONITOR
                rewards[node_idx] = 0.5  # Neutral
            else:  # ALLOW
                rewards[node_idx] = -0.5  # Bad for suspicious nodes
        
        # Store experience
        self.rl_agent.store_experience(graph_data, actions, rewards, graph_data)
        
        # Verify experience was stored
        self.assertGreater(len(self.rl_agent.memory), 0)
    
    def test_multimodal_detection_flow(self):
        """Test multi-modal detection integration"""
        from mycoshield.host import HostMonitor, MultiModalDetector
        
        # Initialize components
        host_monitor = HostMonitor()
        multimodal = MultiModalDetector(self.detector, host_monitor, None)
        
        # Create network data
        graph_data, node_list, G = self.parser.create_graph(self.sample_flows, feature_dim=6)
        
        # Run comprehensive analysis
        with patch.object(self.model, 'forward') as mock_forward, \
             patch.object(host_monitor, 'detect_suspicious_processes') as mock_host:
            
            mock_forward.return_value = torch.tensor([[0.8], [0.6], [0.3]])
            mock_host.return_value = [
                {'type': 'suspicious_binary', 'threat_score': 0.7}
            ]
            
            results = multimodal.comprehensive_analysis((graph_data, node_list))
        
        # Verify correlation
        self.assertIn('network', results)
        self.assertIn('host', results)
        self.assertGreater(results['correlation_score'], 0)
    
    def test_configuration_integration(self):
        """Test configuration system integration"""
        config = {
            'email': {'enabled': False},
            'firewall': {'enabled': True},
            'scan_interval': 60
        }
        
        # Initialize with config
        enforcer = SecurityEnforcer(config)
        
        # Verify config was applied
        self.assertEqual(enforcer.config['scan_interval'], 60)
        self.assertFalse(enforcer.config['email']['enabled'])
    
    def test_error_handling_integration(self):
        """Test error handling across components"""
        # Test with invalid data
        invalid_flows = [
            {
                'orig_h': None,  # Invalid IP
                'resp_h': '192.168.1.2',
                'duration': 'invalid',  # Invalid duration
            }
        ]
        
        # Should handle gracefully without crashing
        try:
            graph_data, node_list, G = self.parser.create_graph(invalid_flows, feature_dim=6)
            # Should not crash
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"Integration failed with error: {e}")
    
    def test_performance_integration(self):
        """Test performance with larger datasets"""
        # Generate larger dataset
        large_flows = []
        for i in range(100):
            flow = {
                'orig_h': f'192.168.1.{i % 50 + 1}',
                'resp_h': f'10.0.0.{i % 30 + 1}',
                'duration': float(i % 60),
                'orig_bytes': i * 100,
                'resp_bytes': i * 50,
                'orig_p': 80 + (i % 10),
                'resp_p': 443 + (i % 5),
                'proto': 'tcp' if i % 2 == 0 else 'udp'
            }
            large_flows.append(flow)
        
        # Process large dataset
        import time
        start_time = time.time()
        
        graph_data, node_list, G = self.parser.create_graph(large_flows, feature_dim=6)
        
        processing_time = time.time() - start_time
        
        # Should complete within reasonable time (5 seconds)
        self.assertLess(processing_time, 5.0)
        self.assertIsNotNone(graph_data)
        self.assertGreater(len(node_list), 0)

class TestEnterpriseIntegration(unittest.TestCase):
    
    def setUp(self):
        """Set up enterprise integration tests"""
        from mycoshield.enterprise import EnterpriseMycoShield
        
        self.config = {
            'scan_interval': 1,  # Fast scanning for tests
            'auto_response': True
        }
        self.enterprise = EnterpriseMycoShield(self.config)
    
    def test_enterprise_initialization(self):
        """Test enterprise platform initialization"""
        # Verify all components are initialized
        self.assertIsNotNone(self.enterprise.host_monitor)
        self.assertIsNotNone(self.enterprise.security_enforcer)
        self.assertIsNotNone(self.enterprise.registry_monitor)
        self.assertIsNotNone(self.enterprise.malware_scanner)
    
    @patch('time.sleep')  # Speed up test
    def test_monitoring_lifecycle(self, mock_sleep):
        """Test monitoring start/stop lifecycle"""
        # Start monitoring
        self.enterprise.start_monitoring()
        self.assertTrue(self.enterprise.monitoring_active)
        self.assertIsNotNone(self.enterprise.monitoring_thread)
        
        # Stop monitoring
        self.enterprise.stop_monitoring()
        self.assertFalse(self.enterprise.monitoring_active)
    
    def test_comprehensive_scan_integration(self):
        """Test comprehensive scanning integration"""
        # Mock individual scanners to avoid system dependencies
        with patch.object(self.enterprise.host_monitor, 'detect_suspicious_processes') as mock_host, \
             patch.object(self.enterprise.registry_monitor, 'detect_registry_changes') as mock_registry, \
             patch.object(self.enterprise.malware_scanner, 'scan_running_processes') as mock_malware:
            
            mock_host.return_value = [{'type': 'test', 'threat_score': 0.8}]
            mock_registry.return_value = [{'type': 'registry_mod', 'threat_score': 0.6}]
            mock_malware.return_value = []
            
            results = self.enterprise.comprehensive_scan()
        
        # Verify scan results structure
        self.assertIn('timestamp', results)
        self.assertIn('host', results)
        self.assertIn('registry', results)
        self.assertIn('malware', results)
    
    def test_threat_processing_integration(self):
        """Test threat processing and response"""
        # Create mock threats
        threats = {
            'timestamp': '2024-01-01T00:00:00',
            'host': {
                'processes': [{'threat_score': 0.9, 'pid': 1234}]
            },
            'registry': [{'threat_score': 0.8}],
            'malware': []
        }
        
        with patch.object(self.enterprise.security_enforcer, 'isolate_node') as mock_isolate:
            self.enterprise._process_threats(threats)
        
        # Verify threat was processed
        self.assertGreater(len(self.enterprise.threat_database), 0)
    
    def test_dashboard_data_integration(self):
        """Test security dashboard data generation"""
        dashboard = self.enterprise.get_security_dashboard()
        
        # Verify dashboard structure
        self.assertIn('system_status', dashboard)
        self.assertIn('total_threats', dashboard)
        self.assertIn('monitoring_active', dashboard)
        self.assertIn('device_fingerprint', dashboard)

if __name__ == '__main__':
    unittest.main()