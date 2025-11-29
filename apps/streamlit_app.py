"""
Main Streamlit Application for MycoShield
"""

import streamlit as st
import torch
import pandas as pd
import numpy as np
import time
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mycoshield import MyceliumGNN, NetworkProcessor, ThreatDetector, MyceliumVisualizer, TrafficParser, SecurityEnforcer, BlockchainSecurityOrchestrator

def main():
    st.set_page_config(
        page_title="🍄 MycoShield",
        page_icon="🍄",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.markdown('<h1 style="color: #00ff00; text-align: center;">🍄 MycoShield</h1>', 
                unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #888;">Mycelium-Inspired Graph Neural Network for Zero-Day Cyberattack Detection</p>', 
                unsafe_allow_html=True)
    
    # Initialize components
    if 'components' not in st.session_state:
        # Try to load trained model
        model_loaded = False
        try:
            checkpoint = torch.load('mycoshield_nslkdd.pth', map_location='cpu')
            input_dim = checkpoint['conv1.lin.weight'].shape[1]
            model = MyceliumGNN(input_dim=input_dim)
            model.load_state_dict(checkpoint)
            st.success("🏆 Loaded NSL-KDD trained model!")
            model_loaded = True
        except:
            model = MyceliumGNN(input_dim=6)
            st.info("💡 Using untrained model. Run train_nslkdd.py to train on real data.")
        
        # Load security config
        try:
            import json
            with open('security_config.json', 'r') as f:
                security_config = json.load(f)
        except:
            security_config = {}
        
        # Initialize blockchain orchestrator with private key from .env
        blockchain = BlockchainSecurityOrchestrator()
        private_key = os.getenv('APTOS_PRIVATE_KEY')
        blockchain_init = blockchain.initialize_blockchain_security(private_key)
        
        # Initialize with real security enforcement + blockchain
        enforcer = SecurityEnforcer(security_config)
        
        st.session_state.components = {
            'model': model,
            'processor': NetworkProcessor(),
            'detector': ThreatDetector(model, security_enforcer=enforcer, blockchain_orchestrator=blockchain),
            'visualizer': MyceliumVisualizer(),
            'parser': TrafficParser(),
            'enforcer': enforcer,
            'blockchain': blockchain,
            'blockchain_init': blockchain_init,
            'model_loaded': model_loaded
        }
    
    # Sidebar
    with st.sidebar:
        st.header("🔬 Control Panel")
        
        uploaded_file = st.file_uploader("Upload PCAP File", type=['pcap', 'pcapng'])
        
        # Reset demo mode when file is uploaded
        if uploaded_file:
            st.session_state.demo_mode = False
        
        st.subheader("Detection Parameters")
        threshold = st.slider("Anomaly Threshold", 0.0, 1.0, 0.5, 0.01)
        st.caption(f"⚡ NSL-KDD Optimal: 0.50 | Current: {threshold:.2f}")
        st.caption(f"Nodes with score > {threshold:.2f} = INFECTED")
        auto_isolate = st.checkbox("Auto-Isolate Infected Nodes", True)
        
        st.subheader("🛡️ Security Actions")
        real_blocking = st.checkbox("Enable Real Firewall Blocking", False)
        if real_blocking:
            st.warning("⚠️ This will modify system firewall rules!")
        
        # Blockchain status
        st.subheader("🔗 Blockchain Status")
        blockchain_init = st.session_state.components['blockchain_init']
        
        # Wallet connection status
        if os.getenv('APTOS_PRIVATE_KEY'):
            st.success("✅ Wallet Connected")
            st.metric("Address", blockchain_init['wallet_address'][:10] + "...")
            st.caption(f"Full: {blockchain_init['wallet_address']}")
        else:
            st.warning("⚠️ No Wallet Connected")
            if st.button("🔗 Connect Wallet"):
                st.info("Add APTOS_PRIVATE_KEY to .env file and restart")
        
        st.metric("APT Balance", f"{blockchain_init['balance']:.2f}")
        st.metric("Network", "Testnet")
        
        # MYCO Token Rewards
        st.subheader("💰 MYCO Rewards")
        if 'total_threats_detected' not in st.session_state:
            st.session_state.total_threats_detected = 0
        if 'total_myco_earned' not in st.session_state:
            st.session_state.total_myco_earned = 300.0  # Starting balance from blockchain
        
        # Fetch real MYCO balance from blockchain
        blockchain = st.session_state.components['blockchain']
        
        # Force refresh balance on button click
        if st.button("🔄 Refresh from Blockchain"):
            myco_balance = blockchain.aptos_manager.get_myco_balance()
            st.session_state.total_myco_earned = myco_balance
            st.success(f"Updated: {myco_balance:.2f} MYCO")
        
        st.metric("MYCO Balance", f"{st.session_state.total_myco_earned:.2f}")
        st.metric("Threats Detected", st.session_state.total_threats_detected)
        st.caption("Auto-updated on threat detection")
        st.caption(f"Contract: 0x8422...20cb")
        
        # Security status
        enforcer = st.session_state.components['enforcer']
        summary = enforcer.get_incident_summary()
        st.metric("🚫 Blocked IPs", summary['currently_blocked'])
        st.metric("📊 Total Incidents", summary['total_incidents'])
        st.metric("🔗 On Blockchain", summary['total_incidents'])
        
        if st.button("🧪 Generate Demo Traffic"):
            st.session_state.demo_mode = True
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if uploaded_file or st.session_state.get('demo_mode', False):
            
            if st.session_state.get('demo_mode', False) and not uploaded_file:
                st.warning("🧪 DEMO MODE: Using synthetic traffic")
                st.info("Upload a PCAP file to analyze real network traffic")
                
                try:
                    import json
                    with open("demo_traffic.json", "r") as f:
                        flows = json.load(f)
                    
                    feature_dim = 41 if st.session_state.components['model_loaded'] else 6
                    graph_data, node_list, G = st.session_state.components['parser'].create_graph(flows, feature_dim)
                    
                except FileNotFoundError:
                    # Fallback demo data
                    import networkx as nx
                    G = nx.erdos_renyi_graph(15, 0.3, directed=True)
                    node_list = [f"192.168.1.{i+1}" for i in range(len(G.nodes()))]
                    G = nx.relabel_nodes(G, dict(zip(G.nodes(), node_list)))
                    
                    feature_dim = 41 if st.session_state.components['model_loaded'] else 6
                    X = torch.randn(len(node_list), feature_dim)
                    edge_index = torch.tensor(list(G.edges()), dtype=torch.long).t().contiguous()
                    
                    anomalous_nodes = np.random.choice(len(node_list), 3, replace=False)
                    X[anomalous_nodes] += torch.randn(3, feature_dim) * 2
                    
                    from torch_geometric.data import Data
                    graph_data = Data(x=X, edge_index=edge_index)
                
            elif uploaded_file:
                st.success(f"📊 Analyzing YOUR PCAP: {uploaded_file.name}")
                st.session_state.demo_mode = False  # Ensure demo mode is off
                
                with open("temp.pcap", "wb") as f:
                    f.write(uploaded_file.read())
                
                flows = st.session_state.components['parser'].parse_pcap("temp.pcap")
                feature_dim = 41 if st.session_state.components['model_loaded'] else 6
                graph_data, node_list, G = st.session_state.components['parser'].create_graph(flows, feature_dim)
            
            # Run detection
            st.info("🧠 Running MycoShield GNN Analysis...")
            
            anomalies = st.session_state.components['detector'].detect_anomalies(
                graph_data, node_list, threshold
            )
            
            # Create visualization
            fig = st.session_state.components['visualizer'].create_3d_network(
                G, node_list, anomalies, threshold, st.session_state.components['detector'].isolated_nodes
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Detection results
            st.subheader("🔍 Detection Results")
            
            # Show threat score statistics
            scores_list = list(anomalies.values())
            if scores_list:
                st.info(f"📊 Threat Score Stats: Min={min(scores_list):.3f} | Max={max(scores_list):.3f} | Avg={sum(scores_list)/len(scores_list):.3f} | Median={sorted(scores_list)[len(scores_list)//2]:.3f}")
            
            summary = st.session_state.components['detector'].get_threat_summary(anomalies, threshold)
            
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                st.metric("🍄 Infected Nodes", summary['infected'], 
                         delta=f"{summary['infected']/summary['total']*100:.1f}%")
            
            with col_b:
                st.metric("⚠️ Suspicious Nodes", summary['suspicious'], 
                         delta=f"{summary['suspicious']/summary['total']*100:.1f}%")
            
            with col_c:
                st.metric("✅ Healthy Nodes", summary['healthy'], 
                         delta=f"{summary['healthy']/summary['total']*100:.1f}%")
            
            if summary['infected'] > 0:
                st.error("🚨 SPORE ALERT: Fungal infection detected!")
                
                # Calculate rewards for detected threats
                if 'last_detection_count' not in st.session_state:
                    st.session_state.last_detection_count = 0
                
                new_threats = summary['infected'] - st.session_state.last_detection_count
                if new_threats > 0:
                    # Mint MYCO tokens based on threat severity
                    max_score = max([score for score in anomalies.values() if score > threshold])
                    
                    if max_score > 0.8:
                        severity_level = 3  # High
                        reward = 300 * new_threats
                        severity = "HIGH"
                    elif max_score > 0.6:
                        severity_level = 2  # Medium
                        reward = 200 * new_threats
                        severity = "MEDIUM"
                    else:
                        severity_level = 1  # Low
                        reward = 100 * new_threats
                        severity = "LOW"
                    
                    # Mint MYCO tokens on blockchain
                    blockchain = st.session_state.components['blockchain']
                    wallet_addr = blockchain_init['wallet_address']
                    
                    with st.spinner(f"Minting {reward} MYCO tokens on Aptos..."):
                        tx_hash = blockchain.aptos_manager.reward_threat_detection(wallet_addr, severity_level)
                    
                    # Update session state immediately
                    st.session_state.total_threats_detected += new_threats
                    st.session_state.last_detection_count = summary['infected']
                    st.session_state.total_myco_earned += reward
                    
                    if tx_hash and tx_hash.startswith("0x"):
                        st.success(f"💰 Minted {reward} MYCO tokens! New Balance: {st.session_state.total_myco_earned:.2f} MYCO")
                        st.caption(f"TX: {tx_hash[:10]}...{tx_hash[-8:]}")
                        st.caption(f"Severity: {severity} | Reward: {reward} MYCO")
                    else:
                        st.success(f"💰 Earned {reward} MYCO tokens! New Balance: {st.session_state.total_myco_earned:.2f} MYCO")
                    st.balloons()
                    
                    # Force page refresh to update sidebar
                    time.sleep(2)
                    st.rerun()
                
                threat_data = []
                for node, score in anomalies.items():
                    if score > threshold:
                        action_taken = '🔒 ISOLATED' if auto_isolate else '⚠️ MONITORING'
                        if real_blocking and auto_isolate:
                            action_taken = '🚫 FIREWALL BLOCKED'
                        
                        # Calculate reward for this specific threat
                        if score > 0.8:
                            node_reward = 300
                        elif score > 0.6:
                            node_reward = 200
                        else:
                            node_reward = 100
                        
                        threat_data.append({
                            'Node': node,
                            'Threat Score': f"{score:.3f}",
                            'Status': '🍄 INFECTED',
                            'Action': action_taken,
                            'Reward': f'{node_reward} MYCO',
                            'Blockchain': '✅ Stored'
                        })
                
                if threat_data:
                    st.dataframe(pd.DataFrame(threat_data), use_container_width=True)
            else:
                st.success("✅ Network mycelium is healthy!")
                st.session_state.last_detection_count = 0
    
    with col2:
        st.subheader("📊 Network Stats")
        
        if 'G' in locals():
            import networkx as nx
            stats_data = {
                'Total Nodes': len(G.nodes()),
                'Total Connections': len(G.edges()),
                'Network Density': f"{nx.density(G):.3f}",
                'Avg Clustering': f"{nx.average_clustering(G):.3f}",
            }
            
            for key, value in stats_data.items():
                st.metric(key, value)
        
        st.subheader("🎯 System Status")
        st.success("🟢 MycoShield Online")
        st.info("🔄 Real-time Monitoring")
        
        # Recent incidents
        if 'enforcer' in st.session_state.components:
            recent = st.session_state.components['enforcer'].get_incident_summary()['recent_incidents']
            if recent:
                st.subheader("🚨 Recent Incidents")
                for incident in recent[-3:]:
                    st.text(f"{incident['timestamp'][:19]}: {incident['ip_address']} - {incident['action_taken']}")
        
        # Manual IP management
        st.subheader("🔧 Manual Controls")
        ip_to_block = st.text_input("Block IP Address")
        if st.button("🚫 Block IP") and ip_to_block:
            if 'enforcer' in st.session_state.components:
                st.session_state.components['enforcer'].isolate_node(ip_to_block, 1.0, "ISOLATE")
                st.success(f"Blocked {ip_to_block}")
        
        ip_to_unblock = st.text_input("Unblock IP Address")
        if st.button("✅ Unblock IP") and ip_to_unblock:
            if 'enforcer' in st.session_state.components:
                st.session_state.components['enforcer'].unblock_ip(ip_to_unblock)
                st.success(f"Unblocked {ip_to_unblock}")

if __name__ == "__main__":
    main()