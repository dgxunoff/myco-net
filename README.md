# 🍄 MycoShield - Blockchain-Powered Cybersecurity Platform

**World's First Mycelium-Inspired Network Defense with Aptos Blockchain Integration**

AI-powered cybersecurity system that mimics fungal networks to detect threats and uses blockchain for decentralized security intelligence.

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run MycoShield
streamlit run apps/streamlit_app.py

# Check MYCO balance
python check_myco.py
```

## 🧬 How It Works (Simple Explanation)

**Think of your network like a fungal forest:**
- **Network nodes** = Mushrooms in the forest
- **Data connections** = Underground fungal threads (mycelium)
- **Cyber threats** = Diseases spreading through the network
- **MycoShield** = Immune system that detects and stops diseases

**AI Detection Process:**
1. Monitor all network connections (like fungal threads)
2. Use Graph Neural Networks to spot unusual patterns
3. Mark suspicious nodes as "infected" (red spores)
4. Automatically isolate threats to protect the network

## 🔗 Why Blockchain? (Main Purpose)

**Think of Blockchain as a "Digital Security Notebook" that:**

### 📝 **Keeps Permanent Records**
- Normal way: Security incidents stored in files that can be deleted/changed
- **Blockchain way**: All security events written in permanent digital book that CANNOT be erased
- **Example**: When MycoShield blocks a hacker IP, it's recorded forever on blockchain

### 🤝 **Gets Multiple Opinions Before Acting**
- Normal way: One computer decides if something is dangerous
- **Blockchain way**: Multiple computers vote together to confirm if threat is real
- **Example**: 3 different security nodes must agree "192.168.1.100 is malware" before blocking

### 💰 **Rewards Good Security Work**
- Normal way: No rewards for detecting threats
- **Blockchain way**: Get paid in crypto tokens (APT) for finding real threats
- **Example**: Find malware = earn 100 APT tokens, false alarm = lose reputation

### 🌐 **Shares Threat Information Globally**
- Normal way: Each company keeps their own threat list
- **Blockchain way**: All companies share one global threat database
- **Example**: If Company A finds new malware, Company B instantly knows about it

### 🔒 **Requires Multiple Approvals for Big Actions**
- Normal way: One person can block entire networks
- **Blockchain way**: Multiple security experts must approve big decisions
- **Example**: Blocking 1000 IPs needs 3 out of 5 security managers to approve

**In Simple Terms**: Blockchain makes MycoShield's security decisions more trustworthy, permanent, and globally shared!

## 🎯 Features

### **🤖 AI-Powered Detection**
- Graph Neural Networks trained on NSL-KDD dataset
- 80%+ accuracy on real attack data
- Real-time threat scoring
- 3D network visualization

### **🔗 Blockchain Integration**
- MYCO token rewards (300 MYCO earned!)
- Deployed on Aptos testnet
- Automatic minting on threat detection
- Permanent security audit trail
- Reputation system (77/100)

### **🛡️ Security Actions**
- Automatic threat isolation
- Firewall integration
- Real-time monitoring
- Incident logging
- Manual IP blocking/unblocking

## 🤖 How AI Makes Decisions

**The AI can take 3 actions when it finds something suspicious:**
- **🟢 ALLOW**: Let it continue (probably safe)
- **🟡 MONITOR**: Watch it closely (might be dangerous)
- **🔴 ISOLATE**: Block it immediately (definitely dangerous)

**Learning Process:**
1. AI observes network behavior
2. Makes a decision (Allow/Monitor/Isolate)
3. Sees if the decision was correct
4. Gets better at making decisions over time

## 🏆 What Makes MycoShield Special

### **🧬 Bio-Inspired Design**
- First cybersecurity system inspired by fungal networks
- Beautiful 3D visualization of network connections
- Natural approach to threat detection

### **🤖 Advanced AI**
- Graph Neural Networks understand network relationships
- Reinforcement Learning adapts to new threats
- 80%+ accuracy on real attack data

### **🔗 Blockchain Innovation**
- World's first blockchain-powered cybersecurity
- Permanent, tamper-proof security records
- Global threat intelligence sharing
- Economic incentives for good security

## 📊 How to Read the Results

- **🔴 Infected**: High threat score (Dangerous - Block immediately)
- **🟡 Suspicious**: Medium threat score (Watch carefully)
- **🟢 Healthy**: Low threat score (Safe - Allow normally)

## 🔧 Technical Details

### **AI Technologies**
- **PyTorch**: Deep learning framework
- **Graph Neural Networks**: Understand network connections
- **Reinforcement Learning**: AI that learns from experience

### **Blockchain Technologies**
- **Aptos Blockchain**: Stores security data permanently
- **Move Language**: Smart contracts for security actions
- **Multi-Signature**: Multiple approvals for big decisions

### **Security Integration**
- **Real Firewalls**: Actually blocks dangerous IPs
- **Live Monitoring**: Watches network traffic in real-time
- **Cross-Platform**: Works on Windows, Linux, macOS

## 🧪 Try It Out

```bash
# Test with demo data
# Click "Generate Demo Traffic" in the app

