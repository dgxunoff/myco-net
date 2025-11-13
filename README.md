# 🍄 MycoShield - Enterprise Mycelium Network Defense Platform

**Shaastra Biogen 2026 Winning Project → Enterprise Security Platform**

A revolutionary **Graph Neural Network (GNN)** with **Reinforcement Learning** and **Multi-Modal Detection** inspired by mycelium networks for **zero-day cyberattack detection** and **enterprise endpoint security**.

## 🚀 Quick Start

```bash
# Install as package
pip install -e .

# Run applications (4 deployment levels)
streamlit run apps/streamlit_app.py    # Basic: Network detection
streamlit run apps/rl_app.py           # Advanced: RL-enhanced
streamlit run apps/multimodal_app.py   # Professional: Multi-modal
streamlit run apps/enterprise_app.py   # Enterprise: Full platform

# Or use console commands
mycoshield-app          # Basic network detection
mycoshield-rl           # RL-enhanced detection
mycoshield-multimodal   # Network + Host + Logs
mycoshield-enterprise   # Complete security platform
```

## 🧬 Core Concept

- **Mycelium Network**: Each network node = fungal cell
- **Hyphae Connections**: Network traffic flows as growing hyphae
- **Spore Detection**: Anomalies detected as "fungal infections"
- **Auto-Isolation**: Infected nodes turn black and get isolated
- **RL Evolution**: System learns optimal defense strategies

## 🎯 Features

### ✅ Network Detection (Basic)
- **GNN Model**: 3-layer Graph Convolutional Network
- **PCAP Parser**: Real network traffic analysis
- **3D Visualization**: Interactive mycelium network (Plotly)
- **NSL-KDD Training**: 125K+ real attack samples (80%+ accuracy)

### ✅ RL Enhancement (Advanced)
- **RL Agent**: Deep Q-Network for adaptive responses
- **Auto-Isolation**: Infected node quarantine
- **Action Learning**: ALLOW/MONITOR/ISOLATE decisions

### ✅ Multi-Modal Detection (Professional)
- **Host Monitoring**: Process & file system analysis
- **Log Analysis**: System & application log parsing
- **Correlation Engine**: Cross-source threat validation
- **Live Monitoring**: Real-time Zeek log processing

### ✅ Enterprise Platform (Complete)
- **Registry Monitoring**: Windows registry change detection
- **Memory Analysis**: Code injection & process anomalies
- **Malware Scanning**: YARA-based signature detection
- **Behavioral Analysis**: ML-based anomaly detection
- **User Activity**: Session & privilege escalation monitoring
- **Device Fingerprinting**: Hardware asset management
- **Real Firewall Integration**: Actual IP blocking
- **Incident Response**: Automated threat containment
- **Security Dashboard**: Enterprise monitoring interface

### 🔄 Architecture
```
Live Traffic → Zeek Logs → Graph Builder → MyceliumGNN → RL Agent → Actions → 3D Viz
```

## 🎮 Deployment Levels

### **Level 1: Basic Network Detection** 🍄
```bash
mycoshield-app
```
**Perfect for**: Hackathons, demos, proof-of-concept
- Upload PCAP files
- Demo traffic generation
- GNN-based threat detection
- 3D mycelium visualization
- Bio-inspired network analysis

### **Level 2: RL-Enhanced Detection** 🤖
```bash
mycoshield-rl
```
**Perfect for**: AI competitions, ML challenges
- Autonomous decision making
- Adaptive threat response
- Real-time learning
- Action visualization (Allow/Monitor/Isolate)
- Reinforcement learning showcase

### **Level 3: Multi-Modal Detection** 🔍
```bash
mycoshield-multimodal
```
**Perfect for**: Security competitions, enterprise demos
- Network + Host + Log analysis
- Multi-source correlation
- Real firewall blocking
- Incident logging
- Live monitoring dashboard

### **Level 4: Enterprise Platform** 🏢
```bash
mycoshield-enterprise
```
**Perfect for**: Production deployment, startup demos
- Complete endpoint security
- Registry & memory monitoring
- Malware detection (YARA rules)
- Behavioral analysis
- Device fingerprinting
- Automated incident response
- Enterprise security dashboard

