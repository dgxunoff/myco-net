"""
Test Aptos Configuration
"""

import json
from mycoshield import AptosSecurityManager

def test_config():
    """Test Aptos configuration"""
    
    print("Testing Aptos configuration...")
    
    # Load config
    with open("security_config.json", "r") as f:
        config = json.load(f)
    
    aptos_config = config.get("aptos", {})
    
    print(f"Network: {aptos_config.get('network')}")
    print(f"Wallet: {aptos_config.get('wallet', {}).get('address')}")
    print(f"Endpoint: {aptos_config.get('endpoints', {}).get('testnet')}")
    
    # Test Aptos manager
    aptos = AptosSecurityManager()
    
    # Test wallet connection
    wallet = aptos.connect_wallet()
    print(f"Connected wallet: {wallet}")
    
    # Test balance
    balance = aptos.get_balance()
    print(f"Balance: {balance}")
    
    # Test threat submission (mock)
    threat_tx = aptos.submit_threat_data("192.168.1.100", 0.85, "malware")
    print(f"Threat submission: {threat_tx}")
    
    print("Configuration test completed!")

if __name__ == "__main__":
    test_config()