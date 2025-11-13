"""
Unit tests for MycoShield core components
"""

import unittest
import torch
import networkx as nx
from unittest.mock import Mock, patch
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mycoshield.core import NetworkProcessor, ThreatDetector
from mycoshield.models import MyceliumGNN

class TestNetworkProcessor(unittest.TestCase):
    
    def setUp(self):
        self.processor = NetworkProcessor()
        self.sample_conn = {
            'orig_h': '192.168.1.1',
            'resp_h': '192.168.1.2',
            'duration': 10.5,
            'orig_bytes': 1024,
            'resp_bytes': 512,
            'orig_p': 80,
            'resp_p': 443,
            'proto': 'tcp',
            'threat_score': 0.3
        }
    
    def test_initialization(self):
        """Test NetworkProcessor initialization"""
        self.assertIsInstance(self.processor.G, nx.Graph)
        self.assertEqual(len(self.processor.node_features), 0)
    
    def test_update_graph_new_nodes(self):
        """Test adding new nodes to graph"""
        self.processor.update_graph(self.sample_conn)
        
        # Check nodes were added
        self.assertIn('192.168.1.1', self.processor.G.nodes())
        self.assertIn('192.168.1.2', self.processor.G.nodes())
        
        # Check edge was added
        self.assertTrue(self.processor.G.has_edge('192.168.1.1', '192.168.1.2'))
    
    def test_update_graph_existing_nodes(self):
        """Test updating existing nodes"""
        # Add connection twice
        self.processor.update_graph(self.sample_conn)
        self.processor.update_graph(self.sample_conn)
        
        # Check edge weight increased
        edge_weight = self.processor.G['192.168.1.1']['192.168.1.2']['weight']
        self.assertEqual(edge_weight, 2)
    
    def test_feature_extraction(self):
        """Test feature extraction from connection data"""
        self.processor.update_graph(self.sample_conn)
        
        # Check features were stored
        self.assertIn('192.168.1.1', self.processor.node_features)
        self.assertIn('192.168.1.2', self.processor.node_features)
        
        # Check feature vector length
        features = self.processor.node_features['192.168.1.1'][0]
        self.assertEqual(len(features), 10)
    
    def test_get_graph_data(self):
        """Test graph data conversion"""
        self.processor.update_graph(self.sample_conn)
        
        # Add another connection for more nodes
        conn2 = self.sample_conn.copy()
        conn2['resp_h'] = '192.168.1.3'
        self.processor.update_graph(conn2)
        
        graph_data, node_list = self.processor.get_graph_data()
        
        # Check data structure
        self.assertIsNotNone(graph_data)
        self.assertIsNotNone(node_list)
        self.assertEqual(len(node_list), 3)
        self.assertEqual(graph_data.x.shape[0], 3)
    
    def test_empty_graph(self):
        """Test handling of empty graph"""
        graph_data, node_list = self.processor.get_graph_data()
        
        self.assertIsNone(graph_data)
        self.assertIsNone(node_list)

class TestThreatDetector(unittest.TestCase):
    
    def setUp(self):
        self.model = MyceliumGNN(input_dim=10)
        self.detector = ThreatDetector(self.model)
        
        # Create sample graph data
        self.x = torch.randn(3, 10)
        self.edge_index = torch.tensor([[0, 1], [1, 2]], dtype=torch.long)
        from torch_geometric.data import Data
        self.graph_data = Data(x=self.x, edge_index=self.edge_index)
        self.node_list = ['192.168.1.1', '192.168.1.2', '192.168.1.3']
    
    def test_initialization(self):
        """Test ThreatDetector initialization"""
        self.assertEqual(len(self.detector.isolated_nodes), 0)
        self.assertIsNone(self.detector.security_enforcer)
    
    def test_detect_anomalies_no_data(self):
        """Test anomaly detection with no data"""
        anomalies = self.detector.detect_anomalies(None, [])
        self.assertEqual(anomalies, {})
    
    @patch('torch.no_grad')
    def test_detect_anomalies_with_data(self, mock_no_grad):
        """Test anomaly detection with sample data"""
        # Mock model output
        with patch.object(self.model, 'forward') as mock_forward:
            mock_forward.return_value = torch.tensor([[0.8], [0.3], [0.9]])
            
            anomalies = self.detector.detect_anomalies(
                self.graph_data, self.node_list, threshold=0.7
            )
            
            # Check results
            self.assertEqual(len(anomalies), 3)
            self.assertAlmostEqual(anomalies['192.168.1.1'], 0.8, places=1)
            self.assertAlmostEqual(anomalies['192.168.1.2'], 0.3, places=1)
            self.assertAlmostEqual(anomalies['192.168.1.3'], 0.9, places=1)
            
            # Check isolated nodes
            self.assertIn('192.168.1.1', self.detector.isolated_nodes)
            self.assertIn('192.168.1.3', self.detector.isolated_nodes)
            self.assertNotIn('192.168.1.2', self.detector.isolated_nodes)
    
    def test_get_threat_summary(self):
        """Test threat summary calculation"""
        anomalies = {
            'node1': 0.9,  # infected
            'node2': 0.6,  # suspicious
            'node3': 0.3,  # healthy
            'node4': 0.8,  # infected
        }
        
        summary = self.detector.get_threat_summary(anomalies, threshold=0.7)
        
        self.assertEqual(summary['infected'], 2)
        self.assertEqual(summary['suspicious'], 1)
        self.assertEqual(summary['healthy'], 1)
        self.assertEqual(summary['total'], 4)
    
    def test_security_enforcer_integration(self):
        """Test integration with security enforcer"""
        mock_enforcer = Mock()
        detector = ThreatDetector(self.model, mock_enforcer)
        
        with patch.object(self.model, 'forward') as mock_forward:
            mock_forward.return_value = torch.tensor([[0.9], [0.6], [0.3]])
            
            detector.detect_anomalies(self.graph_data, self.node_list, threshold=0.7)
            
            # Check enforcer was called
            mock_enforcer.isolate_node.assert_called()

if __name__ == '__main__':
    unittest.main()