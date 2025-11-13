"""
Unit tests for MycoShield data processing components
"""

import unittest
from unittest.mock import Mock, patch, mock_open
import json
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mycoshield.data import TrafficParser, ZeekLogTailer

class TestTrafficParser(unittest.TestCase):
    
    def setUp(self):
        self.parser = TrafficParser()
    
    def test_initialization(self):
        """Test TrafficParser initialization"""
        self.assertIsInstance(self.parser, TrafficParser)
    
    @patch('scapy.all.rdpcap')
    def test_parse_pcap(self, mock_rdpcap):
        """Test PCAP file parsing"""
        # Mock scapy packet
        mock_packet = Mock()
        mock_packet.haslayer.return_value = True
        mock_packet.__getitem__.side_effect = lambda x: Mock(
            src='192.168.1.1', 
            dst='192.168.1.2',
            sport=80,
            dport=443
        )
        mock_packet.time = 1234567890.0
        mock_packet.__len__ = Mock(return_value=1024)
        
        mock_rdpcap.return_value = [mock_packet] * 5
        
        flows = self.parser.parse_pcap('test.pcap')
        
        # Check flows were extracted
        self.assertGreater(len(flows), 0)
        mock_rdpcap.assert_called_once_with('test.pcap')
    
    @patch('scapy.all.rdpcap')
    def test_parse_pcap_file_not_found(self, mock_rdpcap):
        """Test PCAP parsing with missing file"""
        mock_rdpcap.side_effect = FileNotFoundError()
        
        flows = self.parser.parse_pcap('nonexistent.pcap')
        
        # Should return empty list
        self.assertEqual(flows, [])
    
    def test_create_graph_empty_flows(self):
        """Test graph creation with empty flows"""
        graph_data, node_list, G = self.parser.create_graph([], feature_dim=6)
        
        self.assertIsNone(graph_data)
        self.assertEqual(node_list, [])
        self.assertEqual(len(G.nodes()), 0)
    
    def test_create_graph_with_flows(self):
        """Test graph creation with sample flows"""
        flows = [
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
                'orig_bytes': 256,
                'resp_bytes': 128,
                'orig_p': 443,
                'resp_p': 80,
                'proto': 'tcp'
            }
        ]
        
        graph_data, node_list, G = self.parser.create_graph(flows, feature_dim=6)
        
        # Check graph structure
        self.assertIsNotNone(graph_data)
        self.assertEqual(len(node_list), 3)
        self.assertEqual(len(G.nodes()), 3)
        self.assertEqual(len(G.edges()), 2)
        
        # Check graph data tensor shapes
        self.assertEqual(graph_data.x.shape[0], 3)  # 3 nodes
        self.assertEqual(graph_data.x.shape[1], 6)  # 6 features
    
    def test_feature_padding(self):
        """Test feature padding for different dimensions"""
        flows = [
            {
                'orig_h': '192.168.1.1',
                'resp_h': '192.168.1.2',
                'duration': 10.0,
                'orig_bytes': 1024,
                'resp_bytes': 512,
                'orig_p': 80,
                'resp_p': 443,
                'proto': 'tcp'
            }
        ]
        
        # Test with larger feature dimension
        graph_data, node_list, G = self.parser.create_graph(flows, feature_dim=41)
        
        # Should pad features to 41 dimensions
        self.assertEqual(graph_data.x.shape[1], 41)

class TestZeekLogTailer(unittest.TestCase):
    
    def setUp(self):
        self.tailer = ZeekLogTailer('test_conn.log')
    
    def test_initialization(self):
        """Test ZeekLogTailer initialization"""
        self.assertEqual(self.tailer.log_file, 'test_conn.log')
        self.assertEqual(len(self.tailer.connections), 0)
    
    @patch('builtins.open', new_callable=mock_open, read_data='#separator \\x09\n#fields\tts\tid.orig_h\tid.resp_h\n1234567890.0\t192.168.1.1\t192.168.1.2\n')
    def test_parse_zeek_log(self, mock_file):
        """Test Zeek log parsing"""
        connections = self.tailer.parse_zeek_log()
        
        # Should parse one connection
        self.assertEqual(len(connections), 1)
        self.assertEqual(connections[0]['orig_h'], '192.168.1.1')
        self.assertEqual(connections[0]['resp_h'], '192.168.1.2')
    
    @patch('builtins.open', side_effect=FileNotFoundError())
    def test_parse_zeek_log_file_not_found(self, mock_file):
        """Test Zeek log parsing with missing file"""
        connections = self.tailer.parse_zeek_log()
        
        # Should return empty list
        self.assertEqual(connections, [])
    
    @patch('builtins.open', new_callable=mock_open, read_data='invalid log format\n')
    def test_parse_zeek_log_invalid_format(self, mock_file):
        """Test Zeek log parsing with invalid format"""
        connections = self.tailer.parse_zeek_log()
        
        # Should handle gracefully
        self.assertEqual(connections, [])
    
    def test_get_new_connections(self):
        """Test getting new connections"""
        # Add some test connections
        self.tailer.connections = [
            {'ts': 1234567890.0, 'orig_h': '192.168.1.1'},
            {'ts': 1234567891.0, 'orig_h': '192.168.1.2'},
            {'ts': 1234567892.0, 'orig_h': '192.168.1.3'},
        ]
        
        # Get connections after timestamp
        new_connections = self.tailer.get_new_connections(since_timestamp=1234567890.5)
        
        # Should return 2 connections
        self.assertEqual(len(new_connections), 2)
        self.assertEqual(new_connections[0]['orig_h'], '192.168.1.2')
        self.assertEqual(new_connections[1]['orig_h'], '192.168.1.3')
    
    def test_get_new_connections_empty(self):
        """Test getting new connections with no new data"""
        self.tailer.connections = [
            {'ts': 1234567890.0, 'orig_h': '192.168.1.1'},
        ]
        
        # Get connections after latest timestamp
        new_connections = self.tailer.get_new_connections(since_timestamp=1234567900.0)
        
        # Should return empty list
        self.assertEqual(len(new_connections), 0)
    
    @patch.object(ZeekLogTailer, 'parse_zeek_log')
    def test_tail_logs(self, mock_parse):
        """Test log tailing functionality"""
        # Mock parse_zeek_log to return test data
        mock_parse.return_value = [
            {'ts': 1234567890.0, 'orig_h': '192.168.1.1'},
            {'ts': 1234567891.0, 'orig_h': '192.168.1.2'},
        ]
        
        # Call tail_logs
        new_connections = self.tailer.tail_logs()
        
        # Should return new connections
        self.assertEqual(len(new_connections), 2)
        mock_parse.assert_called_once()

if __name__ == '__main__':
    unittest.main()