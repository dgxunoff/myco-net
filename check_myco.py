"""Quick MYCO balance checker"""
import subprocess
import json

WALLET = "0x84226fc4b809a744f0195c0d63d51e51e96e85881f6cd26e1102cfe758ce20cb"

print("=== MYCO Token Status ===\n")

# Get node stats
result = subprocess.run([
    "aptos", "move", "view",
    "--function-id", f"{WALLET}::myco_reward::get_node_stats",
    "--args", f"address:{WALLET}"
], capture_output=True, text=True)

if result.returncode == 0:
    data = json.loads(result.stdout)
    reputation, threats, rewards, false_pos = data["Result"]
    
    myco_balance = int(rewards) / 100000000
    
    print(f"Wallet: {WALLET[:10]}...{WALLET[-8:]}")
    print(f"\nMYCO Balance: {myco_balance:.2f} MYCO")
    print(f"Reputation: {reputation}/100")
    print(f"Threats Detected: {threats}")
    print(f"False Positives: {false_pos}")
    print(f"\nStatus: {'Active Security Node' if int(reputation) >= 50 else 'Low Reputation'}")
else:
    print("Error: Could not fetch stats")
