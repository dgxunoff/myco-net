"""
Level 5: Blockchain-Enhanced MycoShield Application
"""

import streamlit as st
import asyncio
import pandas as pd
import time
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mycoshield import (
    BlockchainSecurityOrchestrator, AptosSecurityManager, 
    MyceliumVisualizer, TrafficParser
)

def main():
    st.set_page_config(
        page_title="🔗 MycoShield Blockchain",
        page_icon="🔗",
        layout="wide"
    )
    
    st.markdown('<h1 style="color: #00ff00;">🔗 MycoShield Blockchain Security</h1>', 
                unsafe_allow_html=True)
    st.markdown('<p style="color: #888;">Decentralized Mycelium Network Defense with Aptos Blockchain</p>', 
                unsafe_allow_html=True)
    
    # Initialize blockchain orchestrator
    if 'blockchain_orchestrator' not in st.session_state:
        st.session_state.blockchain_orchestrator = BlockchainSecurityOrchestrator()
        st.session_state.blockchain_init = st.session_state.blockchain_orchestrator.initialize_blockchain_security()
    
    orchestrator = st.session_state.blockchain_orchestrator
    
    # Sidebar - Blockchain Controls
    with st.sidebar:
        st.header("🔗 Blockchain Controls")
        
        # Blockchain Status
        st.subheader("📊 Blockchain Status")
        init_data = st.session_state.blockchain_init
        st.metric("Wallet Address", init_data['wallet_address'][:10] + "...")
        st.metric("Balance", f"{init_data['balance']} APT")
        st.metric("Network", "Testnet")
        
        # Threat Intelligence
        st.subheader("🧠 Threat Intelligence")
        threat_ip = st.text_input("Threat IP", "192.168.1.100")
        threat_type = st.selectbox("Threat Type", ["malware", "port_scan", "ddos", "phishing"])
        threat_score = st.slider("Threat Score", 0.0, 1.0, 0.8, 0.1)
        
        if st.button("📤 Submit to Blockchain"):
            tx_hash = orchestrator.threat_intel.store_threat_signature(
                threat_ip, f"sig_{threat_type}", threat_type
            )
            st.success(f"Submitted: {tx_hash}")
        
        # Validator Network
        st.subheader("🔍 Validator Network")
        validators = ["0x123", "0x456", "0x789"]
        validator_results = orchestrator.scoring_system.implement_validator_network(validators)
        
        for validator in validator_results:
            status = "🟢" if validator['active'] else "🔴"
            st.text(f"{status} {validator['address'][:8]}... Rep: {validator['reputation']}")
    
    # Main Content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🔗 Blockchain Security Dashboard")
        
        # Real-time Blockchain Monitoring
        if st.button("🔄 Start Blockchain Monitoring"):
            placeholder = st.empty()
            
            for i in range(10):
                with placeholder.container():
                    # Simulate blockchain events
                    event_data = {
                        "ip": f"192.168.1.{i+100}",
                        "ip_address": f"192.168.1.{i+100}",
                        "signature": f"hash_{i}",
                        "type": ["malware", "port_scan", "ddos"][i % 3],
                        "evidence": f"Threat detected #{i+1}",
                        "action_taken": "ISOLATED",
                        "threat_score": 0.7 + (i * 0.05),
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                    }
                    
                    # Process through blockchain
                    result = orchestrator.process_security_event(event_data)
                    
                    st.write(f"🔗 Block #{i+1}: {event_data['ip']} - {event_data['type']}")
                    st.write(f"   TX: {result['threat_transaction']}")
                    st.write(f"   Score: {result['threat_score']:.3f}")
                    
                    time.sleep(1)
        
        # Threat Database Visualization
        st.subheader("📊 Decentralized Threat Database")
        
        threat_data = [
            {"IP": "192.168.1.100", "Type": "malware", "Score": 0.95, "Validators": 3, "Status": "🔴 Confirmed"},
            {"IP": "10.0.0.50", "Type": "port_scan", "Score": 0.75, "Validators": 2, "Status": "🟡 Pending"},
            {"IP": "172.16.1.20", "Type": "ddos", "Score": 0.85, "Validators": 3, "Status": "🔴 Confirmed"},
        ]
        
        df = pd.DataFrame(threat_data)
        st.dataframe(df, use_container_width=True)
        
        # Multi-Signature Actions
        st.subheader("✍️ Multi-Signature Security Actions")
        
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            if st.button("🚫 Propose IP Block"):
                st.info("Multi-sig proposal created. Awaiting approvals...")
        
        with col_b:
            if st.button("✅ Approve Action"):
                st.success("Action approved. 2/3 signatures collected.")
        
        with col_c:
            if st.button("⚡ Execute Action"):
                st.success("Multi-sig action executed on blockchain!")
    
    with col2:
        st.subheader("🏆 Reputation System")
        
        # Node Reputation Scores
        reputation_data = [
            {"Node": "Node-001", "Reputation": 95, "Detections": 150, "Rewards": "500 APT"},
            {"Node": "Node-002", "Reputation": 87, "Detections": 120, "Rewards": "400 APT"},
            {"Node": "Node-003", "Reputation": 92, "Detections": 135, "Rewards": "450 APT"},
        ]
        
        for node in reputation_data:
            with st.container():
                st.metric(
                    node["Node"], 
                    f"{node['Reputation']}/100",
                    delta=f"{node['Detections']} detections"
                )
                st.caption(f"Rewards: {node['Rewards']}")
        
        # Consensus Validation
        st.subheader("🤝 Consensus Validation")
        
        consensus_metrics = {
            "Active Validators": 5,
            "Consensus Threshold": "60%",
            "Validated Threats": 247,
            "Pending Validation": 3
        }
        
        for metric, value in consensus_metrics.items():
            st.metric(metric, value)
        
        # Blockchain Statistics
        st.subheader("📈 Blockchain Stats")
        
        blockchain_stats = {
            "Total Transactions": 1247,
            "Threat Records": 89,
            "Security Incidents": 156,
            "Gas Used": "45.2K"
        }
        
        for stat, value in blockchain_stats.items():
            st.metric(stat, value)
        
        # Token Economics
        st.subheader("💰 Token Economics")
        
        st.metric("Total Rewards Distributed", "2,450 APT")
        st.metric("Security Staking Pool", "10,000 APT")
        st.metric("Governance Tokens", "50,000 MYC")
        
        if st.button("🎁 Claim Rewards"):
            st.balloons()
            st.success("Rewards claimed: 25 APT!")

if __name__ == "__main__":
    main()