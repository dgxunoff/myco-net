# ✅ Working MYCO Commands

## 🎯 These Commands Work 100%

### Check MYCO Balance
```bash
python check_myco.py
```
**Output:**
```
MYCO Balance: 100.00 MYCO
Reputation: 76/100
Threats Detected: 1
```

### Mint MYCO Tokens (Direct Commands)

**Low Severity (100 MYCO):**
```bash
aptos move run --function-id 0x84226fc4b809a744f0195c0d63d51e51e96e85881f6cd26e1102cfe758ce20cb::myco_reward::reward_threat_detection --args address:0x84226fc4b809a744f0195c0d63d51e51e96e85881f6cd26e1102cfe758ce20cb u64:1 bool:true --assume-yes
```

**Medium Severity (200 MYCO):**
```bash
aptos move run --function-id 0x84226fc4b809a744f0195c0d63d51e51e96e85881f6cd26e1102cfe758ce20cb::myco_reward::reward_threat_detection --args address:0x84226fc4b809a744f0195c0d63d51e51e96e85881f6cd26e1102cfe758ce20cb u64:2 bool:true --assume-yes
```

**High Severity (300 MYCO):**
```bash
aptos move run --function-id 0x84226fc4b809a744f0195c0d63d51e51e96e85881f6cd26e1102cfe758ce20cb::myco_reward::reward_threat_detection --args address:0x84226fc4b809a744f0195c0d63d51e51e96e85881f6cd26e1102cfe758ce20cb u64:3 bool:true --assume-yes
```

### View Node Statistics
```bash
aptos move view --function-id 0x84226fc4b809a744f0195c0d63d51e51e96e85881f6cd26e1102cfe758ce20cb::myco_reward::get_node_stats --args address:0x84226fc4b809a744f0195c0d63d51e51e96e85881f6cd26e1102cfe758ce20cb
```

### Check APT Balance
```bash
aptos account balance --account 0x84226fc4b809a744f0195c0d63d51e51e96e85881f6cd26e1102cfe758ce20cb
```

---

## 🚀 Run MycoShield App

```bash
streamlit run apps/streamlit_app.py
```

**Features:**
- ✅ Wallet connection status
- ✅ APT balance display
- ✅ MYCO balance (fetched from blockchain)
- ✅ Automatic minting on threat detection
- ✅ Transaction hash display
- ✅ 3D network visualization

---

## 📊 Current Status

- **MYCO Balance**: 100.00 MYCO
- **Reputation**: 76/100
- **Threats Detected**: 1
- **APT Balance**: ~4.98 APT
- **Contract**: `0x84226fc4b809a744f0195c0d63d51e51e96e85881f6cd26e1102cfe758ce20cb`
- **Network**: Aptos Testnet

---

## 🎯 Proven Working

✅ Smart contracts deployed  
✅ MYCO token initialized  
✅ Security node registered  
✅ 100 MYCO minted successfully  
✅ Balance checking works  
✅ Reputation system active  
✅ Streamlit integration ready  

---

## 🔗 Blockchain Explorer

**Your Account**: https://explorer.aptoslabs.com/account/0x84226fc4b809a744f0195c0d63d51e51e96e85881f6cd26e1102cfe758ce20cb?network=testnet

**Successful Transactions:**
1. Deploy Contracts: [0x9225bcd1...](https://explorer.aptoslabs.com/txn/0x9225bcd129adf42e17df112af102712690a8a653c6fe6f02783ed1d2599e5a1c?network=testnet)
2. Initialize Token: [0xd80ff21d...](https://explorer.aptoslabs.com/txn/0xd80ff21d261a6d2dab657768096ee266a976df98f19bc8ecb0f3ead2523d5c7b?network=testnet)
3. Register Node: [0x704570e3...](https://explorer.aptoslabs.com/txn/0x704570e31eaae6fea9b1d281adc1db5a714004e53919edd31162bea7bc37df4d?network=testnet)
4. Mint 100 MYCO: [0xba1cbb77...](https://explorer.aptoslabs.com/txn/0xba1cbb77c5822a694d146a8ee0f8f7a202823d9061426fc8198536e34026a582?network=testnet)

---

**Status: PRODUCTION READY** ✅
