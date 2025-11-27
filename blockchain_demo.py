"""
Blockchain Integration Demo for MycoShield
"""

from mycoshield import BlockchainSecurityOrchestrator
import asyncio

async def main():
    print("MycoShield Blockchain Security Demo")
    
    # Initialize blockchain orchestrator
    orchestrator = BlockchainSecurityOrchestrator()
    
    # Initialize blockchain security system
    init_result = orchestrator.initialize_blockchain_security()
    print(f"Blockchain initialized: {init_result}")
    
    # Demo security event
    security_event = {
        "ip": "192.168.1.100",
        "ip_address": "192.168.1.100",
        "signature": "malware_hash_abc123",
        "type": "malware",
        "evidence": "malware detected in network traffic",
        "action_taken": "ISOLATED",
        "threat_score": 0.85,
        "timestamp": "2024-01-01T12:00:00"
    }
    
    # Process through blockchain pipeline
    result = orchestrator.process_security_event(security_event)
    print(f"Blockchain processing result: {result}")
    
    # Demo threat intelligence storage
    threat_signatures = [
        {"ip": "10.0.0.1", "score": 0.9, "type": "port_scan"},
        {"ip": "10.0.0.2", "score": 0.7, "type": "suspicious_traffic"},
        {"ip": "10.0.0.3", "score": 0.95, "type": "malware"}
    ]
    
    db_result = orchestrator.threat_intel.create_immutable_threat_db(threat_signatures)
    print(f"Threat database created: {len(db_result)} entries")
    
    # Demo validator network
    validators = ["0x123", "0x456", "0x789"]
    validator_result = orchestrator.scoring_system.implement_validator_network(validators)
    print(f"Validator network: {validator_result}")
    
    # Demo reputation system
    performance_metrics = {
        "accuracy": 0.92,
        "uptime": 0.98,
        "detections": 150,
        "rewards": 500
    }
    
    reputation_result = orchestrator.scoring_system.create_reputation_system(
        "0x123", performance_metrics
    )
    print(f"Reputation system: {reputation_result}")
    
    print("Blockchain demo completed!")

if __name__ == "__main__":
    asyncio.run(main())