"""
Test MycoShield Smart Contracts
"""

from mycoshield import AptosSecurityManager
import asyncio

async def test_contracts():
    """Test deployed smart contracts"""
    
    print("🧪 Testing MycoShield Smart Contracts...")
    
    # Initialize Aptos manager
    aptos = AptosSecurityManager()
    
    # Connect wallet
    wallet = aptos.connect_wallet()
    print(f"Connected wallet: {wallet}")
    
    # Test threat intelligence contract
    print("\n1. Testing ThreatIntelligence contract...")
    threat_tx = aptos.submit_threat_data("192.168.1.100", 0.85, "malware")
    print(f"Threat submitted: {threat_tx}")
    
    # Test security incidents contract
    print("\n2. Testing SecurityIncidents contract...")
    incident_data = {
        "ip_address": "10.0.0.1",
        "action_taken": "ISOLATED",
        "threat_score": 0.9,
        "timestamp": "2024-01-01T12:00:00"
    }
    incident_tx = aptos.log_security_incident(incident_data)
    print(f"Incident logged: {incident_tx}")
    
    # Test threat scoring
    print("\n3. Testing ThreatScoring contract...")
    consensus = aptos.validate_threat_consensus("192.168.1.100")
    print(f"Threat consensus: {consensus}")
    
    print("\n✅ All contract tests completed!")

if __name__ == "__main__":
    asyncio.run(test_contracts())