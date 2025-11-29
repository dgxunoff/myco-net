"""
Petra Wallet Connection for MycoShield
"""

try:
    from aptos_sdk.account import Account
    from aptos_sdk.client import RestClient
    APTOS_AVAILABLE = True
except ImportError:
    try:
        from aptos_sdk.account import Account
        from aptos_sdk.async_client import RestClient
        APTOS_AVAILABLE = True
    except ImportError:
        APTOS_AVAILABLE = False
        print("Aptos SDK not available. Install with: pip install aptos-sdk")
import json
import os

class PetraWalletConnector:
    """Connect to Petra wallet and manage Aptos transactions"""
    
    def __init__(self, network="testnet"):
        self.network = network
        self.endpoints = {
            "testnet": "https://fullnode.testnet.aptoslabs.com/v1",
            "mainnet": "https://fullnode.mainnet.aptoslabs.com/v1",
            "devnet": "https://fullnode.devnet.aptoslabs.com/v1"
        }
        self.client = RestClient(self.endpoints[network])
        self.account = None
        self.wallet_address = None
        
    def connect_with_private_key(self, private_key_hex):
        """Connect using private key from Petra wallet"""
        try:
            if private_key_hex.startswith("0x"):
                private_key_hex = private_key_hex[2:]
            
            self.account = Account.load_key(private_key_hex)
            self.wallet_address = str(self.account.address())
            
            print(f"[OK] Connected to Petra Wallet!")
            print(f"Address: {self.wallet_address}")
            print(f"Network: {self.network}")
            
            return self.wallet_address
        except Exception as e:
            print(f"[ERROR] Connection failed: {e}")
            return None
    
    async def get_balance(self):
        """Get APT balance"""
        if not self.account:
            print("[ERROR] Wallet not connected")
            return 0
        
        try:
            balance = await self.client.account_balance(self.account.address())
            apt_balance = balance / 100000000
            print(f"Balance: {apt_balance} APT")
            return apt_balance
        except Exception as e:
            print(f"[ERROR] Failed to get balance: {e}")
            return 0
    
    async def get_account_info(self):
        """Get account information"""
        if not self.account:
            print("[ERROR] Wallet not connected")
            return None
        
        try:
            info = await self.client.account(self.account.address())
            print(f"Account Info:")
            print(f"   Sequence Number: {info['sequence_number']}")
            print(f"   Authentication Key: {info['authentication_key']}")
            return info
        except Exception as e:
            print(f"[ERROR] Failed to get account info: {e}")
            return None
    
    def save_connection(self, filename="wallet_config.json"):
        """Save wallet configuration"""
        if not self.wallet_address:
            print("[ERROR] No wallet connected")
            return False
        
        config = {
            "wallet_address": self.wallet_address,
            "network": self.network
        }
        
        with open(filename, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"[OK] Configuration saved to {filename}")
        return True
    
    def load_connection(self, filename="wallet_config.json"):
        """Load wallet configuration"""
        if not os.path.exists(filename):
            print(f"[ERROR] Configuration file not found: {filename}")
            return None
        
        with open(filename, 'r') as f:
            config = json.load(f)
        
        print(f"Loaded configuration:")
        print(f"   Address: {config['wallet_address']}")
        print(f"   Network: {config['network']}")
        return config

async def interactive_connect():
    """Interactive wallet connection"""
    print("=" * 60)
    print("MycoShield - Petra Wallet Connection")
    print("=" * 60)
    print()
    
    print("Select Network:")
    print("1. Testnet (recommended for testing)")
    print("2. Mainnet (production)")
    print("3. Devnet (development)")
    
    network_choice = input("\nEnter choice (1-3): ").strip()
    network_map = {"1": "testnet", "2": "mainnet", "3": "devnet"}
    network = network_map.get(network_choice, "testnet")
    
    print(f"\nSelected network: {network}")
    print()
    
    connector = PetraWalletConnector(network=network)
    
    print("=" * 60)
    print("How to get your Private Key from Petra Wallet:")
    print("=" * 60)
    print("1. Open Petra Wallet extension in Chrome")
    print("2. Click on Settings (gear icon)")
    print("3. Click on 'Manage Account'")
    print("4. Click on 'Show Private Key'")
    print("5. Enter your password")
    print("6. Copy the private key")
    print()
    print("SECURITY WARNING:")
    print("   - Never share your private key with anyone")
    print("   - This is for testing/demo purposes only")
    print("   - Use a test wallet, not your main wallet")
    print("=" * 60)
    print()
    
    private_key = input("Enter your Petra wallet private key: ").strip()
    
    print("\nConnecting to wallet...")
    address = connector.connect_with_private_key(private_key)
    
    if address:
        print("\n" + "=" * 60)
        await connector.get_balance()
        await connector.get_account_info()
        print("=" * 60)
        
        save = input("\nSave configuration? (y/n): ").strip().lower()
        if save == 'y':
            connector.save_connection()
        
        return connector
    else:
        print("\n[ERROR] Failed to connect wallet")
        return None

if __name__ == "__main__":
    import asyncio
    
    async def main():
        connector = await interactive_connect()
        
        if connector:
            print("\n[OK] Wallet connected successfully!")
            print("\nYou can now use this wallet with MycoShield blockchain features.")
            print("\nNext steps:")
            print("1. Run: python blockchain_demo.py")
            print("2. Or use: mycoshield-blockchain")
    
    asyncio.run(main())
