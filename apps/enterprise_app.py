"""
Enterprise MycoShield Dashboard
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mycoshield import MyceliumGNN, ThreatDetector, SecurityEnforcer
from mycoshield.enterprise import EnterpriseMycoShield

def main():
    st.set_page_config(
        page_title="🍄 MycoShield Enterprise",
        page_icon="🍄",
        layout="wide"
    )
    
    st.markdown('<h1 style="color: #00ff00; text-align: center;">🍄 MycoShield Enterprise Security Platform</h1>', 
                unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #888;">Complete Endpoint + Network + Application Security</p>', 
                unsafe_allow_html=True)
    
    # Initialize enterprise platform
    if 'enterprise' not in st.session_state:
        
        # Load security config
        try:
            import json
            with open('security_config.json', 'r') as f:
                config = json.load(f)
        except:
            config = {}
        
        # Initialize enterprise platform
        enterprise = EnterpriseMycoShield(config)
        
        st.session_state.enterprise = enterprise
        st.session_state.monitoring_started = False
    
    # Sidebar controls
    with st.sidebar:
        st.header("🎛️ Enterprise Controls")
        
        # Monitoring controls
        if not st.session_state.monitoring_started:
            if st.button("🚀 Start Enterprise Monitoring"):
                st.session_state.enterprise.start_monitoring()
                st.session_state.monitoring_started = True
                st.success("Enterprise monitoring started!")
        else:
            if st.button("⏹️ Stop Monitoring"):
                st.session_state.enterprise.stop_monitoring()
                st.session_state.monitoring_started = False
                st.info("Monitoring stopped")
        
        st.subheader("🔧 Scan Controls")
        
        if st.button("🔍 Manual Comprehensive Scan"):
            st.session_state.manual_scan = True
        
        if st.button("🧹 Clear Threat Database"):
            st.session_state.enterprise.threat_database = []
            st.success("Threat database cleared")
        
        # Configuration
        st.subheader("⚙️ Configuration")
        scan_interval = st.slider("Scan Interval (seconds)", 10, 300, 30)
        st.session_state.enterprise.config['scan_interval'] = scan_interval
        
        auto_response = st.checkbox("Auto Response to Threats", True)
        st.session_state.enterprise.config['auto_response'] = auto_response
    
    # Main dashboard
    dashboard_data = st.session_state.enterprise.get_security_dashboard()
    
    # Status overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        status_color = {"HEALTHY": "🟢", "WARNING": "🟡", "CRITICAL": "🔴"}
        st.metric("System Status", 
                 f"{status_color.get(dashboard_data['system_status'], '⚪')} {dashboard_data['system_status']}")
    
    with col2:
        st.metric("Total Threats", dashboard_data['total_threats'])
    
    with col3:
        st.metric("Critical Threats", dashboard_data['critical_threats'], 
                 delta=f"🚨" if dashboard_data['critical_threats'] > 0 else None)
    
    with col4:
        st.metric("Monitoring", "ACTIVE" if dashboard_data['monitoring_active'] else "INACTIVE")
    
    # Threat breakdown
    st.subheader("🎯 Threat Analysis")
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        # Threat categories chart
        current_threats = dashboard_data['current_threats']
        
        threat_counts = {}
        for category, threats in current_threats.items():
            if category != 'timestamp':
                if isinstance(threats, list):
                    threat_counts[category] = len(threats)
                elif isinstance(threats, dict):
                    count = 0
                    for sub_category, sub_threats in threats.items():
                        if isinstance(sub_threats, list):
                            count += len(sub_threats)
                    threat_counts[category] = count
        
        if threat_counts:
            fig_pie = px.pie(
                values=list(threat_counts.values()),
                names=list(threat_counts.keys()),
                title="Threats by Category"
            )
            st.plotly_chart(fig_pie, use_container_width=True)
    
    with col_right:
        # Threat timeline
        recent_scans = dashboard_data['recent_scans']
        
        if recent_scans:
            df_timeline = pd.DataFrame(recent_scans)
            
            fig_timeline = px.line(
                df_timeline, 
                x='timestamp', 
                y='max_threat_score',
                title="Threat Score Timeline"
            )
            st.plotly_chart(fig_timeline, use_container_width=True)
    
    # Detailed threat information
    st.subheader("🔍 Current Threat Details")
    
    # Create tabs for different threat categories
    tabs = st.tabs(["🌐 Network", "💻 Host", "📝 Registry", "🧠 Memory", "🔧 System Calls", 
                   "🦠 Malware", "👤 Users", "📱 Device", "🌐 Applications"])
    
    current_threats = dashboard_data['current_threats']
    
    with tabs[0]:  # Network
        network_threats = current_threats.get('network', {})
        if network_threats:
            st.json(network_threats)
        else:
            st.info("No network threats detected")
    
    with tabs[1]:  # Host
        host_threats = current_threats.get('host', {})
        if host_threats.get('processes'):
            df_processes = pd.DataFrame(host_threats['processes'])
            st.dataframe(df_processes, use_container_width=True)
        else:
            st.info("No host threats detected")
    
    with tabs[2]:  # Registry
        registry_threats = current_threats.get('registry', [])
        if registry_threats:
            df_registry = pd.DataFrame(registry_threats)
            st.dataframe(df_registry, use_container_width=True)
        else:
            st.info("No registry threats detected")
    
    with tabs[3]:  # Memory
        memory_threats = current_threats.get('memory', [])
        if memory_threats:
            df_memory = pd.DataFrame(memory_threats)
            st.dataframe(df_memory, use_container_width=True)
        else:
            st.info("No memory threats detected")
    
    with tabs[4]:  # System Calls
        syscall_threats = current_threats.get('syscalls', [])
        if syscall_threats:
            df_syscalls = pd.DataFrame(syscall_threats)
            st.dataframe(df_syscalls, use_container_width=True)
        else:
            st.info("No system call threats detected")
    
    with tabs[5]:  # Malware
        malware_threats = current_threats.get('malware', [])
        if malware_threats:
            df_malware = pd.DataFrame(malware_threats)
            st.dataframe(df_malware, use_container_width=True)
        else:
            st.info("No malware detected")
    
    with tabs[6]:  # Users
        user_threats = current_threats.get('users', [])
        if user_threats:
            df_users = pd.DataFrame(user_threats)
            st.dataframe(df_users, use_container_width=True)
        else:
            st.info("No user activity threats detected")
    
    with tabs[7]:  # Device
        device_threats = current_threats.get('device', [])
        if device_threats:
            df_device = pd.DataFrame(device_threats)
            st.dataframe(df_device, use_container_width=True)
        else:
            st.info("No device threats detected")
            
        # Show device fingerprint
        st.subheader("Device Fingerprint")
        st.code(dashboard_data['device_fingerprint'])
    
    with tabs[8]:  # Applications
        app_threats = current_threats.get('applications', [])
        if app_threats:
            df_apps = pd.DataFrame(app_threats)
            st.dataframe(df_apps, use_container_width=True)
        else:
            st.info("No application threats detected")
    
    # System metrics
    st.subheader("📊 System Performance")
    
    host_metrics = current_threats.get('host', {}).get('metrics', {})
    if host_metrics:
        col_a, col_b, col_c, col_d, col_e = st.columns(5)
        
        with col_a:
            st.metric("CPU Usage", f"{host_metrics.get('cpu_percent', 0):.1f}%")
        
        with col_b:
            st.metric("Memory Usage", f"{host_metrics.get('memory_percent', 0):.1f}%")
        
        with col_c:
            st.metric("Disk Usage", f"{host_metrics.get('disk_usage', 0):.1f}%")
        
        with col_d:
            st.metric("Network Connections", host_metrics.get('network_connections', 0))
        
        with col_e:
            st.metric("Running Processes", host_metrics.get('running_processes', 0))
    
    # Manual scan results
    if st.session_state.get('manual_scan', False):
        st.subheader("🔍 Manual Scan Results")
        
        with st.spinner("Performing comprehensive scan..."):
            scan_results = st.session_state.enterprise.comprehensive_scan()
        
        st.success("Scan completed!")
        st.json(scan_results)
        
        st.session_state.manual_scan = False
    
    # Auto-refresh for live monitoring
    if st.session_state.monitoring_started:
        time.sleep(5)
        st.rerun()

if __name__ == "__main__":
    main()