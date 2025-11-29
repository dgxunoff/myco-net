"""
Neural Network Models for MycoShield
"""

import torch
import torch.nn as nn
import torch.nn.functional as F

try:
    from torch_geometric.nn import GCNConv
    TORCH_GEOMETRIC_AVAILABLE = True
except ImportError:
    TORCH_GEOMETRIC_AVAILABLE = False
    # Fallback implementation
    class GCNConv(nn.Module):
        def __init__(self, in_channels, out_channels):
            super().__init__()
            self.linear = nn.Linear(in_channels, out_channels)
        
        def forward(self, x, edge_index):
            return F.relu(self.linear(x))

class MyceliumGNN(nn.Module):
    """Graph Neural Network for mycelium-inspired threat detection"""
    
    def __init__(self, input_dim=6, hidden_dim=64, output_dim=1):
        super().__init__()
        self.conv1 = GCNConv(input_dim, hidden_dim)
        self.conv2 = GCNConv(hidden_dim, hidden_dim)
        self.conv3 = GCNConv(hidden_dim, output_dim)
        self.dropout = nn.Dropout(0.2)
        
    def forward(self, x, edge_index, batch=None):
        x = F.relu(self.conv1(x, edge_index))
        x = self.dropout(x)
        x = F.relu(self.conv2(x, edge_index))
        x = self.dropout(x)
        x = torch.sigmoid(self.conv3(x, edge_index))
        return x

class MyceliumDQN(nn.Module):
    """Deep Q-Network for RL-based threat response"""
    
    def __init__(self, input_dim=10, hidden_dim=64, num_actions=3):
        super().__init__()
        self.gnn_layers = nn.ModuleList([
            GCNConv(input_dim, hidden_dim),
            GCNConv(hidden_dim, hidden_dim),
            GCNConv(hidden_dim, hidden_dim)
        ])
        
        self.q_heads = nn.ModuleList([
            nn.Linear(hidden_dim, 1) for _ in range(num_actions)
        ])
        
        self.dropout = nn.Dropout(0.2)
        
    def forward(self, x, edge_index, node_mask=None):
        h = x
        for layer in self.gnn_layers:
            h = F.relu(layer(h, edge_index))
            h = self.dropout(h)
        
        if node_mask is not None:
            h = h[node_mask]
            
        q_values = []
        for head in self.q_heads:
            q_values.append(head(h))
            
        return torch.cat(q_values, dim=1)