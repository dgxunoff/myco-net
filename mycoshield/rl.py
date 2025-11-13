"""
Reinforcement Learning components for MycoShield
"""

import torch
import torch.nn.functional as F
import numpy as np
import random
from collections import deque, namedtuple
from .models import MyceliumDQN

ACTIONS = {
    0: "ALLOW",
    1: "MONITOR", 
    2: "ISOLATE"
}

Experience = namedtuple('Experience', ['state', 'action', 'reward', 'next_state', 'done'])

class ReplayBuffer:
    """Experience replay buffer"""
    
    def __init__(self, capacity=10000):
        self.buffer = deque(maxlen=capacity)
        
    def push(self, state, action, reward, next_state, done):
        self.buffer.append(Experience(state, action, reward, next_state, done))
        
    def sample(self, batch_size):
        return random.sample(self.buffer, batch_size)
    
    def __len__(self):
        return len(self.buffer)

class MyceliumRLAgent:
    """RL Agent for adaptive threat response"""
    
    def __init__(self, input_dim=10, hidden_dim=64, lr=0.001):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        self.q_network = MyceliumDQN(input_dim, hidden_dim).to(self.device)
        self.target_network = MyceliumDQN(input_dim, hidden_dim).to(self.device)
        self.target_network.load_state_dict(self.q_network.state_dict())
        
        self.optimizer = torch.optim.Adam(self.q_network.parameters(), lr=lr)
        self.memory = ReplayBuffer()
        
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.gamma = 0.95
        self.batch_size = 32
        self.target_update = 100
        self.step_count = 0
        
        self.episode_rewards = []
        
    def select_action(self, state, suspicious_nodes=None):
        if suspicious_nodes is None:
            suspicious_nodes = list(range(state.x.shape[0]))
            
        if random.random() < self.epsilon:
            actions = {}
            for node_idx in suspicious_nodes:
                actions[node_idx] = random.randint(0, 2)
            return actions
        
        with torch.no_grad():
            state_tensor = state.to(self.device)
            q_values = self.q_network(state_tensor.x, state_tensor.edge_index)
            
            actions = {}
            for node_idx in suspicious_nodes:
                if node_idx < q_values.shape[0]:
                    action = q_values[node_idx].argmax().item()
                    actions[node_idx] = action
                    
        return actions
    
    def store_experience(self, state, actions, rewards, next_state, done=False):
        for node_idx, action in actions.items():
            reward = rewards.get(node_idx, 0)
            self.memory.push(state, action, reward, next_state, done)
            
    def train(self):
        if len(self.memory) < self.batch_size:
            return
            
        experiences = self.memory.sample(self.batch_size)
        
        states = [e.state for e in experiences]
        actions = torch.tensor([e.action for e in experiences], dtype=torch.long).to(self.device)
        rewards = torch.tensor([e.reward for e in experiences], dtype=torch.float).to(self.device)
        next_states = [e.next_state for e in experiences]
        dones = torch.tensor([e.done for e in experiences], dtype=torch.bool).to(self.device)
        
        current_q_values = []
        for i, state in enumerate(states):
            state_tensor = state.to(self.device)
            q_vals = self.q_network(state_tensor.x, state_tensor.edge_index)
            if q_vals.shape[0] > 0:
                node_q = q_vals[0, actions[i]]
                current_q_values.append(node_q)
            else:
                current_q_values.append(torch.tensor(0.0).to(self.device))
                
        current_q_values = torch.stack(current_q_values)
        
        next_q_values = []
        with torch.no_grad():
            for i, next_state in enumerate(next_states):
                if dones[i]:
                    next_q_values.append(torch.tensor(0.0).to(self.device))
                else:
                    next_state_tensor = next_state.to(self.device)
                    next_q_vals = self.target_network(next_state_tensor.x, next_state_tensor.edge_index)
                    if next_q_vals.shape[0] > 0:
                        max_next_q = next_q_vals[0].max()
                        next_q_values.append(max_next_q)
                    else:
                        next_q_values.append(torch.tensor(0.0).to(self.device))
                        
        next_q_values = torch.stack(next_q_values)
        target_q_values = rewards + (self.gamma * next_q_values)
        
        loss = F.mse_loss(current_q_values, target_q_values)
        
        self.optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(self.q_network.parameters(), 1.0)
        self.optimizer.step()
        
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
            
        self.step_count += 1
        if self.step_count % self.target_update == 0:
            self.target_network.load_state_dict(self.q_network.state_dict())
            
    def save_model(self, filepath):
        torch.save({
            'q_network': self.q_network.state_dict(),
            'target_network': self.target_network.state_dict(),
            'optimizer': self.optimizer.state_dict(),
            'epsilon': self.epsilon,
            'step_count': self.step_count
        }, filepath)
        
    def load_model(self, filepath):
        checkpoint = torch.load(filepath, map_location=self.device)
        self.q_network.load_state_dict(checkpoint['q_network'])
        self.target_network.load_state_dict(checkpoint['target_network'])
        self.optimizer.load_state_dict(checkpoint['optimizer'])
        self.epsilon = checkpoint['epsilon']
        self.step_count = checkpoint['step_count']