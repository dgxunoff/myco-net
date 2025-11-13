"""
Multi-Modal MycoShield Application - Network + Host + Logs
"""

import streamlit as st
import torch
import pandas as pd
import time
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mycoshield import (MyceliumGNN, NetworkProcessor, ThreatDetector, 
                       SecurityEnforcer, HostMonitor, LogAnalyzer, 
                       MultiModalDetector, MyceliumVisualizer)

def main():
    st.set_page_config(
        page_title="🍄 MycoShield Multi-Modal",
        page_icon="🍄",
        layout="wide"
    )
    
    st.markdown('<h1 style="color: #00ff00; text-align: center;">🍄 MycoShield Multi-Modal Defense</h1>', 
                unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #888;">Network + Host + Log Analysis</p>', 
                unsafe_allow_html=True)
    
    # Initialize components
    if 'multimodal' not in st.session_state:
        # Load model
        try:
            checkpoint = torch.load('mycoshield_nslkdd.pth', map_location='cpu')
            input_dim = checkpoint['conv1.lin.weight'].shape[1]
            model = MyceliumGNN(input_dim=input_dim)
            model.load_state_dict(checkpoint)
        except:
            model = MyceliumGNN(input_dim=6)
        
        # Initialize all components
        enforcer = SecurityEnforcer()
        network_detector = ThreatDetector(model, enforcer)
        host_monitor = HostMonitor()
        log_analyzer = LogAnalyzer()
        
        # Establish host baseline
        host_monitor.establish_baseline()
        
        st.session_state.multimodal = {
            'detector': MultiModalDetector(network_detector, host_monitor, log_analyzer),
            'host_monitor': host_monitor,
            'log_analyzer': log_analyzer,
            'enforcer': enforcer,
            'visualizer': MyceliumVisualizer()
        }
    
    # Sidebar controls
    with st.sidebar:
        st.header("🔬 Multi-Modal Controls")
        
        analysis_mode = st.selectbox("Analysis Mode", 
                                   ["Real-Time Monitoring", "Host Analysis", "Log Analysis", "Full Scan"])
        
        if st.button("🚀 Start Analysis"):
            st.session_state.analysis_running = True
        
        if st.button("⏹️ Stop Analysis"):
            st.session_state.analysis_running = False
    
    # Main dashboard
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("🌐 Network Threats")
        network_placeholder = st.empty()
    
    with col2:
        st.subheader("💻 Host Threats")
        host_placeholder = st.empty()
    
    with col3:
        st.subheader("📋 Log Threats")
        log_placeholder = st.empty()
    
    # Analysis results
    st.subheader("🔍 Comprehensive Analysis Results")
    results_placeholder = st.empty()
    
    # Real-time monitoring
    if st.session_state.get('analysis_running', False):
        
        for i in range(10):  # Run for 10 iterations
            
            # Perform comprehensive analysis
            analysis_results = st.session_state.multimodal['detector'].comprehensive_analysis()
            
            # Update network threats
            with network_placeholder.container():
                network_threats = analysis_results['network']
                if network_threats:
                    max_score = max(network_threats.values())
                    st.metric("Max Network Threat", f"{max_score:.3f}")
                    if max_score > 0.7:
                        st.error("🚨 High network threat detected!")
                else:
                    st.success("✅ Network clean")
            
            # Update host threats
            with host_placeholder.container():
                host_threats = analysis_results['host']['processes']
                if host_threats:
                    st.metric("Suspicious Processes", len(host_threats))
                    if len(host_threats) > 0:
                        st.warning(f"⚠️ {len(host_threats)} suspicious processes")
                else:
                    st.success("✅ Host clean")
            
            # Update log threats
            with log_placeholder.container():
                log_threats = analysis_results['logs']
                if log_threats:
                    st.metric("Log Alerts", len(log_threats))
                    if len(log_threats) > 0:
                        st.warning(f"⚠️ {len(log_threats)} log alerts")
                else:
                    st.success("✅ Logs clean")
            
            # Update comprehensive results
            with results_placeholder.container():
                correlation_score = analysis_results['correlation_score']
                recommended_action = analysis_results['recommended_action']
                
                st.metric("Correlation Score", f"{correlation_score:.3f}")
                
                if correlation_score > 0.8:
                    st.error(f"🚨 CRITICAL THREAT - Action: {recommended_action}")
                elif correlation_score > 0.6:
                    st.warning(f"⚠️ MODERATE THREAT - Action: {recommended_action}")
                else:
                    st.success(f"✅ LOW RISK - Action: {recommended_action}")
                
                # Detailed breakdown
                if host_threats:
                    st.subheader("🔍 Host Threat Details")
                    threat_data = []
                    for threat in host_threats[:5]:  # Show top 5
                        threat_data.append({
                            'Type': threat['type'],
                            'Process': threat.get('name', 'N/A'),
                            'PID': threat.get('pid', 'N/A'),
                            'Threat Score': f"{threat['threat_score']:.3f}"
                        })
                    
                    if threat_data:
                        st.dataframe(pd.DataFrame(threat_data))
                
                if log_threats:
                    st.subheader("📋 Log Threat Details")
                    log_data = []
                    for threat in log_threats[:5]:
                        log_data.append({
                            'Type': threat['type'],
                            'Event': threat['event'][:100] + '...' if len(threat['event']) > 100 else threat['event'],
                            'Threat Score': f"{threat['threat_score']:.3f}"
                        })
                    
                    if log_data:
                        st.dataframe(pd.DataFrame(log_data))
            
            time.sleep(2)  # Update every 2 seconds
            
            if not st.session_state.get('analysis_running', False):
                break
    
    # System metrics
    st.subheader("📊 System Metrics")
    if st.session_state.get('multimodal'):
        metrics = st.session_state.multimodal['host_monitor'].get_system_metrics()
        
        col_a, col_b, col_c, col_d = st.columns(4)
        
        with col_a:
            st.metric("CPU Usage", f"{metrics['cpu_percent']:.1f}%")
        
        with col_b:
            st.metric("Memory Usage", f"{metrics['memory_percent']:.1f}%")
        
        with col_c:
            st.metric("Disk Usage", f"{metrics['disk_usage']:.1f}%")
        
        with col_d:
            st.metric("Active Connections", metrics['network_connections'])

if __name__ == "__main__":
    main()