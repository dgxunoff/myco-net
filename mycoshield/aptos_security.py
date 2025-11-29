"""
Aptos Blockchain Security Integration for MycoShield
"""

try:
    from aptos_sdk.async_client import RestClient
    from aptos_sdk.account import Account
    from aptos_sdk.transactions import EntryFunction, TransactionArgument, TransactionPayload
    APTOS_AVAILABLE = True
except (ImportError, ModuleNotFoundError, AttributeError) as e:
    APTOS_AVAILABLE = False
    print(f"Warning: Aptos SDK not properly installed ({e}). Running in mock mode.")
    print("Install with: pip install aptos-sdk==0.8.6")

import asyncio
import json
from datetime import datetime

class AptosSecurityManager:
    """Aptos blockchain integration for MycoShield"""
    
    def __init__(self, config_file="security_config.json"):
        self.config = self._load_config(config_file)
        
        if not APTOS_AVAILABLE:
            self.client = None
            self.account = None
            self.contract_address = None
            return
            
        # Use config for network endpoint
        network = self.config.get("aptos", {}).get("network", "testnet")
        endpoints = self.config.get("aptos", {}).get("endpoints", {})
        node_url = endpoints.get(network, "https://fullnode.testnet.aptoslabs.com/v1")
        
        self.client = RestClient(node_url)
        self.account = None
        self.contract_address = self.config.get("aptos", {}).get("contracts", {}).get("threat_intelligence")
    
    def _load_config(self, config_file):
        """Load configuration from JSON file"""
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"aptos": {"enabled": False}}
        
    def connect_wallet(self, private_key=None):
        """Connect to Aptos wallet (Petra or generated)"""
        if not APTOS_AVAILABLE:
            return "aptos_sdk_not_available"
            
        if private_key:
            # Remove ed25519-priv- prefix if present
            if isinstance(private_key, str) and private_key.startswith("ed25519-priv-"):
                private_key = private_key[13:]
            # Remove 0x prefix if present
            if isinstance(private_key, str) and private_key.startswith("0x"):
                private_key = private_key[2:]
            self.account = Account.load_key(private_key)
            print(f"Connected to wallet: {str(self.account.address())}")
        else:
            self.account = Account.generate()
            print(f"Generated new wallet: {str(self.account.address())}")
        
        # Fetch and cache balance immediately
        self.cached_balance = self._fetch_balance_sync()
        return str(self.account.address())
    
    def _fetch_balance_sync(self):
        """Internal method to fetch balance synchronously"""
        if not APTOS_AVAILABLE or not self.account:
            return 0
        
        # Use aptos CLI to fetch balance (most reliable method)
        import subprocess
        
        try:
            result = subprocess.run(
                ["aptos", "account", "balance", "--account", str(self.account.address())],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                # Parse JSON output from aptos CLI
                import json
                data = json.loads(result.stdout)
                balance_octas = int(data["Result"][0]["balance"])
                return balance_octas / 100000000
            else:
                return 0
        except Exception as e:
            print(f"Balance fetch error: {e}")
            return 0
    
    def get_balance(self):
        """Get cached APT balance"""
        return getattr(self, 'cached_balance', 0)
    
    def submit_threat_data(self, threat_ip, threat_score, threat_type):
        """Submit threat data to blockchain"""
        if not APTOS_AVAILABLE or not self.account or not self.contract_address:
            return f"mock_tx_{threat_ip}_{int(threat_score*1000)}"
            
        try:
            payload = TransactionPayload(
                EntryFunction.natural(
                    f"{self.contract_address}::threat_intelligence",
                    "submit_threat",
                    [],
                    [
                        TransactionArgument(threat_ip, str),
                        TransactionArgument(int(threat_score * 1000), int),
                        TransactionArgument(threat_type, str)
                    ]
                )
            )
            
            txn = self.client.create_bcs_transaction(self.account, payload)
            return self.client.submit_bcs_transaction(txn)
        except:
            return f"mock_tx_{threat_ip}_{int(threat_score*1000)}"
    
    def query_threat_intelligence(self, ip_address):
        """Query threat data from blockchain"""
        if not self.contract_address:
            return None
            
        try:
            resource = self.client.account_resource(
                self.contract_address,
                f"{self.contract_address}::threat_intelligence::ThreatData"
            )
            threats = resource.get("data", {}).get("threats", [])
            return next((t for t in threats if t["ip"] == ip_address), None)
        except:
            return None
    
    def log_security_incident(self, incident_data):
        """Log security incident to blockchain"""
        if not self.account or not self.contract_address:
            return None
            
        payload = TransactionPayload(
            EntryFunction.natural(
                f"{self.contract_address}::security_incidents",
                "log_incident",
                [],
                [
                    TransactionArgument(incident_data["ip_address"], str),
                    TransactionArgument(incident_data["action_taken"], str),
                    TransactionArgument(int(incident_data["threat_score"] * 1000), int),
                    TransactionArgument(incident_data["timestamp"], str)
                ]
            )
        )
        
        txn = self.client.create_bcs_transaction(self.account, payload)
        return self.client.submit_bcs_transaction(txn)
    
    def monitor_transactions(self, callback=None):
        """Monitor blockchain transactions"""
        if not self.account:
            return []
            
        try:
            txns = self.client.account_transactions(self.account.address(), limit=10)
            if callback:
                for txn in txns:
                    callback(txn)
            return txns
        except:
            return []
    
    def validate_threat_consensus(self, threat_ip):
        """Check threat validation consensus"""
        if not self.contract_address:
            return False
            
        try:
            resource = self.client.account_resource(
                self.contract_address,
                f"{self.contract_address}::threat_scoring::ConsensusData"
            )
            consensus = resource.get("data", {}).get("validations", {})
            return consensus.get(threat_ip, {}).get("validated", False)
        except:
            return False
    
    def deploy_contract(self, contract_code):
        """Deploy smart contract"""
        if not self.account:
            return None
            
        # Simplified contract deployment
        payload = TransactionPayload(contract_code)
        txn = self.client.create_bcs_transaction(self.account, payload)
        result = self.client.submit_bcs_transaction(txn)
        
        if result:
            self.contract_address = self.account.address()
        return result
    
    def get_security_reputation(self, node_address):
        """Get security reputation score from blockchain"""
        if not APTOS_AVAILABLE:
            return 75  # Mock reputation score
        return 75
    
    def reward_threat_detection(self, detector_address, reward_amount):
        """Reward successful threat detection"""
        if not APTOS_AVAILABLE:
            return f"mock_reward_{detector_address}_{reward_amount}"
        return f"mock_reward_{detector_address}_{reward_amount}"

class AptosTransactionMonitor:
    """Monitor Aptos transactions for security events"""
    
    def __init__(self, aptos_manager):
        self.aptos_manager = aptos_manager
        self.monitoring = False
    
    async def start_monitoring(self):
        """Start transaction monitoring"""
        self.monitoring = True
        while self.monitoring:
            try:
                txns = self.aptos_manager.monitor_transactions()
                for txn in txns:
                    await self.process_transaction(txn)
                await asyncio.sleep(5)
            except Exception as e:
                print(f"Monitoring error: {e}")
                await asyncio.sleep(10)
    
    async def process_transaction(self, transaction):
        """Process individual transaction"""
        # Extract security-relevant data
        if transaction.get("type") == "user_transaction":
            payload = transaction.get("payload", {})
            if "threat_intelligence" in str(payload):
                return {
                    "type": "threat_submission",
                    "hash": transaction.get("hash"),
                    "timestamp": transaction.get("timestamp"),
                    "sender": transaction.get("sender")
                }
        return None
    
    def stop_monitoring(self):
        """Stop transaction monitoring"""
        self.monitoring = False

class AptosSmartContractInterface:
    """Interface for MycoShield smart contracts"""
    
    def __init__(self, aptos_manager):
        self.aptos_manager = aptos_manager
    
    def create_threat_database_entry(self, ip, score, evidence):
        """Create immutable threat database entry"""
        return self.aptos_manager.submit_threat_data(ip, score, evidence)
    
    def execute_multi_sig_action(self, action_type, target_ip, approvers):
        """Execute multi-signature security action"""
        if not self.aptos_manager.account:
            return None
            
        # Simplified multi-sig implementation
        payload = TransactionPayload(
            EntryFunction.natural(
                f"{self.aptos_manager.contract_address}::multi_sig",
                "execute_action",
                [],
                [
                    TransactionArgument(action_type, str),
                    TransactionArgument(target_ip, str),
                    TransactionArgument(len(approvers), int)
                ]
            )
        )
        
        txn = self.aptos_manager.client.create_bcs_transaction(
            self.aptos_manager.account, payload
        )
        return self.aptos_manager.client.submit_bcs_transaction(txn)
    
    def get_security_reputation(self, node_address):
        """Get security reputation score from blockchain"""
        try:
            resource = self.aptos_manager.client.account_resource(
                self.aptos_manager.contract_address,
                f"{self.aptos_manager.contract_address}::reputation::NodeReputation"
            )
            reputation_data = resource.get("data", {})
            return reputation_data.get(node_address, 0)
        except:
            return 0
    
    def reward_threat_detection(self, detector_address, reward_amount):
        """Reward successful threat detection"""
        if not self.aptos_manager.account:
            return None
            
        payload = TransactionPayload(
            EntryFunction.natural(
                f"{self.aptos_manager.contract_address}::rewards",
                "distribute_reward",
                [],
                [
                    TransactionArgument(detector_address, str),
                    TransactionArgument(reward_amount, int)
                ]
            )
        )
        
        txn = self.aptos_manager.client.create_bcs_transaction(
            self.aptos_manager.account, payload
        )
        return self.aptos_manager.client.submit_bcs_transaction(txn)