"""
Data processing and ingestion for MycoShield
"""

import torch
import numpy as np
import networkx as nx
from torch_geometric.data import Data
from sklearn.preprocessing import StandardScaler
import subprocess
import threading
import queue
import os
import time
from scapy.all import rdpcap, IP, TCP, UDP

class TrafficParser:
    """Parse network traffic from PCAP files"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        
    def parse_pcap(self, pcap_file):
        packets = rdpcap(pcap_file)
        flows = {}
        
        for pkt in packets:
            if IP in pkt:
                src_ip = pkt[IP].src
                dst_ip = pkt[IP].dst
                
                features = {
                    'packet_size': len(pkt),
                    'protocol': pkt[IP].proto,
                    'ttl': pkt[IP].ttl,
                    'flags': 0,
                    'port_src': 0,
                    'port_dst': 0
                }
                
                if TCP in pkt:
                    features['flags'] = pkt[TCP].flags
                    features['port_src'] = pkt[TCP].sport
                    features['port_dst'] = pkt[TCP].dport
                elif UDP in pkt:
                    features['port_src'] = pkt[UDP].sport
                    features['port_dst'] = pkt[UDP].dport
                
                flow_key = f"{src_ip}->{dst_ip}"
                if flow_key not in flows:
                    flows[flow_key] = []
                flows[flow_key].append(features)
        
        return flows
    
    def create_graph(self, flows, feature_dim=6):
        G = nx.DiGraph()
        node_features = {}
        
        for flow_key, packets in flows.items():
            src, dst = flow_key.split('->')
            
            if src not in G:
                G.add_node(src)
                node_features[src] = []
            if dst not in G:
                G.add_node(dst)
                node_features[dst] = []
            
            if G.has_edge(src, dst):
                G[src][dst]['weight'] += len(packets)
            else:
                G.add_edge(src, dst, weight=len(packets))
            
            for pkt in packets:
                base_features = list(pkt.values())
                if feature_dim > len(base_features):
                    extended_features = base_features + [0.0] * (feature_dim - len(base_features))
                else:
                    extended_features = base_features[:feature_dim]
                    
                node_features[src].append(extended_features)
                node_features[dst].append(extended_features)
        
        node_list = list(G.nodes())
        node_mapping = {node: i for i, node in enumerate(node_list)}
        
        X = []
        for node in node_list:
            if node_features[node]:
                feat = np.mean(node_features[node], axis=0)
            else:
                feat = np.zeros(feature_dim)
            X.append(feat)
        
        X = torch.tensor(X, dtype=torch.float)
        X = torch.tensor(self.scaler.fit_transform(X), dtype=torch.float)
        
        edge_index = []
        edge_weights = []
        for src, dst in G.edges():
            edge_index.append([node_mapping[src], node_mapping[dst]])
            edge_weights.append(G[src][dst]['weight'])
        
        edge_index = torch.tensor(edge_index, dtype=torch.long).t().contiguous()
        edge_weights = torch.tensor(edge_weights, dtype=torch.float)
        
        return Data(x=X, edge_index=edge_index, edge_attr=edge_weights), node_list, G

class ZeekLogTailer:
    """Real-time Zeek log monitoring"""
    
    def __init__(self, log_file="mycoshield.log"):
        self.log_file = log_file
        self.data_queue = queue.Queue()
        self.running = False
        self.thread = None
        
    def start_tailing(self):
        self.running = True
        self.thread = threading.Thread(target=self._tail_log)
        self.thread.daemon = True
        self.thread.start()
        
    def stop_tailing(self):
        self.running = False
        
    def _tail_log(self):
        try:
            if not os.path.exists(self.log_file):
                return
                
            process = subprocess.Popen(['tail', '-F', self.log_file], 
                                     stdout=subprocess.PIPE, 
                                     stderr=subprocess.PIPE,
                                     universal_newlines=True)
            
            while self.running:
                line = process.stdout.readline()
                if line:
                    self.data_queue.put(line.strip())
                time.sleep(0.1)
                
        except Exception:
            pass
            
    def get_new_data(self):
        new_lines = []
        while not self.data_queue.empty():
            try:
                new_lines.append(self.data_queue.get_nowait())
            except queue.Empty:
                break
        return new_lines
    
    def parse_zeek_line(self, line):
        if line.startswith('#') or not line.strip():
            return None
            
        try:
            fields = line.split('\t')
            if len(fields) < 10:
                return None
                
            return {
                'ts': float(fields[0]),
                'uid': fields[1],
                'orig_h': fields[2],
                'orig_p': int(fields[3]),
                'resp_h': fields[4],
                'resp_p': int(fields[5]),
                'proto': fields[6],
                'duration': float(fields[7]) if fields[7] != '-' else 0.0,
                'orig_bytes': int(fields[8]) if fields[8] != '-' else 0,
                'resp_bytes': int(fields[9]) if fields[9] != '-' else 0,
                'threat_score': float(fields[-1]) if len(fields) > 10 and fields[-1] != '-' else 0.0
            }
        except:
            return None