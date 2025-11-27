"""
Core processing logic for MycoShield
"""

import torch
import numpy as np
import networkx as nx
from sklearn.preprocessing import StandardScaler
from torch_geometric.data import Data

class NetworkProcessor:
    """Process network data into graph structures"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.G = nx.Graph()
        self.node_features = {}
        
    def update_graph(self, conn_data):
        src = conn_data['orig_h']
        dst = conn_data['resp_h']
        
        if src not in self.G:
            self.G.add_node(src)
            self.node_features[src] = []
            
        if dst not in self.G:
            self.G.add_node(dst)
            self.node_features[dst] = []
            
        if not self.G.has_edge(src, dst):
            self.G.add_edge(src, dst, weight=1)
        else:
            self.G[src][dst]['weight'] += 1
            
        features = [
            conn_data.get('duration', 0),
            conn_data.get('orig_bytes', 0),
            conn_data.get('resp_bytes', 0),
            conn_data.get('orig_p', 0),
            conn_data.get('resp_p', 0),
            1 if conn_data.get('proto') == 'tcp' else 0,
            1 if conn_data.get('proto') == 'udp' else 0,
            1 if conn_data.get('proto') == 'icmp' else 0,
            conn_data.get('threat_score', 0),
            len(list(self.G.neighbors(src)))
        ]
        
        self.node_features[src].append(features)
        self.node_features[dst].append(features)
        
        if len(self.node_features[src]) > 10:
            self.node_features[src] = self.node_features[src][-10:]
        if len(self.node_features[dst]) > 10:
            self.node_features[dst] = self.node_features[dst][-10:]
    
    def get_graph_data(self):
        if len(self.G.nodes()) < 2:
            return None, None
            
        node_list = list(self.G.nodes())
        X = []
        
        for node in node_list:
            if self.node_features[node]:
                feat = np.mean(self.node_features[node], axis=0)
            else:
                feat = np.zeros(10)
            X.append(feat)
            
        X = np.array(X)
        if X.shape[0] > 1:
            X = self.scaler.fit_transform(X)
        
        edge_list = []
        for edge in self.G.edges():
            src_idx = node_list.index(edge[0])
            dst_idx = node_list.index(edge[1])
            edge_list.append([src_idx, dst_idx])
            
        if not edge_list:
            edge_list = [[0, 1]] if len(node_list) > 1 else [[0, 0]]
            
        X_tensor = torch.tensor(X, dtype=torch.float)
        edge_index = torch.tensor(edge_list, dtype=torch.long).t().contiguous()
        
        return Data(x=X_tensor, edge_index=edge_index), node_list

class ThreatDetector:
    """Detect threats using trained models with blockchain integration"""
    
    def __init__(self, model, security_enforcer=None, blockchain_orchestrator=None):
        self.model = model
        self.isolated_nodes = set()
        self.security_enforcer = security_enforcer
        self.blockchain_orchestrator = blockchain_orchestrator
        
    def detect_anomalies(self, graph_data, node_list, threshold=0.7):
        if graph_data is None:
            return {}
            
        with torch.no_grad():
            scores = self.model(graph_data.x, graph_data.edge_index)
            
        anomalies = {}
        for i, node in enumerate(node_list):
            score = scores[i].item()
            anomalies[node] = score
            
            if score > threshold:
                self.isolated_nodes.add(node)
                
                # Check blockchain threat intelligence
                blockchain_validated = False
                if self.blockchain_orchestrator:
                    try:
                        blockchain_threat = self.blockchain_orchestrator.threat_intel.query_threat_intelligence(node)
                        blockchain_validated = blockchain_threat is not None
                        
                        # Submit new threat to blockchain
                        if not blockchain_threat:
                            self.blockchain_orchestrator.threat_intel.store_threat_signature(
                                node, f"gnn_detection_{score:.3f}", "anomaly"
                            )
                    except Exception as e:
                        print(f"Blockchain validation error: {e}")
                
                # Execute real security actions
                if self.security_enforcer:
                    action_type = "ISOLATE" if blockchain_validated or score > 0.8 else "MONITOR"
                    self.security_enforcer.isolate_node(node, score, action_type)
            elif score > 0.5:  # Suspicious but not critical
                if self.security_enforcer:
                    self.security_enforcer.isolate_node(node, score, "MONITOR")
                
        return anomalies
    
    def get_threat_summary(self, anomalies, threshold=0.7):
        infected = sum(1 for score in anomalies.values() if score > threshold)
        suspicious = sum(1 for score in anomalies.values() if 0.5 < score <= threshold)
        healthy = len(anomalies) - infected - suspicious
        
        return {
            'infected': infected,
            'suspicious': suspicious,
            'healthy': healthy,
            'total': len(anomalies)
        }