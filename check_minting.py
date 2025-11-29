"""
Check if MYCO Token Minting is Working

This script verifies:
1. Contract is deployed
2. Tokens are minted
3. Balance is updated
4. Reputation is tracked
"""

import subprocess
import json
import os
from dotenv import load_dotenv

load_dotenv()

def check_myco_balance():
    """Check MYCO token balance"""
    print("💰 Checking MYCO Token Balance...")
    print("=" * 60)
    
    result = subprocess.run(
        ["aptos", "account", "list", "--account", "default"],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print("❌ Could not fetch account info")
        return
    
    try:
        data = json.loads(result.stdout)
        
        # Look for MYCO tokens in resources
        myco_found = False
        for resource in data.get("Result", []):
            if "MycoReward" in str(resource) or "myco_reward" in str(resource):
                print("✅ MYCO Token Found!")
                print(f"📊 Resource: {resource}")
                myco_found = True
        
        if not myco_found:
            print("⚠️  MYCO Token not found in wallet")
            print("   Contract may not be deployed yet")
    except:
        print("❌ Could not parse account data")
    
    print()

def check_security_node_stats():
    """Check security node reputation and stats"""
    print("🔐 Checking Security Node Stats...")
    print("=" * 60)
    
    # Get wallet address
    result = subprocess.run(
        ["aptos", "config", "show-profiles"],
        capture_output=True,
        text=True
    )
    
    if "default" not in result.stdout:
        print("❌ Default profile not found")
        return
    
    # Try to read SecurityNode resource
    result = subprocess.run(
        [
            "aptos", "move", "view",
            "--function-id", "default::myco_reward::get_node_stats",
            "--args", "address:default"
        ],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✅ Security Node Stats Retrieved!")
        print(result.stdout)
        
        # Parse stats
        try:
            data = json.loads(result.stdout)
            reputation = data[0]
            threats_detected = data[1]
            total_rewards = data[2]
            false_positives = data[3]
            
            print(f"\n📊 Your Stats:")
            print(f"   Reputation: {reputation}/100")
            print(f"   Threats Detected: {threats_detected}")
            print(f"   Total Rewards: {total_rewards / 100000000:.2f} MYCO")
            print(f"   False Positives: {false_positives}")
        except:
            pass
    else:
        print("⚠️  Could not fetch stats")
        print("   Contract may not be deployed yet")
    
    print()

def check_reward_pool():
    """Check global reward pool stats"""
    print("🏦 Checking Reward Pool Stats...")
    print("=" * 60)
    
    result = subprocess.run(
        [
            "aptos", "move", "view",
            "--function-id", "default::myco_reward::get_pool_stats",
            "--args", "address:default"
        ],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✅ Reward Pool Stats Retrieved!")
        print(result.stdout)
        
        try:
            data = json.loads(result.stdout)
            total_minted = data[0]
            total_distributed = data[1]
            base_reward = data[2]
            
            print(f"\n📊 Pool Stats:")
            print(f"   Total Minted: {total_minted / 100000000:.2f} MYCO")
            print(f"   Total Distributed: {total_distributed / 100000000:.2f} MYCO")
            print(f"   Base Reward: {base_reward / 100000000:.2f} MYCO")
        except:
            pass
    else:
        print("⚠️  Could not fetch pool stats")
        print("   Contract may not be deployed yet")
    
    print()

def check_recent_transactions():
    """Check recent transactions for minting events"""
    print("📜 Checking Recent Transactions...")
    print("=" * 60)
    
    result = subprocess.run(
        ["aptos", "account", "list", "--query", "transactions"],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        # Look for reward_threat_detection transactions
        if "reward_threat_detection" in result.stdout:
            print("✅ Minting transactions found!")
            print("   Recent minting activity detected")
        else:
            print("⚠️  No minting transactions found")
            print("   No rewards have been distributed yet")
    else:
        print("⚠️  Could not fetch transactions")
    
    print()

def verify_contract_deployed():
    """Verify if MycoReward contract is deployed"""
    print("🔍 Verifying Contract Deployment...")
    print("=" * 60)
    
    result = subprocess.run(
        ["aptos", "account", "list", "--account", "default"],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        if "myco_reward" in result.stdout.lower() or "mycoreward" in result.stdout.lower():
            print("✅ MycoReward contract is DEPLOYED!")
            print("   Minting is ENABLED")
            return True
        else:
            print("❌ MycoReward contract NOT deployed")
            print("   Minting is DISABLED (using mock mode)")
            print()
            print("📋 To enable minting:")
            print("   1. Run: python deploy_minting_contract.py")
            print("   2. Choose option 1 to deploy")
            print("   3. Run this script again to verify")
            return False
    else:
        print("❌ Could not check deployment status")
        return False
    
    print()

def main():
    print()
    print("🍄 MycoShield - Minting Verification Tool")
    print("=" * 60)
    print()
    
    # Step 1: Check if contract is deployed
    is_deployed = verify_contract_deployed()
    print()
    
    if not is_deployed:
        print("⚠️  Contract not deployed - minting is in MOCK MODE")
        print("   All rewards are simulated, no real tokens minted")
        return
    
    # Step 2: Check MYCO balance
    check_myco_balance()
    
    # Step 3: Check security node stats
    check_security_node_stats()
    
    # Step 4: Check reward pool
    check_reward_pool()
    
    # Step 5: Check recent transactions
    check_recent_transactions()
    
    # Summary
    print("=" * 60)
    print("✅ VERIFICATION COMPLETE")
    print("=" * 60)
    print()
    print("📊 Summary:")
    print("   - If you see MYCO tokens: Minting is WORKING ✅")
    print("   - If stats show > 0 rewards: Minting is ACTIVE ✅")
    print("   - If no MYCO found: Contract not deployed or no rewards yet ⚠️")
    print()
    print("🔗 View on Aptos Explorer:")
    print("   https://explorer.aptoslabs.com/account/<YOUR_ADDRESS>?network=testnet")
    print()

if __name__ == "__main__":
    main()
