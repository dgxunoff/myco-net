# MycoShield - Clean Project Structure

## Core Package (mycoshield/)
```
mycoshield/
├── __init__.py              # Package initialization
├── models.py                # GNN models (MyceliumGNN, MyceliumDQN)
├── core.py                  # NetworkProcessor, ThreatDetector (with blockchain)
├── data.py                  # TrafficParser, ZeekLogTailer
├── visualization.py         # 3D mycelium visualization
├── rl.py                    # Reinforcement learning
├── security.py              # SecurityEnforcer (firewall blocking)
├── host.py                  # Host monitoring
├── endpoint.py              # Endpoint security
├── enterprise.py            # Enterprise features
├── aptos_security.py        # Aptos blockchain manager
└── blockchain_integration.py # Blockchain orchestration
```

## Main Application
```
apps/
└── streamlit_app.py         # Main app (GNN + Blockchain integrated)
```

## Smart Contracts
```
contracts/
├── ThreatIntelligence.move  # Threat storage
├── SecurityIncidents.move   # Incident logging
├── ThreatScoring.move       # Consensus validation
├── MultiSigSecurity.move    # Multi-signature actions
└── Move.toml                # Contract config
```

## Tests
```
tests/
├── test_models.py           # GNN model tests
├── test_core.py             # Core functionality tests
├── test_blockchain.py       # Blockchain tests
├── test_security.py         # Security tests
└── run_tests.py             # Test runner
```

## Key Files
```
├── README.md                # Main documentation
├── requirements.txt         # Python dependencies
├── setup.py                 # Package setup
├── train_nslkdd.py          # Train GNN on NSL-KDD
├── mycoshield_nslkdd.pth    # Trained model (80% accuracy)
├── blockchain_demo.py       # Blockchain demo
├── wallet_connect.py        # Petra wallet connection
└── demo_traffic.json        # Demo network data
```

## How to Run

### Main App (GNN + Blockchain)
```bash
streamlit run apps/streamlit_app.py
```

### Train Model
```bash
python train_nslkdd.py
```

### Test Blockchain
```bash
python blockchain_demo.py
```

### Connect Wallet
```bash
python wallet_connect.py
```

## Features

✅ **GNN Detection** - Graph Neural Network for threat detection
✅ **Blockchain Integration** - Aptos blockchain for permanent records
✅ **Real Firewall Blocking** - Actual security enforcement
✅ **3D Visualization** - Beautiful mycelium network display
✅ **80% Accuracy** - Trained on NSL-KDD dataset
✅ **Petra Wallet** - Connect your Aptos wallet
✅ **Smart Contracts** - Written in Move language

## Clean & Production Ready!
