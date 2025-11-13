# 🍄 MycoShield - Mycelium Network Defense System

**Shaastra Biogen 2026 Winning Project**

A revolutionary **Graph Neural Network (GNN)** with **Reinforcement Learning** inspired by mycelium networks for **zero-day cyberattack detection**.

## 🚀 Quick Start

```bash
# Install as package
pip install -e .

# Run applications
streamlit run apps/streamlit_app.py  # Main app
streamlit run apps/rl_app.py         # RL-enhanced app

# Or use console commands
mycoshield-app    # Main interface
mycoshield-rl     # RL interface
```

## 🧬 Core Concept

- **Mycelium Network**: Each network node = fungal cell
- **Hyphae Connections**: Network traffic flows as growing hyphae
- **Spore Detection**: Anomalies detected as "fungal infections"
- **Auto-Isolation**: Infected nodes turn black and get isolated
- **RL Evolution**: System learns optimal defense strategies

## 🎯 Features

### ✅ Implemented
- **GNN Model**: 3-layer Graph Convolutional Network
- **RL Agent**: Deep Q-Network for adaptive responses
- **PCAP Parser**: Real network traffic analysis
- **Live Monitoring**: Real-time Zeek log processing
- **3D Visualization**: Interactive mycelium network (Plotly)
- **Auto-Isolation**: Infected node quarantine
- **NSL-KDD Training**: 125K+ real attack samples

### 🔄 Architecture
```
Live Traffic → Zeek Logs → Graph Builder → MyceliumGNN → RL Agent → Actions → 3D Viz
```

## 🎮 Usage Options

### **1. Main Application**
```bash
streamlit run apps/streamlit_app.py
```
- Upload PCAP files
- Demo traffic generation
- GNN-based threat detection
- 3D mycelium visualization

### **2. RL-Enhanced Application**
```bash
streamlit run apps/rl_app.py
```
- Autonomous decision making
- Adaptive threat response
- Real-time learning
- Action visualization (Allow/Monitor/Isolate)

### **3. Live Zeek Integration** (Linux/macOS)
```bash
# Start Zeek monitoring
zeek -i any zeek_mycoshield.zeek

# Run live app
streamlit run apps/streamlit_app.py
```
- Real-time network capture
- Live mycelium growth
- Instant threat detection

## 🤖 Reinforcement Learning

### **RL Actions**
- **🟢 ALLOW**: Let connection continue
- **🟡 MONITOR**: Increase surveillance
- **🔴 ISOLATE**: Block/quarantine node

### **Learning Process**
1. **Observe** network state
2. **Select** action (ε-greedy policy)
3. **Execute** security response
4. **Receive** reward based on outcome
5. **Learn** better strategies over time

### **Training**
```bash
python train_rl.py  # Train RL agent
```

## 🏆 Competition Advantages

### **Bio-Inspired Innovation**
- Unique mycelium network metaphor
- Organic growth visualization
- Fungal infection detection model

### **AI/ML Excellence**
- Graph Neural Networks for network topology
- Reinforcement Learning for adaptive responses
- Unsupervised anomaly detection
- Real NSL-KDD dataset training (80%+ accuracy)

### **Real-Time Capability**
- Live network monitoring (Zeek integration)
- Instant threat detection and response
- Continuous learning and adaptation

### **Visual Impact**
- Stunning 3D mycelium network
- Live growing hyphae connections
- Dramatic spore alert system
- RL decision visualization

## 📊 Detection Metrics

- **🍄 Infected**: Anomaly score > 0.7 (Red spores)
- **⚠️ Suspicious**: Score 0.5-0.7 (Yellow warning)
- **✅ Healthy**: Score < 0.5 (Green mycelium)
- **🤖 RL Actions**: Color-coded by decision type

## 🔬 Technical Stack

- **Deep Learning**: PyTorch + PyTorch Geometric
- **Reinforcement Learning**: Deep Q-Network (DQN)
- **Frontend**: Streamlit + Plotly 3D
- **Network Monitoring**: Zeek + Scapy
- **Graph Processing**: NetworkX
- **Dataset**: NSL-KDD (125K+ samples)

## 🧪 Attack Simulations

```bash
# Port scan simulation
nmap -sS 192.168.1.1

# Suspicious IP ping
ping -c 5 203.0.113.1

# Generate demo traffic
# Click "Generate Demo Traffic" in apps
```

## 📁 Project Structure

```
MycoNet/
├── mycoshield/              # Core Package
│   ├── models.py           # GNN & DQN architectures
│   ├── core.py             # Network processing
│   ├── data.py             # PCAP & Zeek parsing
│   ├── visualization.py    # 3D rendering
│   └── rl.py              # Reinforcement learning
│
├── apps/                   # Applications
│   ├── streamlit_app.py   # Main interface
│   └── rl_app.py          # RL interface
│
├── train_nslkdd.py        # GNN training
├── train_rl.py            # RL training
└── zeek_mycoshield.zeek   # Zeek policy
```

## 🎪 Demo Scenarios

1. **Static Analysis**: Upload PCAP → GNN detection → 3D visualization
2. **RL Decision Making**: Generate traffic → RL agent actions → Learning
3. **Live Monitoring**: Zeek capture → Real-time analysis → Auto-response
4. **Attack Simulation**: Built-in scenarios → Threat detection → Isolation

---

**Built for Shaastra Biogen 2026** 🏆  
**World's First Mycelium-Inspired RL Cybersecurity System** 🍄🤖