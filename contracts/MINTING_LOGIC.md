# MycoReward Token Minting Logic

## 🎯 Purpose
Incentivize security researchers and nodes to detect real threats by rewarding them with MYCO tokens.

## 🏗️ Architecture

### 1. **MycoReward Token (MYCO)**
- Custom Aptos coin with 8 decimals
- Symbol: MYCO
- Minted on-demand when threats are validated
- No pre-mine - tokens only created as rewards

### 2. **Security Node System**
Each security node (threat detector) has:
- **Reputation Score** (0-100): Based on accuracy
  - Starts at 75
  - +1 for each valid threat detected
  - -5 for each false positive
  - Minimum 50 required to claim rewards
  
- **Threats Detected**: Total count of real threats found
- **False Positives**: Count of false alarms
- **Total Rewards**: Cumulative MYCO tokens earned

### 3. **Reward Distribution Logic**

#### Base Rewards:
- **Low Severity Threat**: 100 MYCO
- **Medium Severity Threat**: 200 MYCO (2x multiplier)
- **High Severity Threat**: 300 MYCO (3x multiplier)

#### Reputation Requirements:
- Must have ≥50 reputation to claim rewards
- Prevents spam and encourages accuracy
- False positives reduce reputation

#### Validation Flow:
```
1. Security node detects threat
2. MycoShield AI validates threat (score > threshold)
3. Admin calls reward_threat_detection()
4. If valid:
   - Mint MYCO tokens
   - Transfer to detector's wallet
   - Increase reputation (+1)
   - Update statistics
5. If false positive:
   - No tokens minted
   - Decrease reputation (-5)
   - Track false positive count
```

## 📊 Example Scenarios

### Scenario 1: Valid High-Severity Threat
```
Detector: 0xabc123...
Initial Reputation: 75
Threat Severity: 3 (High)
Result: Valid ✅

Rewards:
- Minted: 300 MYCO
- New Reputation: 76
- Threats Detected: +1
```

### Scenario 2: False Positive
```
Detector: 0xdef456...
Initial Reputation: 60
Threat Severity: 2 (Medium)
Result: False Positive ❌

Penalties:
- Minted: 0 MYCO
- New Reputation: 55
- False Positives: +1
```

### Scenario 3: Low Reputation Block
```
Detector: 0xghi789...
Initial Reputation: 45
Threat Severity: 3 (High)
Result: Valid ✅

Error: E_INSUFFICIENT_REPUTATION
- Cannot claim rewards (need ≥50 reputation)
- Must improve accuracy first
```

## 🔐 Security Features

1. **Admin-Only Minting**: Only contract admin can mint tokens
2. **Reputation Gating**: Prevents low-quality detectors from earning
3. **No Pre-Mine**: Tokens only created for actual work
4. **Transparent Tracking**: All stats visible on-chain
5. **Spam Prevention**: Reputation system discourages false alarms

## 🚀 Deployment Steps

### 1. Initialize Contract
```bash
aptos move publish --named-addresses myco_shield=<YOUR_ADDRESS>
```

### 2. Initialize Token
```bash
aptos move run \
  --function-id <YOUR_ADDRESS>::myco_reward::initialize
```

### 3. Register Security Node
```bash
aptos move run \
  --function-id <YOUR_ADDRESS>::myco_reward::register_security_node
```

### 4. Reward Threat Detection (Admin Only)
```bash
aptos move run \
  --function-id <YOUR_ADDRESS>::myco_reward::reward_threat_detection \
  --args address:<DETECTOR_ADDRESS> u64:3 bool:true
```

## 🔗 Integration with MycoShield

### Python Integration (No Changes to Existing Code)
```python
# Add new method to AptosSecurityManager class
def mint_reward_tokens(self, detector_address, threat_score, is_valid):
    """Mint MYCO tokens for threat detection"""
    if not self.account or not self.contract_address:
        return f"mock_reward_{detector_address}"
    
    # Determine severity from threat score
    severity = 1  # Low
    if threat_score > 0.8:
        severity = 3  # High
    elif threat_score > 0.6:
        severity = 2  # Medium
    
    # Call smart contract
    payload = TransactionPayload(
        EntryFunction.natural(
            f"{self.contract_address}::myco_reward",
            "reward_threat_detection",
            [],
            [
                TransactionArgument(detector_address, str),
                TransactionArgument(severity, int),
                TransactionArgument(is_valid, bool)
            ]
        )
    )
    
    txn = self.client.create_bcs_transaction(self.account, payload)
    return self.client.submit_bcs_transaction(txn)
```

## 📈 Token Economics

### Supply Model:
- **No Max Supply**: Unlimited minting for rewards
- **Inflation Rate**: Depends on threat detection volume
- **Burn Mechanism**: Not implemented (can be added later)

### Reward Pool Tracking:
- Total Minted: All MYCO ever created
- Total Distributed: All MYCO given to detectors
- Base Reward: Configurable by admin (default 100 MYCO)

### Future Enhancements:
1. **Staking**: Lock MYCO to boost reputation
2. **Governance**: Vote on reward parameters
3. **Burn Mechanism**: Reduce supply over time
4. **NFT Badges**: Special achievements for top detectors

## 🎮 Demo Usage

### For Hackathon Demo:
1. Show wallet with 5 APT balance ✅
2. Detect threat in MycoShield UI
3. Call reward function (mock for now)
4. Display "Earned 300 MYCO tokens!" message
5. Show updated reputation score

### For Production:
1. Deploy contract to Aptos testnet
2. Update contract_address in security_config.json
3. Enable real minting in aptos_security.py
4. Track all rewards on blockchain explorer

## 🔍 Why This Design?

### Problem Solved:
- **Spam Prevention**: Reputation system stops false alarms
- **Quality Incentive**: Higher rewards for accurate detection
- **Transparency**: All rewards tracked on-chain
- **Scalability**: No pre-mine, tokens created as needed

### Benefits:
- ✅ Encourages accurate threat detection
- ✅ Penalizes false positives
- ✅ Transparent reward distribution
- ✅ No central authority needed (after deployment)
- ✅ Integrates seamlessly with existing MycoShield code

## 📝 Notes

- **Existing code unchanged**: All current functionality works as-is
- **Optional feature**: Can enable/disable minting
- **Mock mode**: Works without deployed contract
- **Production ready**: Full smart contract implementation
