"""
Unit tests for MycoShield RL components
"""

import unittest
import torch
from unittest.mock import Mock, patch
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mycoshield.rl import MyceliumRLAgent, ReplayBuffer, ACTIONS
from torch_geometric.data import Data

class TestReplayBuffer(unittest.TestCase):
    
    def setUp(self):
        self.buffer = ReplayBuffer(capacity=100)
    
    def test_initialization(self):
        """Test ReplayBuffer initialization"""
        self.assertEqual(len(self.buffer), 0)
        self.assertEqual(self.buffer.buffer.maxlen, 100)
    
    def test_push_experience(self):
        """Test adding experience to buffer"""
        state = torch.randn(5, 10)
        action = 1
        reward = 0.5
        next_state = torch.randn(5, 10)
        done = False
        
        self.buffer.push(state, action, reward, next_state, done)
        
        self.assertEqual(len(self.buffer), 1)
    
    def test_sample_experiences(self):
        """Test sampling from buffer"""
        # Add multiple experiences
        for i in range(10):
            state = torch.randn(5, 10)
            self.buffer.push(state, i % 3, 0.5, state, False)
        
        # Sample batch
        batch = self.buffer.sample(5)
        self.assertEqual(len(batch), 5)
    
    def test_buffer_overflow(self):
        """Test buffer capacity limit"""
        # Fill buffer beyond capacity
        for i in range(150):
            state = torch.randn(5, 10)
            self.buffer.push(state, 0, 0.0, state, False)
        
        # Should not exceed capacity
        self.assertEqual(len(self.buffer), 100)

class TestMyceliumRLAgent(unittest.TestCase):
    
    def setUp(self):
        self.agent = MyceliumRLAgent(input_dim=10, hidden_dim=32, lr=0.001)
        
        # Create sample graph data
        self.x = torch.randn(3, 10)
        self.edge_index = torch.tensor([[0, 1], [1, 2]], dtype=torch.long)
        self.state = Data(x=self.x, edge_index=self.edge_index)
    
    def test_initialization(self):
        """Test RL agent initialization"""
        self.assertEqual(self.agent.epsilon, 1.0)
        self.assertEqual(self.agent.epsilon_min, 0.01)
        self.assertEqual(self.agent.gamma, 0.95)
        self.assertEqual(len(self.agent.episode_rewards), 0)
    
    def test_select_action_random(self):
        """Test random action selection (exploration)"""
        # Force random action
        self.agent.epsilon = 1.0
        
        actions = self.agent.select_action(self.state, [0, 1, 2])
        
        # Check actions are valid
        for node_idx, action in actions.items():
            self.assertIn(action, [0, 1, 2])
            self.assertIn(node_idx, [0, 1, 2])
    
    def test_select_action_greedy(self):
        """Test greedy action selection (exploitation)"""
        # Force greedy action
        self.agent.epsilon = 0.0
        
        with patch.object(self.agent.q_network, 'forward') as mock_forward:
            # Mock Q-values favoring action 2
            mock_forward.return_value = torch.tensor([[0.1, 0.2, 0.9], 
                                                     [0.3, 0.1, 0.8], 
                                                     [0.2, 0.4, 0.7]])
            
            actions = self.agent.select_action(self.state, [0, 1, 2])
            
            # All actions should be 2 (highest Q-value)
            for action in actions.values():
                self.assertEqual(action, 2)
    
    def test_store_experience(self):
        """Test experience storage"""
        actions = {0: 1, 1: 2}
        rewards = {0: 0.5, 1: -0.2}
        
        self.agent.store_experience(self.state, actions, rewards, self.state)
        
        # Check experiences were stored
        self.assertEqual(len(self.agent.memory), 2)
    
    def test_train_insufficient_data(self):
        """Test training with insufficient data"""
        # Should not crash with empty buffer
        self.agent.train()
        
        # Add some experiences but less than batch size
        for i in range(10):
            self.agent.memory.push(self.state, 0, 0.0, self.state, False)
        
        # Should not train with insufficient data
        self.agent.train()
    
    def test_train_with_data(self):
        """Test training with sufficient data"""
        # Fill buffer with experiences
        for i in range(50):
            self.agent.memory.push(self.state, i % 3, 0.1, self.state, False)
        
        # Mock the forward passes to avoid complex tensor operations
        with patch.object(self.agent.q_network, 'forward') as mock_q_forward, \
             patch.object(self.agent.target_network, 'forward') as mock_target_forward:
            
            mock_q_forward.return_value = torch.randn(3, 3)
            mock_target_forward.return_value = torch.randn(3, 3)
            
            # Should not crash
            self.agent.train()
    
    def test_epsilon_decay(self):
        """Test epsilon decay during training"""
        initial_epsilon = self.agent.epsilon
        
        # Fill buffer and train
        for i in range(50):
            self.agent.memory.push(self.state, 0, 0.0, self.state, False)
        
        with patch.object(self.agent.q_network, 'forward'), \
             patch.object(self.agent.target_network, 'forward'):
            self.agent.train()
        
        # Epsilon should decrease
        self.assertLess(self.agent.epsilon, initial_epsilon)
    
    def test_target_network_update(self):
        """Test target network update"""
        # Set step count to trigger update
        self.agent.step_count = 99
        
        # Fill buffer and train
        for i in range(50):
            self.agent.memory.push(self.state, 0, 0.0, self.state, False)
        
        with patch.object(self.agent.q_network, 'forward'), \
             patch.object(self.agent.target_network, 'forward'), \
             patch.object(self.agent.target_network, 'load_state_dict') as mock_load:
            
            self.agent.train()
            
            # Target network should be updated
            mock_load.assert_called()
    
    def test_save_load_model(self):
        """Test model saving and loading"""
        filepath = 'test_model.pth'
        
        # Save model
        with patch('torch.save') as mock_save:
            self.agent.save_model(filepath)
            mock_save.assert_called_once()
        
        # Load model
        mock_checkpoint = {
            'q_network': {},
            'target_network': {},
            'optimizer': {},
            'epsilon': 0.5,
            'step_count': 100
        }
        
        with patch('torch.load', return_value=mock_checkpoint), \
             patch.object(self.agent.q_network, 'load_state_dict'), \
             patch.object(self.agent.target_network, 'load_state_dict'), \
             patch.object(self.agent.optimizer, 'load_state_dict'):
            
            self.agent.load_model(filepath)
            
            self.assertEqual(self.agent.epsilon, 0.5)
            self.assertEqual(self.agent.step_count, 100)

class TestActions(unittest.TestCase):
    
    def test_actions_mapping(self):
        """Test action mapping constants"""
        self.assertEqual(ACTIONS[0], "ALLOW")
        self.assertEqual(ACTIONS[1], "MONITOR")
        self.assertEqual(ACTIONS[2], "ISOLATE")
        self.assertEqual(len(ACTIONS), 3)

if __name__ == '__main__':
    unittest.main()