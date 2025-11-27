"""
Simple Aptos Configuration Setup for MycoShield
"""

import json
import subprocess
import os

def setup_aptos_config():
    """Setup Aptos configuration with CLI"""
    
    print("Setting up Aptos configuration...")
    
    # 1. Initialize Aptos account if not exists
    if not os.path.exists(".aptos"):
        print("1. Initializing Aptos account...")
        try:
            subprocess.run(["aptos", "init", "--network", "testnet"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error initializing Aptos: {e}")
            return False
    
    # 2. Get wallet address
    try:
        result = subprocess.run([
            "aptos", "account", "list", "--query", "balance"
        ], capture_output=True, text=True, check=True)
        
        # Extract address from output
        lines = result.stdout.split('\n')
        wallet_address = None
        for line in lines:
            if "0x" in line:
                wallet_address = line.split()[0]
                break
        
        if not wallet_address:
            print("Could not find wallet address. Please run 'aptos init' manually.")
            return False
            
        print(f"Wallet address: {wallet_address}")
        
    except subprocess.CalledProcessError:
        print("Error getting wallet address. Using default.")
        wallet_address = "0x1"
    
    # 3. Update security_config.json
    try:
        with open("security_config.json", "r") as f:
            config = json.load(f)
        
        config["aptos"]["wallet"]["address"] = wallet_address
        config["aptos"]["contracts"]["threat_intelligence"] = wallet_address
        config["aptos"]["contracts"]["security_incidents"] = wallet_address
        config["aptos"]["contracts"]["threat_scoring"] = wallet_address
        config["aptos"]["contracts"]["multi_sig"] = wallet_address
        
        with open("security_config.json", "w") as f:
            json.dump(config, f, indent=2)
        
        print("Configuration updated successfully!")
        print(f"Network: {config['aptos']['network']}")
        print(f"Wallet: {config['aptos']['wallet']['address']}")
        
        return True
        
    except Exception as e:
        print(f"Error updating config: {e}")
        return False

def fund_wallet():
    """Fund wallet from testnet faucet"""
    try:
        print("Funding wallet from testnet faucet...")
        subprocess.run([
            "aptos", "account", "fund-with-faucet"
        ], check=True)
        print("Wallet funded successfully!")
        return True
        
    except subprocess.CalledProcessError:
        print("Faucet funding failed")
        return False

def check_balance():
    """Check wallet balance"""
    try:
        result = subprocess.run([
            "aptos", "account", "balance"
        ], capture_output=True, text=True, check=True)
        
        print(f"Wallet balance: {result.stdout.strip()}")
        return result.stdout.strip()
        
    except subprocess.CalledProcessError:
        print("Could not fetch balance")
        return "0 APT"

if __name__ == "__main__":
    # Setup configuration
    if setup_aptos_config():
        # Fund wallet if needed
        balance = check_balance()
        if "0" in balance or not balance:
            fund_wallet()
            check_balance()
        
        print("\nAptos setup completed!")
        print("You can now run: python blockchain_demo.py")
    else:
        print("Setup failed. Please check Aptos CLI installation.")