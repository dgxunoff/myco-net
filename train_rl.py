#!/usr/bin/env python3
"""
MycoShield RL Training Script
Train the reinforcement learning agent
"""

from mycoshield_rl import train_mycoshield_rl
import matplotlib.pyplot as plt
import numpy as np

def main():
    print("🤖 Starting MycoShield RL Training...")
    print("=" * 50)
    
    # Train the RL agent
    agent = train_mycoshield_rl(episodes=1000)
    
    # Plot training results
    if len(agent.episode_rewards) > 0:
        plt.figure(figsize=(12, 4))
        
        # Plot 1: Episode rewards
        plt.subplot(1, 2, 1)
        plt.plot(agent.episode_rewards)
        plt.title('Episode Rewards')
        plt.xlabel('Episode')
        plt.ylabel('Total Reward')
        plt.grid(True)
        
        # Plot 2: Moving average
        plt.subplot(1, 2, 2)
        window = 50
        if len(agent.episode_rewards) >= window:
            moving_avg = np.convolve(agent.episode_rewards, 
                                   np.ones(window)/window, mode='valid')
            plt.plot(moving_avg)
            plt.title(f'Moving Average Reward (window={window})')
            plt.xlabel('Episode')
            plt.ylabel('Average Reward')
            plt.grid(True)
        
        plt.tight_layout()
        plt.savefig('rl_training_results.png')
        plt.show()
        
        print(f"📊 Training plots saved as 'rl_training_results.png'")
    
    print("\n🏆 RL Training Summary:")
    print(f"   • Episodes: 1000")
    print(f"   • Final Epsilon: {agent.epsilon:.3f}")
    print(f"   • Total Steps: {agent.step_count}")
    print(f"   • Model saved: mycoshield_rl_model.pth")
    
    print("\n🚀 Next Steps:")
    print("   1. Run: streamlit run app_rl.py")
    print("   2. Generate demo traffic")
    print("   3. Watch RL agent make decisions!")
    
if __name__ == "__main__":
    main()