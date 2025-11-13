"""
Unit tests for MycoShield models
"""

import unittest
import torch
import torch.nn.functional as F
from torch_geometric.data import Data
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mycoshield.models import MyceliumGNN, MyceliumDQN

class TestMyceliumGNN(unittest.TestCase):
    
    def setUp(self):
        self.input_dim = 10
        self.hidden_dim = 64
        self.model = MyceliumGNN(self.input_dim, self.hidden_dim)
        
        # Create sample graph data
        self.x = torch.randn(5, self.input_dim)
        self.edge_index = torch.tensor([[0, 1, 2, 3], [1, 2, 3, 4]], dtype=torch.long)
        self.graph_data = Data(x=self.x, edge_index=self.edge_index)
    
    def test_model_initialization(self):
        """Test model initialization"""
        self.assertEqual(self.model.conv1.in_channels, self.input_dim)
        self.assertEqual(self.model.conv1.out_channels, self.hidden_dim)
        self.assertEqual(self.model.conv2.in_channels, self.hidden_dim)
        self.assertEqual(self.model.conv2.out_channels, self.hidden_dim)
        self.assertEqual(self.model.conv3.in_channels, self.hidden_dim)
        self.assertEqual(self.model.conv3.out_channels, 1)
    
    def test_forward_pass(self):
        """Test forward pass"""
        output = self.model(self.x, self.edge_index)
        
        # Check output shape
        self.assertEqual(output.shape, (5, 1))
        
        # Check output is in valid range (after sigmoid)
        self.assertTrue(torch.all(output >= 0))
        self.assertTrue(torch.all(output <= 1))
    
    def test_model_training_mode(self):
        """Test model can switch between train/eval modes"""
        self.model.train()
        self.assertTrue(self.model.training)
        
        self.model.eval()
        self.assertFalse(self.model.training)
    
    def test_gradient_computation(self):
        """Test gradients are computed correctly"""
        self.model.train()
        output = self.model(self.x, self.edge_index)
        loss = F.mse_loss(output, torch.ones_like(output))
        loss.backward()
        
        # Check gradients exist
        for param in self.model.parameters():
            self.assertIsNotNone(param.grad)

class TestMyceliumDQN(unittest.TestCase):
    
    def setUp(self):
        self.input_dim = 10
        self.hidden_dim = 64
        self.model = MyceliumDQN(self.input_dim, self.hidden_dim)
        self.x = torch.randn(5, self.input_dim)
        self.edge_index = torch.tensor([[0, 1, 2, 3], [1, 2, 3, 4]], dtype=torch.long)
    
    def test_dqn_initialization(self):
        """Test DQN initialization"""
        self.assertEqual(self.model.gnn.conv1.in_channels, self.input_dim)
        self.assertEqual(self.model.fc1.in_features, self.hidden_dim)
        self.assertEqual(self.model.fc3.out_features, 3)  # 3 actions
    
    def test_dqn_forward_pass(self):
        """Test DQN forward pass"""
        output = self.model(self.x, self.edge_index)
        
        # Check output shape (5 nodes, 3 actions each)
        self.assertEqual(output.shape, (5, 3))
    
    def test_action_selection(self):
        """Test action selection from Q-values"""
        output = self.model(self.x, self.edge_index)
        actions = torch.argmax(output, dim=1)
        
        # Check actions are valid (0, 1, or 2)
        self.assertTrue(torch.all(actions >= 0))
        self.assertTrue(torch.all(actions <= 2))

if __name__ == '__main__':
    unittest.main()