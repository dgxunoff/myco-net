"""Fund and initialize Aptos account on testnet"""
import os
import subprocess
from dotenv import load_dotenv

load_dotenv()

def fund_account():
    """Fund account using faucet and initialize profile"""
    
    # Get private key from .env
    private_key = os.getenv("APTOS_PRIVATE_KEY", "")
    if not private_key:
        print("ERROR: APTOS_PRIVATE_KEY not found in .env")
        return False
    
    # Remove prefix if present
    if private_key.startswith("ed25519-priv-"):
        private_key = private_key.replace("ed25519-priv-", "")
    
    wallet_address = "0x84226fc4b809a744f0195c0d63d51e51e96e85881f6cd26e1102cfe758ce20cb"
    
    print(f"Wallet Address: {wallet_address}")
    print(f"Private Key: {private_key[:10]}...{private_key[-10:]}")
    
    # Step 1: Initialize account profile
    print("\n[1/3] Initializing account profile...")
    try:
        result = subprocess.run([
            "aptos", "init",
            "--network", "testnet",
            "--private-key", private_key,
            "--skip-faucet",
            "--assume-yes"
        ], capture_output=True, text=True, cwd=os.path.dirname(__file__))
        
        print(result.stdout)
        if result.returncode != 0:
            print(f"ERROR: {result.stderr}")
            return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False
    
    # Step 2: Fund account from faucet
    print("\n[2/3] Funding account from testnet faucet...")
    try:
        result = subprocess.run([
            "aptos", "account", "fund-with-faucet",
            "--account", wallet_address,
            "--amount", "100000000"  # 1 APT
        ], capture_output=True, text=True, cwd=os.path.dirname(__file__))
        
        print(result.stdout)
        if result.returncode != 0:
            print(f"WARNING: {result.stderr}")
            print("Account may already be funded or faucet unavailable")
    except Exception as e:
        print(f"WARNING: {e}")
    
    # Step 3: Check balance
    print("\n[3/3] Checking account balance...")
    try:
        result = subprocess.run([
            "aptos", "account", "balance",
            "--account", wallet_address
        ], capture_output=True, text=True, cwd=os.path.dirname(__file__))
        
        print(result.stdout)
        if result.returncode != 0:
            print(f"ERROR: {result.stderr}")
            return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False
    
    print("\nAccount initialized successfully!")
    print(f"You can now deploy contracts with: python deploy_contracts.py")
    return True

if __name__ == "__main__":
    fund_account()
