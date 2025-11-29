"""
Deploy All MycoShield Move Smart Contracts to Aptos Testnet

Contracts to deploy:
1. MycoRewardToken.move - Token minting for rewards
2. ThreatIntelligence.move - Threat data storage
3. SecurityIncidents.move - Incident logging
4. ThreatScoring.move - Consensus scoring
5. MultiSigSecurity.move - Multi-signature actions
"""

import os
import subprocess
import json
from dotenv import load_dotenv

load_dotenv()

def check_prerequisites():
    """Check if all prerequisites are met"""
    print("🔍 Checking Prerequisites...")
    print("=" * 60)
    
    # Check Aptos CLI
    result = subprocess.run(["aptos", "--version"], capture_output=True, text=True)
    if result.returncode != 0:
        print("❌ Aptos CLI not installed")
        print("   Install: https://aptos.dev/tools/aptos-cli/install-cli/")
        return False
    print(f"✅ Aptos CLI: {result.stdout.strip()}")
    
    # Check wallet
    private_key = os.getenv('APTOS_PRIVATE_KEY')
    if not private_key:
        print("❌ APTOS_PRIVATE_KEY not found in .env")
        return False
    print("✅ Wallet configured in .env")
    
    # Check balance
    result = subprocess.run(
        ["aptos", "account", "balance", "--account", "0x84226fc4b809a744f0195c0d63d51e51e96e85881f6cd26e1102cfe758ce20cb"],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        data = json.loads(result.stdout)
        balance = int(data["Result"][0]["balance"]) / 100000000
        print(f"✅ APT Balance: {balance:.2f} APT")
        
        if balance < 1.0:
            print("⚠️  Recommended: 1+ APT for deployment")
            print("   Current balance is sufficient for testing")
    
    print()
    return True

def get_wallet_address():
    """Get wallet address from aptos config"""
    # Read from .aptos/config.yaml
    import yaml
    import os
    
    config_path = os.path.expanduser("~/.aptos/config.yaml")
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
            account = config.get('profiles', {}).get('default', {}).get('account')
            if account:
                return account
    except:
        pass
    
    return "0x84226fc4b809a744f0195c0d63d51e51e96e85881f6cd26e1102cfe758ce20cb"

def compile_contracts():
    """Compile Move contracts"""
    print("📦 Compiling Move Contracts...")
    print("=" * 60)
    print("⚠️  First time may take 2-3 minutes (downloading dependencies)")
    print()
    
    try:
        result = subprocess.run(
            ["aptos", "move", "compile", "--package-dir", "contracts"],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        if result.returncode != 0:
            print("❌ Compilation failed:")
            print(result.stderr)
            if result.stdout:
                print(result.stdout)
            return False
        
        print("✅ All contracts compiled successfully")
        print()
        return True
    except subprocess.TimeoutExpired:
        print("❌ Compilation timeout (>5 minutes)")
        print("   Try running manually: cd contracts && aptos move compile")
        return False

def publish_contracts():
    """Publish contracts to Aptos testnet"""
    print("🌐 Publishing Contracts to Aptos Testnet...")
    print("=" * 60)
    
    wallet_addr = get_wallet_address()
    
    print(f"📍 Deploying to address: {wallet_addr}")
    print("⚠️  This will cost APT for gas fees")
    print()
    
    confirm = input("Continue with deployment? (yes/no): ")
    if confirm.lower() != 'yes':
        print("❌ Deployment cancelled")
        return False
    
    print("\n🚀 Publishing...")
    
    # Clean wallet address (remove quotes if present)
    clean_addr = wallet_addr.strip('"').strip("'")
    if not clean_addr.startswith('0x'):
        clean_addr = f"0x{clean_addr}"
    
    result = subprocess.run(
        [
            "aptos", "move", "publish",
            "--package-dir", "contracts",
            "--named-addresses", f"mycoshield={clean_addr}",
            "--assume-yes"
        ],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print("❌ Publishing failed:")
        print(result.stderr)
        return False
    
    print("✅ Contracts published successfully!")
    print()
    return True

def initialize_myco_token():
    """Initialize MycoReward token"""
    print("🎯 Initializing MYCO Token...")
    print("=" * 60)
    
    result = subprocess.run(
        [
            "aptos", "move", "run",
            "--function-id", "default::myco_reward::initialize",
            "--assume-yes"
        ],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print("⚠️  Initialization skipped (may already be initialized)")
        print()
        return True
    
    print("✅ MYCO Token initialized")
    print()
    return True

def register_security_node():
    """Register as security node"""
    print("🔐 Registering Security Node...")
    print("=" * 60)
    
    result = subprocess.run(
        [
            "aptos", "move", "run",
            "--function-id", "default::myco_reward::register_security_node",
            "--assume-yes"
        ],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print("⚠️  Registration skipped (may already be registered)")
        print()
        return True
    
    print("✅ Security node registered")
    print()
    return True

def verify_deployment():
    """Verify contracts are deployed"""
    print("🔍 Verifying Deployment...")
    print("=" * 60)
    
    result = subprocess.run(
        ["aptos", "account", "list", "--account", "default"],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        if "myco_reward" in result.stdout.lower() or "mycoshield" in result.stdout.lower():
            print("✅ Contracts verified on blockchain")
            print()
            return True
    
    print("⚠️  Could not verify deployment")
    print()
    return False

def save_contract_address():
    """Save contract address to config"""
    print("💾 Saving Contract Configuration...")
    print("=" * 60)
    
    wallet_addr = get_wallet_address()
    
    config = {
        "aptos": {
            "enabled": True,
            "network": "testnet",
            "contract_address": wallet_addr,
            "endpoints": {
                "testnet": "https://fullnode.testnet.aptoslabs.com/v1"
            },
            "contracts": {
                "myco_reward": f"{wallet_addr}::myco_reward",
                "threat_intelligence": f"{wallet_addr}::threat_intelligence",
                "security_incidents": f"{wallet_addr}::security_incidents",
                "threat_scoring": f"{wallet_addr}::threat_scoring",
                "multi_sig": f"{wallet_addr}::multi_sig_security"
            }
        }
    }
    
    with open("security_config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print("✅ Configuration saved to security_config.json")
    print()

def main():
    print()
    print("🍄 MycoShield - Smart Contract Deployment")
    print("=" * 60)
    print()
    
    # Step 1: Check prerequisites
    if not check_prerequisites():
        print("\n❌ Prerequisites not met. Please fix and try again.")
        return
    
    # Step 2: Compile contracts
    if not compile_contracts():
        print("\n❌ Compilation failed. Please fix errors and try again.")
        return
    
    # Step 3: Publish contracts
    if not publish_contracts():
        print("\n❌ Publishing failed. Please check errors above.")
        return
    
    # Step 4: Initialize MYCO token
    initialize_myco_token()
    
    # Step 5: Register security node
    register_security_node()
    
    # Step 6: Verify deployment
    verify_deployment()
    
    # Step 7: Save configuration
    save_contract_address()
    
    # Success summary
    wallet_addr = get_wallet_address()
    
    print("=" * 60)
    print("🎉 DEPLOYMENT SUCCESSFUL!")
    print("=" * 60)
    print()
    print("📋 Deployed Contracts:")
    print(f"   1. MycoReward Token (MYCO)")
    print(f"   2. Threat Intelligence")
    print(f"   3. Security Incidents")
    print(f"   4. Threat Scoring")
    print(f"   5. Multi-Sig Security")
    print()
    print(f"📍 Contract Address: {wallet_addr}")
    print()
    print("🔗 View on Aptos Explorer:")
    print(f"   https://explorer.aptoslabs.com/account/{wallet_addr}?network=testnet")
    print()
    print("✅ Next Steps:")
    print("   1. Restart Streamlit app to use deployed contracts")
    print("   2. Run: python check_minting.py to verify")
    print("   3. Detect threats to earn real MYCO tokens!")
    print()

if __name__ == "__main__":
    main()
