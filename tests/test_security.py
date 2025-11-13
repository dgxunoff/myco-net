"""
Unit tests for MycoShield security components
"""

import unittest
from unittest.mock import Mock, patch, mock_open
import json
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mycoshield.security import SecurityEnforcer, NetworkMonitor

class TestSecurityEnforcer(unittest.TestCase):
    
    def setUp(self):
        self.config = {
            'email': {'enabled': False},
            'firewall': {'enabled': True}
        }
        self.enforcer = SecurityEnforcer(self.config)
    
    def test_initialization(self):
        """Test SecurityEnforcer initialization"""
        self.assertEqual(len(self.enforcer.blocked_ips), 0)
        self.assertEqual(len(self.enforcer.incident_log), 0)
        self.assertEqual(self.enforcer.config, self.config)
    
    @patch('subprocess.run')
    @patch('platform.system')
    def test_block_ip_windows(self, mock_system, mock_subprocess):
        """Test IP blocking on Windows"""
        mock_system.return_value = 'Windows'
        mock_subprocess.return_value = Mock(returncode=0)
        
        result = self.enforcer.isolate_node('192.168.1.100', 0.9, 'ISOLATE')
        
        self.assertTrue(result)
        self.assertIn('192.168.1.100', self.enforcer.blocked_ips)
        mock_subprocess.assert_called()
    
    @patch('subprocess.run')
    @patch('platform.system')
    def test_block_ip_linux(self, mock_system, mock_subprocess):
        """Test IP blocking on Linux"""
        mock_system.return_value = 'Linux'
        mock_subprocess.return_value = Mock(returncode=0)
        
        result = self.enforcer.isolate_node('192.168.1.100', 0.9, 'ISOLATE')
        
        self.assertTrue(result)
        self.assertIn('192.168.1.100', self.enforcer.blocked_ips)
    
    @patch('subprocess.run')
    def test_block_ip_failure(self, mock_subprocess):
        """Test handling of firewall command failure"""
        mock_subprocess.side_effect = Exception("Command failed")
        
        # Should not raise exception
        self.enforcer.isolate_node('192.168.1.100', 0.9, 'ISOLATE')
        
        # IP should not be in blocked list
        self.assertNotIn('192.168.1.100', self.enforcer.blocked_ips)
    
    def test_monitor_action(self):
        """Test monitoring action"""
        result = self.enforcer.isolate_node('192.168.1.100', 0.6, 'MONITOR')
        
        self.assertFalse(result)  # Monitor doesn't block
        self.assertNotIn('192.168.1.100', self.enforcer.blocked_ips)
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_incident_logging(self, mock_json_dump, mock_file):
        """Test incident logging"""
        self.enforcer._log_incident('192.168.1.100', 0.9, 'ISOLATED')
        
        # Check incident was logged
        self.assertEqual(len(self.enforcer.incident_log), 1)
        incident = self.enforcer.incident_log[0]
        
        self.assertEqual(incident['ip_address'], '192.168.1.100')
        self.assertEqual(incident['threat_score'], 0.9)
        self.assertEqual(incident['action_taken'], 'ISOLATED')
        
        # Check file was written
        mock_file.assert_called()
        mock_json_dump.assert_called()
    
    @patch('subprocess.run')
    @patch('platform.system')
    def test_unblock_ip(self, mock_system, mock_subprocess):
        """Test IP unblocking"""
        mock_system.return_value = 'Windows'
        mock_subprocess.return_value = Mock(returncode=0)
        
        # First block the IP
        self.enforcer.blocked_ips.add('192.168.1.100')
        
        # Then unblock it
        self.enforcer.unblock_ip('192.168.1.100')
        
        self.assertNotIn('192.168.1.100', self.enforcer.blocked_ips)
        mock_subprocess.assert_called()
    
    def test_get_incident_summary(self):
        """Test incident summary generation"""
        # Add some test incidents
        self.enforcer.incident_log = [
            {'action_taken': 'ISOLATED', 'timestamp': '2024-01-01'},
            {'action_taken': 'MONITORING', 'timestamp': '2024-01-02'},
            {'action_taken': 'ISOLATED', 'timestamp': '2024-01-03'},
        ]
        self.enforcer.blocked_ips = {'192.168.1.1', '192.168.1.2'}
        
        summary = self.enforcer.get_incident_summary()
        
        self.assertEqual(summary['total_incidents'], 3)
        self.assertEqual(summary['blocked_ips'], 2)
        self.assertEqual(summary['monitored_ips'], 1)
        self.assertEqual(summary['currently_blocked'], 2)

class TestNetworkMonitor(unittest.TestCase):
    
    def setUp(self):
        self.monitor = NetworkMonitor()
    
    @patch('builtins.open', new_callable=mock_open, read_data='[]')
    def test_initialization(self, mock_file):
        """Test NetworkMonitor initialization"""
        monitor = NetworkMonitor()
        self.assertEqual(monitor.monitoring_rules, [])
    
    @patch('builtins.open', new_callable=mock_open, read_data='[{"ip": "192.168.1.1", "alert_threshold": 0.5}]')
    def test_load_monitoring_rules(self, mock_file):
        """Test loading monitoring rules"""
        monitor = NetworkMonitor()
        self.assertEqual(len(monitor.monitoring_rules), 1)
        self.assertEqual(monitor.monitoring_rules[0]['ip'], '192.168.1.1')
    
    def test_check_monitored_ips(self):
        """Test checking monitored IPs"""
        # Set up monitoring rules
        self.monitor.monitoring_rules = [
            {'ip': '192.168.1.1', 'alert_threshold': 0.5}
        ]
        
        # Create test connections with high volume
        connections = [
            {'orig_h': '192.168.1.1', 'resp_h': '10.0.0.1'},
            {'orig_h': '192.168.1.1', 'resp_h': '10.0.0.2'},
        ] * 6  # 12 connections total
        
        alerts = self.monitor.check_monitored_ips(connections)
        
        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0]['ip'], '192.168.1.1')
        self.assertEqual(alerts[0]['connection_count'], 12)
    
    def test_check_monitored_ips_no_alerts(self):
        """Test no alerts for normal activity"""
        self.monitor.monitoring_rules = [
            {'ip': '192.168.1.1', 'alert_threshold': 0.5}
        ]
        
        # Low connection volume
        connections = [
            {'orig_h': '192.168.1.1', 'resp_h': '10.0.0.1'},
        ]
        
        alerts = self.monitor.check_monitored_ips(connections)
        self.assertEqual(len(alerts), 0)

if __name__ == '__main__':
    unittest.main()