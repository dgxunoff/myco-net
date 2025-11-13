"""
RL-Enhanced Streamlit Application for MycoShield
"""

import streamlit as st
import pandas as pd
import numpy as np
import time
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mycoshield import MyceliumVisualizer
from mycoshield.rl import MyceliumRLAgent, ACTIONS
from mycoshield.core import NetworkProcessor

class RLMycoShield:
    def __init__(self):
        self.rl_agent = MyceliumRLAgent()
        self.processor = NetworkProcessor()
        self.visualizer = MyceliumVisualizer()
        self.isolated_nodes = set()
        self.monitored_nodes = set()
        self.action_history = []
        self.reward_history = []
        
        try:
            self.rl_agent.load_model('mycoshield_rl_model.pth')
            st.success("🤖 Loaded trained RL model!")
        except:
            st.info("💡 Using untrained RL model. Run train_rl.py to train.")
    
    def rl_detect_and_respond(self):
        graph_data, node_list = self.processor.get_graph_data()
        if graph_data is None:
            return {}, {}
        
        suspicious_nodes = []
        for i, node in enumerate(node_list):
            if self.processor.G.degree(node) > np.mean([self.processor.G.degree(n) for n in self.processor.G.nodes()]):
                suspicious_nodes.append(i)
                
        if not suspicious_nodes:
            suspicious_nodes = list(range(min(5, len(node_list))))
            
        actions = self.rl_agent.select_action(graph_data, suspicious_nodes)
        
        rewards = {}
        action_results = {}
        
        for node_idx, action in actions.items():
            if node_idx < len(node_list):
                node = node_list[node_idx]
                action_name = ACTIONS[action]
                
                if action == 0:  # ALLOW
                    if node in self.isolated_nodes:
                        self.isolated_nodes.remove(node)
                    if node in self.monitored_nodes:
                        self.monitored_nodes.remove(node)
                    reward = 1
                    
                elif action == 1:  # MONITOR
                    self.monitored_nodes.add(node)
                    if node in self.isolated_nodes:
                        self.isolated_nodes.remove(node)
                    reward = 2
                    
                elif action == 2:  # ISOLATE
                    self.isolated_nodes.add(node)
                    if node in self.monitored_nodes:
                        self.monitored_nodes.remove(node)
                    reward = 5
                    
                rewards[node_idx] = reward
                action_results[node] = {
                    'action': action_name,
                    'reward': reward,
                    'node_idx': node_idx
                }
        
        if len(self.action_history) > 0:
            prev_state, prev_actions, prev_rewards = self.action_history[-1]
            self.rl_agent.store_experience(prev_state, prev_actions, prev_rewards, graph_data)
            
        self.rl_agent.train()
        
        self.action_history.append((graph_data, actions, rewards))
        self.reward_history.extend(list(rewards.values()))
        
        if len(self.action_history) > 100:
            self.action_history = self.action_history[-100:]
        if len(self.reward_history) > 1000:
            self.reward_history = self.reward_history[-1000:]
            
        return action_results, rewards

def main():
    st.set_page_config(
        page_title="🤖 MycoShield RL",
        page_icon="🤖",
        layout="wide"
    )
    
    st.markdown('<h1 style="color: #00ff00; text-align: center;">🤖 MycoShield RL</h1>', 
                unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #888;">Reinforcement Learning Enhanced Mycelium Defense</p>', 
                unsafe_allow_html=True)
    
    if 'rl_mycoshield' not in st.session_state:
        st.session_state.rl_mycoshield = RLMycoShield()
        
    with st.sidebar:
        st.header("🤖 RL Control Panel")
        
        auto_refresh = st.checkbox("Auto RL Decision Making", True)
        refresh_rate = st.slider("Decision Rate (sec)", 1, 10, 3)
        
        st.subheader("RL Parameters")
        st.metric("Epsilon (Exploration)", f"{st.session_state.rl_mycoshield.rl_agent.epsilon:.3f}")
        st.metric("Total Steps", st.session_state.rl_mycoshield.rl_agent.step_count)
        
        if st.button("🧪 Generate Demo Traffic"):
            demo_data = {
                'orig_h': f"192.168.1.{np.random.randint(1,20)}",
                'resp_h': f"192.168.1.{np.random.randint(1,20)}",
                'orig_p': np.random.randint(1024, 65535),
                'resp_p': np.random.choice([80, 443, 22, 21, 25]),
                'proto': np.random.choice(['tcp', 'udp']),
                'duration': np.random.exponential(2),
                'orig_bytes': np.random.randint(64, 1500),
                'resp_bytes': np.random.randint(64, 1500),
                'threat_score': np.random.random()
            }
            st.session_state.rl_mycoshield.processor.update_graph(demo_data)
            st.success("Demo traffic generated!")
            
        st.subheader("📊 RL Stats")
        st.metric("Active Nodes", len(st.session_state.rl_mycoshield.processor.G.nodes()))
        st.metric("Isolated Nodes", len(st.session_state.rl_mycoshield.isolated_nodes))
        st.metric("Monitored Nodes", len(st.session_state.rl_mycoshield.monitored_nodes))
        
        if st.session_state.rl_mycoshield.reward_history:
            avg_reward = np.mean(st.session_state.rl_mycoshield.reward_history[-100:])
            st.metric("Avg Reward (last 100)", f"{avg_reward:.2f}")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        chart_placeholder = st.empty()
        
    with col2:
        rl_info_placeholder = st.empty()
        
    if auto_refresh and len(st.session_state.rl_mycoshield.processor.G.nodes()) > 0:
        while True:
            action_results, rewards = st.session_state.rl_mycoshield.rl_detect_and_respond()
            
            fig = st.session_state.rl_mycoshield.visualizer.create_rl_visualization(
                st.session_state.rl_mycoshield.processor.G,
                list(st.session_state.rl_mycoshield.processor.G.nodes()),
                action_results,
                st.session_state.rl_mycoshield.isolated_nodes,
                st.session_state.rl_mycoshield.monitored_nodes
            )
            chart_placeholder.plotly_chart(fig, use_container_width=True)
            
            with rl_info_placeholder.container():
                st.subheader("🤖 RL Decisions")
                
                if action_results:
                    for node, result in action_results.items():
                        action_color = {
                            'ALLOW': '🟢',
                            'MONITOR': '🟡', 
                            'ISOLATE': '🔴'
                        }
                        
                        color = action_color.get(result['action'], '⚪')
                        st.write(f"{color} **{node}**: {result['action']} (Reward: {result['reward']})")
                        
                    total_reward = sum(rewards.values())
                    if total_reward > 0:
                        st.success(f"🏆 Total Reward: +{total_reward}")
                    else:
                        st.warning(f"⚠️ Total Reward: {total_reward}")
                else:
                    st.info("🤖 RL Agent learning from network patterns...")
                    
                if len(st.session_state.rl_mycoshield.reward_history) > 10:
                    recent_rewards = st.session_state.rl_mycoshield.reward_history[-10:]
                    st.line_chart(pd.DataFrame({'Reward': recent_rewards}))
                    
            time.sleep(refresh_rate)
            st.rerun()
    
    else:
        st.info("🤖 Generate demo traffic to see RL agent in action!")

if __name__ == "__main__":
    main()