### **Live Zeek Integration** (Linux/macOS)
```bash
# Start Zeek monitoring
zeek -i any zeek_mycoshield.zeek

# Run any application level
mycoshield-app  # or any other level
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

## 🔬 Enterprise Technical Stack

### **AI/ML Core**
- **Deep Learning**: PyTorch + PyTorch Geometric
- **Reinforcement Learning**: Deep Q-Network (DQN)
- **Graph Processing**: NetworkX
- **Dataset**: NSL-KDD (125K+ samples, 80%+ accuracy)

### **Security Technologies**
- **Network Monitoring**: Zeek + Scapy + psutil
- **Malware Detection**: YARA rules engine
- **Firewall Integration**: Windows/Linux/macOS
- **Memory Analysis**: Process injection detection
- **Registry Monitoring**: Windows registry tracking

### **Platform & UI**
- **Frontend**: Streamlit + Plotly 3D
- **Visualization**: Interactive mycelium networks
- **Dashboard**: Enterprise security metrics
- **APIs**: RESTful security endpoints

### **DevOps & Quality**
- **Testing**: pytest + unittest + mocking
- **Packaging**: setuptools + pip installable
- **Configuration**: JSON-based security policies
- **Logging**: Comprehensive incident tracking

## 🧪 Attack Simulations

```bash
# Port scan simulation
nmap -sS 192.168.1.1

# Suspicious IP ping
ping -c 5 203.0.113.1

# Generate demo traffic
# Click "Generate Demo Traffic" in apps
```

## 📁 Enterprise Project Structure

```
MycoNet/
├── mycoshield/                 # Core Security Package
│   ├── models.py              # GNN & DQN architectures
│   ├── core.py                # Network processing
│   ├── data.py                # PCAP & Zeek parsing
│   ├── visualization.py       # 3D rendering
│   ├── rl.py                  # Reinforcement learning
│   ├── security.py            # Firewall & enforcement
│   ├── host.py                # Host monitoring
│   ├── endpoint.py            # Endpoint security
│   └── enterprise.py          # Enterprise orchestration
│
├── apps/                      # Multi-Level Applications
│   ├── streamlit_app.py      # Level 1: Basic
│   ├── rl_app.py             # Level 2: RL-Enhanced
│   ├── multimodal_app.py     # Level 3: Multi-Modal
│   └── enterprise_app.py     # Level 4: Enterprise
│
├── tests/                     # Comprehensive Test Suite
│   ├── test_models.py        # Neural network tests
│   ├── test_core.py          # Core component tests
│   ├── test_security.py      # Security enforcement tests
│   ├── test_rl.py            # RL agent tests
│   ├── test_data.py          # Data processing tests
│   ├── test_integration.py   # End-to-end tests
│   └── run_tests.py          # Test runner
│
├── train_nslkdd.py           # GNN training (NSL-KDD)
├── train_rl.py               # RL training
├── security_config.json      # Security configuration
├── requirements.txt          # Dependencies
├── setup.py                  # Package installation
└── zeek_mycoshield.zeek      # Zeek policy
```

## 🎪 Demo Scenarios by Level

### **Level 1 Demos** (Hackathons)
1. **Bio-Inspired Visualization**: 3D mycelium network growth
2. **PCAP Analysis**: Upload → GNN detection → Spore alerts
3. **Demo Traffic**: Instant threat simulation

### **Level 2 Demos** (AI Competitions)
1. **RL Learning**: Watch agent learn optimal responses
2. **Adaptive Decisions**: ALLOW/MONITOR/ISOLATE actions
3. **Performance Metrics**: Learning curves & accuracy

### **Level 3 Demos** (Security Events)
1. **Multi-Source Detection**: Network + Host + Logs
2. **Correlation Analysis**: Cross-source threat validation
3. **Real Enforcement**: Actual firewall blocking

### **Level 4 Demos** (Enterprise/Startup)
1. **Complete Platform**: Full endpoint security
2. **Live Monitoring**: Real-time threat hunting
3. **Incident Response**: Automated containment
4. **Security Dashboard**: Enterprise metrics

## 🧪 Testing & Quality

```bash
# Run comprehensive test suite
python tests/run_tests.py

# Run with coverage
pytest tests/ --cov=mycoshield

# Run specific test module
python tests/run_tests.py test_models
```

- **Unit Tests**: All core components
- **Integration Tests**: End-to-end workflows
- **Mocking**: External dependencies
- **Performance Tests**: Large dataset handling

## 🏆 Competition Readiness

**Choose your demo level**:
- **Basic Hackathons**: Level 1 (mycoshield-app)
- **AI/ML Events**: Level 2 (mycoshield-rl)
- **Security Competitions**: Level 3 (mycoshield-multimodal)
- **Startup Pitches**: Level 4 (mycoshield-enterprise)

---

**From Shaastra Biogen 2026 Winner → Enterprise Security Platform** 🏆  
**World's First Mycelium-Inspired Multi-Modal Cybersecurity System** 🍄🤖🛡️