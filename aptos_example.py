"""
Example usage of Aptos integration with MycoShield
"""

from mycoshield import AptosSecurityManager, AptosTransactionMonitor, AptosSmartContractInterface
import asyncio

async def main():
    # Initialize Aptos manager
    aptos_manager = AptosSecurityManager()
    
    # Connect wallet (generates new account for demo)
    wallet_address = aptos_manager.connect_wallet()
    print(f"Connected wallet: {wallet_address}")
    
    # Check balance
    balance = aptos_manager.get_balance()
    print(f"Wallet balance: {balance} APT")
    
    # Submit threat data to blockchain
    threat_hash = aptos_manager.submit_threat_data(
        threat_ip="192.168.1.100",
        threat_score=0.85,
        threat_type="malware"
    )
    print(f"Threat submitted: {threat_hash}")
    
    # Query threat intelligence
    threat_data = aptos_manager.query_threat_intelligence("192.168.1.100")
    print(f"Threat data: {threat_data}")
    
    # Smart contract interface
    contract_interface = AptosSmartContractInterface(aptos_manager)
    
    # Create threat database entry
    entry_hash = contract_interface.create_threat_database_entry(
        ip="10.0.0.1",
        score=0.9,
        evidence="Port scan detected"
    )
    print(f"Database entry: {entry_hash}")
    
    # Start transaction monitoring
    monitor = AptosTransactionMonitor(aptos_manager)
    print("Starting transaction monitoring...")
    
    # Monitor for 10 seconds then stop
    monitor_task = asyncio.create_task(monitor.start_monitoring())
    await asyncio.sleep(10)
    monitor.stop_monitoring()
    monitor_task.cancel()
    
    print("Aptos integration demo completed!")

if __name__ == "__main__":
    asyncio.run(main())