#!/usr/bin/env python3
"""
MycoShield Training with NSL-KDD Dataset
Real network intrusion detection training
"""

import kagglehub
import pandas as pd
import numpy as np
import torch
import torch.nn.functional as F
from torch_geometric.data import Data, DataLoader
from torch_geometric.nn import GCNConv
import networkx as nx
from sklearn.preprocessing import StandardScaler, LabelEncoder
import os


# ===================== Model Definition =====================
class MyceliumGNN(torch.nn.Module):
    def __init__(self, input_dim=41, hidden_dim=64, output_dim=1):
        super().__init__()
        self.conv1 = GCNConv(input_dim, hidden_dim)
        self.conv2 = GCNConv(hidden_dim, hidden_dim)
        self.conv3 = GCNConv(hidden_dim, output_dim)
        self.dropout = torch.nn.Dropout(0.2)

    def forward(self, x, edge_index, batch=None):
        x = F.relu(self.conv1(x, edge_index))
        x = self.dropout(x)
        x = F.relu(self.conv2(x, edge_index))
        x = self.dropout(x)
        x = torch.sigmoid(self.conv3(x, edge_index))
        return x


# ===================== Trainer Class =====================
class NSLKDDTrainer:
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoders = {}

    def download_dataset(self):
        """Download NSL-KDD dataset"""
        print("🍄 Downloading NSL-KDD dataset...")
        path = kagglehub.dataset_download("hassan06/nslkdd")
        print(f"Dataset path: {path}")
        return path

    def load_nslkdd(self, path):
        """Load and preprocess NSL-KDD data"""
        columns = [
            'duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes',
            'land', 'wrong_fragment', 'urgent', 'hot', 'num_failed_logins', 'logged_in',
            'num_compromised', 'root_shell', 'su_attempted', 'num_root', 'num_file_creations',
            'num_shells', 'num_access_files', 'num_outbound_cmds', 'is_host_login',
            'is_guest_login', 'count', 'srv_count', 'serror_rate', 'srv_serror_rate',
            'rerror_rate', 'srv_rerror_rate', 'same_srv_rate', 'diff_srv_rate',
            'srv_diff_host_rate', 'dst_host_count', 'dst_host_srv_count',
            'dst_host_same_srv_rate', 'dst_host_diff_srv_rate', 'dst_host_same_src_port_rate',
            'dst_host_srv_diff_host_rate', 'dst_host_serror_rate', 'dst_host_srv_serror_rate',
            'dst_host_rerror_rate', 'dst_host_srv_rerror_rate', 'attack_type', 'difficulty'
        ]

        train_file = os.path.join(path, 'KDDTrain+.txt')
        test_file = os.path.join(path, 'KDDTest+.txt')

        train_data = pd.read_csv(train_file, names=columns)
        test_data = pd.read_csv(test_file, names=columns)

        print(f"✅ Loaded {len(train_data)} training samples, {len(test_data)} test samples")
        return train_data, test_data

    def preprocess_data(self, train_data, test_data):
        """Preprocess NSL-KDD data for GNN"""
        all_data = pd.concat([train_data, test_data], ignore_index=True)

        categorical_cols = ['protocol_type', 'service', 'flag']
        for col in categorical_cols:
            le = LabelEncoder()
            all_data[col] = le.fit_transform(all_data[col])
            self.label_encoders[col] = le

        all_data['is_attack'] = (all_data['attack_type'] != 'normal').astype(int)

        # Select only numeric features (exclude attack_type and difficulty)
        feature_cols = [
            'duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes',
            'land', 'wrong_fragment', 'urgent', 'hot', 'num_failed_logins', 'logged_in',
            'num_compromised', 'root_shell', 'su_attempted', 'num_root', 'num_file_creations',
            'num_shells', 'num_access_files', 'num_outbound_cmds', 'is_host_login',
            'is_guest_login', 'count', 'srv_count', 'serror_rate', 'srv_serror_rate',
            'rerror_rate', 'srv_rerror_rate', 'same_srv_rate', 'diff_srv_rate',
            'srv_diff_host_rate', 'dst_host_count', 'dst_host_srv_count',
            'dst_host_same_srv_rate', 'dst_host_diff_srv_rate', 'dst_host_same_src_port_rate',
            'dst_host_srv_diff_host_rate', 'dst_host_serror_rate', 'dst_host_srv_serror_rate',
            'dst_host_rerror_rate', 'dst_host_srv_rerror_rate'
        ]
        
        X = all_data[feature_cols].values
        y = all_data['is_attack'].values

        X = self.scaler.fit_transform(X)

        train_size = len(train_data)
        X_train, y_train = X[:train_size], y[:train_size]
        X_test, y_test = X[train_size:], y[train_size:]
        return X_train, y_train, X_test, y_test

    def create_graph_from_flows(self, X, y, batch_size=1000):
        """Convert network flows to graph structure"""
        graphs = []

        for i in range(0, len(X), batch_size):
            batch_X = X[i:i + batch_size]
            batch_y = y[i:i + batch_size]

            n_nodes = min(len(batch_X), 50)
            G = nx.Graph()
            node_features = []

            for j in range(n_nodes):
                G.add_node(j)
                node_features.append(batch_X[j])

                for k in range(j + 1, min(j + 5, n_nodes)):
                    similarity = np.exp(-np.linalg.norm(batch_X[j] - batch_X[k]))
                    if similarity > 0.5:
                        G.add_edge(j, k)

            if len(G.edges()) > 0:
                edge_index = torch.tensor(list(G.edges()), dtype=torch.long).t().contiguous()
            else:
                edge_index = torch.tensor([[0, 1], [1, 0]], dtype=torch.long)

            node_features = torch.tensor(node_features, dtype=torch.float)
            node_labels = torch.tensor(batch_y[:n_nodes], dtype=torch.float)

            graph = Data(x=node_features, edge_index=edge_index, y=node_labels)
            graphs.append(graph)

        return graphs

    def train_model(self, epochs=50):
        """Train MycoShield on NSL-KDD data"""
        dataset_path = self.download_dataset()
        train_data, test_data = self.load_nslkdd(dataset_path)

        X_train, y_train, X_test, y_test = self.preprocess_data(train_data, test_data)

        print("🕸️ Creating graph structures...")
        train_graphs = self.create_graph_from_flows(X_train, y_train)
        test_graphs = self.create_graph_from_flows(X_test, y_test)

        train_loader = DataLoader(train_graphs, batch_size=32, shuffle=True)
        test_loader = DataLoader(test_graphs, batch_size=32, shuffle=False)

        model = MyceliumGNN(input_dim=41, hidden_dim=64, output_dim=1)
        optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

        print("🧠 Training MycoShield on NSL-KDD...")

        best_acc = 0
        for epoch in range(epochs):
            # ---- Training ----
            model.train()
            train_loss = 0

            for batch in train_loader:
                optimizer.zero_grad()
                out = model(batch.x, batch.edge_index, batch.batch)
                loss = F.binary_cross_entropy(out.squeeze(), batch.y)
                loss.backward()
                optimizer.step()
                train_loss += loss.item()

            # ---- Validation ----
            model.eval()
            test_loss = 0
            correct = 0
            total = 0

            with torch.no_grad():
                for batch in test_loader:
                    out = model(batch.x, batch.edge_index, batch.batch)
                    test_loss += F.binary_cross_entropy(out.squeeze(), batch.y).item()

                    predicted = (out.squeeze() > 0.5).float()
                    total += batch.y.size(0)
                    correct += (predicted == batch.y).sum().item()

            accuracy = correct / total

            if accuracy > best_acc:
                best_acc = accuracy
                torch.save(model.state_dict(), 'mycoshield_nslkdd.pth')

            if epoch % 5 == 0:
                print(f"Epoch {epoch:3d} | "
                      f"Train Loss: {train_loss / len(train_loader):.4f} | "
                      f"Test Loss: {test_loss / len(test_loader):.4f} | "
                      f"Acc: {accuracy:.4f}")

        print(f"🏆 Training complete! Best accuracy: {best_acc:.4f}")
        print("✅ Model saved as mycoshield_nslkdd.pth")
        return model


# ===================== Run Script =====================
if __name__ == "__main__":
    trainer = NSLKDDTrainer()
    model = trainer.train_model()
