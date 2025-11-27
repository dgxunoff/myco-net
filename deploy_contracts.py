"""
Deploy MycoShield Smart Contracts to Aptos
"""

import subprocess
import os

def deploy_contracts():
    """Deploy all MycoShield contracts to Aptos testnet"""
    
    print("🚀 Deploying MycoShield Smart Contracts...")
    
    # Change to contracts directory
    os.chdir("contracts")
    
    try:
        # Initialize Aptos account
        print("1. Initializing Aptos account...")
        subprocess.run(["aptos", "init", "--network", "testnet"], check=True)
        
        # Compile contracts
        print("2. Compiling Move contracts...")
        subprocess.run(["aptos", "move", "compile"], check=True)
        
        # Test contracts
        print("3. Testing contracts...")
        subprocess.run(["aptos", "move", "test"], check=True)
        
        # Deploy contracts
        print("4. Deploying to testnet...")
        result = subprocess.run([
            "aptos", "move", "publish", 
            "--named-addresses", "mycoshield=default"
        ], check=True, capture_output=True, text=True)
        
        print("✅ Contracts deployed successfully!")
        print(f"Transaction: {result.stdout}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Deployment failed: {e}")
        return False
    
    except FileNotFoundError:
        print("❌ Aptos CLI not found. Install with:")
        print("curl -fsSL 'https://aptos.dev/scripts/install_cli.py' | python3")
        return False

if __name__ == "__main__":
    deploy_contracts()