# Or test with real network files
# Upload your .pcap files to analyze
```

## 📁 Project Structure

```
MycoNet/
├── apps/
│   └── streamlit_app.py          # Main web interface
├── mycoshield/                   # Core modules
│   ├── aptos_security.py         # Blockchain integration
│   ├── blockchain_integration.py # Security orchestrator
│   ├── core.py                   # Threat detection
│   ├── models.py                 # GNN models
│   ├── security.py               # Security enforcement
│   └── visualization.py          # 3D visualization
├── contracts/
│   ├── sources/                  # Move smart contracts
│   │   └── MycoRewardToken.move  # MYCO token
│   ├── Move.toml                 # Contract config
│   └── deploy_contracts.py       # Deployment script
├── tests/                        # Test suite
├── .env                          # Wallet configuration
├── check_myco.py                 # Balance checker
├── mycoshield_nslkdd.pth         # Trained AI model
├── requirements.txt              # Dependencies
└── README.md                     # This file
```

## 🎪 Demo Ideas

### **For Hackathons**
- Show the beautiful 3D fungal network visualization
- Upload network files and watch threat detection
- Generate demo attacks and see automatic blocking

### **For AI Competitions**
- Demonstrate machine learning that gets smarter over time
- Show how AI makes security decisions
- Display accuracy improvements with training

### **For Blockchain Events**
- Show permanent security records on blockchain
- Demonstrate multi-signature security approvals
- Display token rewards for threat detection

### **For Business Demos**
- Complete enterprise security dashboard
- Real-time threat monitoring
- Automated incident response

## 🧪 Testing & Usage

```bash
# Check MYCO balance
python check_myco.py

# Run main application
streamlit run apps/streamlit_app.py

# Mint MYCO tokens manually
aptos move run \
  --function-id 0x84226fc4...::myco_reward::reward_threat_detection \
  --args address:0x84226fc4... u64:3 bool:true --assume-yes

# Run tests
python -m pytest tests/
```

## 🏆 Current Status

- ✅ **MYCO Token**: Live on Aptos testnet
- ✅ **Balance**: 300 MYCO earned
- ✅ **Reputation**: 77/100
- ✅ **Threats Detected**: 2
- ✅ **Network**: Aptos Testnet

## 🎯 Perfect For

- **🏫 Hackathons**: Real blockchain integration + AI detection
- **🤖 AI Competitions**: GNN trained on NSL-KDD dataset
- **🔗 Blockchain Events**: Working MYCO token on Aptos
- **🏢 Business Demos**: Production-ready security platform
- **🎓 Research**: Novel bio-inspired + blockchain approach

## 📚 Documentation

- `QUICK_START.md` - Quick reference guide
- `DEPLOYMENT_SUCCESS.md` - Deployment details
- `MYCO_APTOS_EXPLAINED.md` - Token architecture
- `WORKING_COMMANDS.md` - All commands
- `FINAL_SETUP.md` - Complete setup guide

---

**🍄 World's First Mycelium-Inspired Blockchain-Powered Cybersecurity Platform 🔗**