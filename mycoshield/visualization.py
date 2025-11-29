"""
3D Visualization for MycoShield mycelium networks
"""

import torch
import networkx as nx
import plotly.graph_objects as go

class MyceliumVisualizer:
    """Create 3D mycelium network visualizations"""
    
    def __init__(self):
        self.colors = {
            'normal': '#00ff00',
            'suspicious': '#ffff00', 
            'infected': '#ff0000',
            'isolated': '#000000'
        }
    
    def create_3d_network(self, G, node_list, anomaly_scores, threshold=0.7, isolated_nodes=None):
        if len(G.nodes()) == 0:
            return go.Figure()
            
        pos = nx.spring_layout(G, dim=3, k=3, iterations=50)
        isolated_nodes = isolated_nodes or set()
        
        node_trace = go.Scatter3d(
            x=[], y=[], z=[],
            mode='markers+text',
            marker=dict(size=[], color=[], colorscale='RdYlGn_r', 
                       showscale=True, colorbar=dict(title="Threat Level")),
            text=[], textposition="middle center",
            hovertemplate='<b>%{text}</b><br>Threat: %{marker.color:.2f}<extra></extra>',
            name='Mycelium Nodes'
        )
        
        edge_trace = go.Scatter3d(
            x=[], y=[], z=[],
            mode='lines',
            line=dict(width=2, color='rgba(125,125,125,0.3)'),
            hoverinfo='none',
            name='Hyphae Connections'
        )
        
        for i, node in enumerate(node_list):
            if node in pos:
                x, y, z = pos[node]
                node_trace['x'] += tuple([x])
                node_trace['y'] += tuple([y])
                node_trace['z'] += tuple([z])
                
                score = anomaly_scores.get(node, 0.0)
                if isinstance(score, torch.Tensor):
                    score = score.item()
                    
                node_trace['marker']['color'] += tuple([score])
                
                size = max(10, min(30, G.degree(node) * 3))
                node_trace['marker']['size'] += tuple([size])
                
                if node in isolated_nodes:
                    status = "🔒 ISOLATED"
                elif score > threshold:
                    status = "🍄 INFECTED"
                elif score > 0.5:
                    status = "⚠️ SUSPICIOUS"
                else:
                    status = "✅ HEALTHY"
                
                node_trace['text'] += tuple([f"{node}<br>{status}"])
        
        for edge in G.edges():
            if edge[0] in pos and edge[1] in pos:
                x0, y0, z0 = pos[edge[0]]
                x1, y1, z1 = pos[edge[1]]
                edge_trace['x'] += tuple([x0, x1, None])
                edge_trace['y'] += tuple([y0, y1, None])
                edge_trace['z'] += tuple([z0, z1, None])
        
        fig = go.Figure(data=[edge_trace, node_trace])
        fig.update_layout(
            title="🍄 MycoShield: Mycelium Network Defense System",
            scene=dict(
                xaxis=dict(showbackground=False, showticklabels=False, showgrid=False),
                yaxis=dict(showbackground=False, showticklabels=False, showgrid=False),
                zaxis=dict(showbackground=False, showticklabels=False, showgrid=False),
                bgcolor='black'
            ),
            showlegend=True,
            height=600,
            paper_bgcolor='black',
            font=dict(color='white')
        )
        
        return fig
    
    def create_rl_visualization(self, G, node_list, action_results, isolated_nodes=None, monitored_nodes=None):
        """Create RL-specific visualization"""
        if len(G.nodes()) == 0:
            return go.Figure()
            
        pos = nx.spring_layout(G, dim=3, k=2, iterations=50)
        isolated_nodes = isolated_nodes or set()
        monitored_nodes = monitored_nodes or set()
        
        node_trace = go.Scatter3d(
            x=[], y=[], z=[],
            mode='markers+text',
            marker=dict(size=[], color=[], colorscale='RdYlBu', 
                       showscale=True, colorbar=dict(title="RL Action")),
            text=[], textposition="middle center",
            hovertemplate='<b>%{text}</b><br>Action: %{marker.color}<extra></extra>',
            name='RL Mycelium Nodes'
        )
        
        edge_trace = go.Scatter3d(
            x=[], y=[], z=[],
            mode='lines',
            line=dict(width=2, color='rgba(0,255,0,0.3)'),
            hoverinfo='none',
            name='Hyphae Connections'
        )
        
        for node in node_list:
            if node in pos:
                x, y, z = pos[node]
                node_trace['x'] += tuple([x])
                node_trace['y'] += tuple([y])
                node_trace['z'] += tuple([z])
                
                if node in isolated_nodes:
                    color_val = 2
                    status = "🔒 ISOLATED"
                    size = 25
                elif node in monitored_nodes:
                    color_val = 1
                    status = "👁️ MONITORED"
                    size = 20
                else:
                    color_val = 0
                    status = "✅ ALLOWED"
                    size = 15
                    
                node_trace['marker']['color'] += tuple([color_val])
                node_trace['marker']['size'] += tuple([size])
                
                action_info = ""
                if node in action_results:
                    action_info = f"<br>Action: {action_results[node]['action']}<br>Reward: {action_results[node]['reward']}"
                    
                node_trace['text'] += tuple([f"{node}<br>{status}{action_info}"])
                
        for edge in G.edges():
            if edge[0] in pos and edge[1] in pos:
                x0, y0, z0 = pos[edge[0]]
                x1, y1, z1 = pos[edge[1]]
                edge_trace['x'] += tuple([x0, x1, None])
                edge_trace['y'] += tuple([y0, y1, None])
                edge_trace['z'] += tuple([z0, z1, None])
                
        fig = go.Figure(data=[edge_trace, node_trace])
        fig.update_layout(
            title="🤖 MycoShield: RL-Enhanced Mycelium Defense",
            scene=dict(
                xaxis=dict(showbackground=False, showticklabels=False, showgrid=False),
                yaxis=dict(showbackground=False, showticklabels=False, showgrid=False),
                zaxis=dict(showbackground=False, showticklabels=False, showgrid=False),
                bgcolor='black'
            ),
            showlegend=True,
            height=600,
            paper_bgcolor='black',
            font=dict(color='white')
        )
        
        return fig