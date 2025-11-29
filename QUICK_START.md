# 🚀 MycoShield Quick Start Guide

## ✅ Current Status

**MYCO Token**: LIVE on Aptos Testnet  
**Contract**: `0x84226fc4b809a744f0195c0d63d51e51e96e85881f6cd26e1102cfe758ce20cb`  
**Your Balance**: 100 MYCO (1 threat detected)  
**Reputation**: 76/100

---

## 🎯 Run MycoShield

```bash
# Start the app
streamlit run apps/streamlit_app.py
```

**What happens:**
1. Upload PCAP file or click "Generate Demo Traffic"
2. AI detects threats using Graph Neural Networks
3. MYCO tokens automatically minted to your wallet
4. View balance and transaction hashes in sidebar

---

## 💰 Check MYCO Balance

```bash
python check_myco.py
```

**Output:**
```
MYCO Balance: 100.00 MYCO
Reputation: 76/100
Threats Detected: 1
```

---

## 🔗 Mint MYCO Manually

```bash
# Low severity (100 MYCO)
aptos move run \
  --function-id 0x84226fc4b809a744f0195c0d63d51e51e96e85881f6cd26e1102cfe758ce20cb::myco_reward::reward_threat_detection \
  --args address:0x84226fc4b809a744f0195c0d63d51e51e96e85881f6cd26e1102cfe758ce20cb u64:1 bool:true \
  --assume-yes

# Medium severity (200 MYCO)
aptos move run \
  --function-id 0x84226fc4b809a744f0195c0d63d51e51e96e85881f6cd26e1102cfe758ce20cb::myco_reward::reward_threat_detection \
  --args address:0x84226fc4b809a744f0195c0d63d51e51e96e85881f6cd26e1102cfe758ce20cb u64:2 bool:true \
  --assume-yes

# High severity (300 MYCO)
aptos move run \
  --function-id 0x84226fc4b809a744f0195c0d63d51e51e96e85881f6cd26e1102cfe758ce20cb::myco_reward::reward_threat_detection \
  --args address:0x84226fc4b809a744f0195c0d63d51e51e96e85881f6cd26e1102cfe758ce20cb u64:3 bool:true \
  --assume-yes
```

---

## 📊 View on Blockchain

**Aptos Explorer**: https://explorer.aptoslabs.com/account/0x84226fc4b809a744f0195c0d63d51e51e96e85881f6cd26e1102cfe758ce20cb?network=testnet

**Recent Transactions:**
- Deploy: [0x9225bcd1...](https://explorer.aptoslabs.com/txn/0x9225bcd129adf42e17df112af102712690a8a653c6fe6f02783ed1d2599e5a1c?network=testnet)
- Initialize: [0xd80ff21d...](https://explorer.aptoslabs.com/txn/0xd80ff21d261a6d2dab657768096ee266a976df98f19bc8ecb0f3ead2523d5c7b?network=testnet)
- Register: [0x704570e3...](https://explorer.aptoslabs.com/txn/0x704570e31eaae6fea9b1d281adc1db5a714004e53919edd31162bea7bc37df4d?network=testnet)
- Mint 100 MYCO: [0xba1cbb77...](https://explorer.aptoslabs.com/txn/0xba1cbb77c5822a694d146a8ee0f8f7a202823d9061426fc8198536e34026a582?network=testnet)

---

## 🎪 Demo Flow

### For Hackathons
1. Open Streamlit app
2. Show wallet connected (sidebar)
3. Generate demo traffic
4. Watch 3D mycelium network visualization
5. See threats detected (red nodes)
6. Show MYCO tokens minted automatically
7. Display transaction hash
8. Open Aptos Explorer to show real blockchain transaction

### Key Talking Points
- "World's first mycelium-inspired cybersecurity on blockchain"
- "AI detects threats, blockchain rewards security researchers"
- "100/200/300 MYCO based on threat severity"
- "Permanent, tamper-proof security audit trail"
- "Decentralized threat intelligence sharing"

---

## 🏆 What Makes This Special

✅ **Real AI**: Graph Neural Networks trained on NSL-KDD dataset  
✅ **Real Blockchain**: Actual smart contracts on Aptos testnet  
✅ **Real Tokens**: MYCO tokens minted on-chain  
✅ **Real Integration**: Python app calls blockchain in real-time  
✅ **Beautiful UI**: 3D visualization of network threats  

---

## 📁 Key Files

- `apps/streamlit_app.py` - Main UI with blockchain integration
- `mycoshield/aptos_security.py` - Blockchain integration layer
- `contracts/sources/MycoRewardToken.move` - MYCO token smart contract
- `check_myco.py` - Quick balance checker
- `.env` - Contains APTOS_PRIVATE_KEY

---

## 🐛 Troubleshooting

**Balance shows 0 in app?**
- Restart Streamlit app to refresh balance

**Transaction failed?**
- Check APT balance: `aptos account balance --account 0x84226fc4b809a744f0195c0d63d51e51e96e85881f6cd26e1102cfe758ce20cb`
- Need more APT? Visit https://aptos.dev/network/faucet

**Wallet not connected?**
- Check `.env` file has APTOS_PRIVATE_KEY

---

## 🎓 Documentation

- `README.md` - Full project overview
- `MYCO_APTOS_EXPLAINED.md` - Token architecture
- `DEPLOYMENT_SUCCESS.md` - Complete deployment details

---

**Built with 🍄 by MycoShield**  
**Powered by Aptos Blockchain 🔗**
