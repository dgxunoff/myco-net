"""
Deploy MycoReward Minting Contract to Aptos Testnet

This script deploys the MYCO token minting contract without affecting existing code.
Run this ONLY when you want to enable real token minting.
"""

import os
import subprocess
from dotenv import load_dotenv

load_dotenv()

def deploy_contract():
    """Deploy MycoReward contract to Aptos testnet"""
    
    print("🚀 Deploying MycoReward Minting Contract...")
    print("=" * 60)
    
    # Get wallet address from .env
    private_key = os.getenv('APTOS_PRIVATE_KEY')
    if not private_key:
        print("❌ Error: APTOS_PRIVATE_KEY not found in .env file")
        return False
    
    # Get wallet address
    result = subprocess.run(
        ["aptos", "account", "list", "--account", "default"],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print("❌ Error: Could not get wallet address")
        return False
    
    print("✅ Wallet connected")
    print()
    
    # Step 1: Compile contract
    print("📦 Step 1: Compiling Move contract...")
    compile_result = subprocess.run(
        ["aptos", "move", "compile", "--package-dir", "contracts"],
        capture_output=True,
        text=True
    )
    
    if compile_result.returncode != 0:
        print(f"❌ Compilation failed:\n{compile_result.stderr}")
        return False
    
    print("✅ Contract compiled successfully")
    print()
    
    # Step 2: Publish contract
    print("🌐 Step 2: Publishing to Aptos testnet...")
    print("⚠️  This will cost gas fees (APT)")
    
    confirm = input("Continue? (yes/no): ")
    if confirm.lower() != 'yes':
        print("❌ Deployment cancelled")
        return False
    
    publish_result = subprocess.run(
        [
            "aptos", "move", "publish",
            "--package-dir", "contracts",
            "--named-addresses", "myco_shield=default",
            "--assume-yes"
        ],
        capture_output=True,
        text=True
    )
    
    if publish_result.returncode != 0:
        print(f"❌ Publishing failed:\n{publish_result.stderr}")
        return False
    
    print("✅ Contract published to testnet")
    print()
    
    # Step 3: Initialize token
    print("🎯 Step 3: Initializing MycoReward token...")
    
    init_result = subprocess.run(
        [
            "aptos", "move", "run",
            "--function-id", "default::myco_reward::initialize",
            "--assume-yes"
        ],
        capture_output=True,
        text=True
    )
    
    if init_result.returncode != 0:
        print(f"❌ Initialization failed:\n{init_result.stderr}")
        return False
    
    print("✅ MycoReward token initialized")
    print()
    
    # Step 4: Register as security node
    print("🔐 Step 4: Registering as security node...")
    
    register_result = subprocess.run(
        [
            "aptos", "move", "run",
            "--function-id", "default::myco_reward::register_security_node",
            "--assume-yes"
        ],
        capture_output=True,
        text=True
    )
    
    if register_result.returncode != 0:
        print(f"❌ Registration failed:\n{register_result.stderr}")
        return False
    
    print("✅ Registered as security node")
    print()
    
    # Success summary
    print("=" * 60)
    print("🎉 DEPLOYMENT SUCCESSFUL!")
    print("=" * 60)
    print()
    print("📋 Next Steps:")
    print("1. Update security_config.json with contract address")
    print("2. Enable minting in aptos_security.py")
    print("3. Test reward distribution")
    print()
    print("🔗 View on Explorer:")
    print("https://explorer.aptoslabs.com/account/<YOUR_ADDRESS>?network=testnet")
    print()
    
    return True

def test_minting():
    """Test minting functionality (optional)"""
    
    print("🧪 Testing Token Minting...")
    print("=" * 60)
    
    # Get your wallet address
    result = subprocess.run(
        ["aptos", "account", "list"],
        capture_output=True,
        text=True
    )
    
    print("This will mint 300 MYCO tokens as a test reward")
    confirm = input("Continue? (yes/no): ")
    
    if confirm.lower() != 'yes':
        print("❌ Test cancelled")
        return
    
    # Mint test reward
    mint_result = subprocess.run(
        [
            "aptos", "move", "run",
            "--function-id", "default::myco_reward::reward_threat_detection",
            "--args", "address:default", "u64:3", "bool:true",
            "--assume-yes"
        ],
        capture_output=True,
        text=True
    )
    
    if mint_result.returncode != 0:
        print(f"❌ Minting failed:\n{mint_result.stderr}")
        return
    
    print("✅ Test minting successful!")
    print("💰 You should now have 300 MYCO tokens")
    print()

if __name__ == "__main__":
    print()
    print("🍄 MycoShield - Token Minting Contract Deployment")
    print("=" * 60)
    print()
    print("⚠️  WARNING: This will deploy a real smart contract")
    print("⚠️  Make sure you have enough APT for gas fees")
    print()
    
    choice = input("What would you like to do?\n1. Deploy contract\n2. Test minting (after deployment)\n3. Exit\n\nChoice: ")
    
    if choice == "1":
        if deploy_contract():
            print("\n✅ Deployment complete!")
            test_choice = input("\nWould you like to test minting now? (yes/no): ")
            if test_choice.lower() == 'yes':
                test_minting()
    elif choice == "2":
        test_minting()
    else:
        print("👋 Goodbye!")
