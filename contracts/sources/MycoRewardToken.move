/// MycoReward Token - Reward token for MycoShield threat detection
/// Purpose: Incentivize security researchers to detect and report threats
/// 
/// Logic:
/// 1. Mint MYCO tokens as rewards for valid threat detection
/// 2. Track reputation scores of security nodes
/// 3. Distribute rewards based on threat severity and accuracy
/// 4. Prevent spam by requiring minimum reputation to claim rewards

module myco_shield::myco_reward {
    use std::signer;
    use std::string;
    use aptos_framework::coin::{Self, MintCapability, BurnCapability};

    /// Error codes
    const E_NOT_AUTHORIZED: u64 = 1;
    const E_INSUFFICIENT_REPUTATION: u64 = 2;
    const E_ALREADY_INITIALIZED: u64 = 3;
    const E_NOT_INITIALIZED: u64 = 4;
    const E_INVALID_AMOUNT: u64 = 5;

    /// MycoReward Token structure
    struct MycoReward {}

    /// Capabilities for minting and burning tokens
    struct Capabilities has key {
        mint_cap: MintCapability<MycoReward>,
        burn_cap: BurnCapability<MycoReward>,
    }

    /// Security node reputation and rewards tracking
    struct SecurityNode has key {
        address: address,
        reputation_score: u64,      // 0-100 score based on accuracy
        threats_detected: u64,       // Total threats detected
        false_positives: u64,        // False alarms (reduces reputation)
        total_rewards_earned: u64,   // Total MYCO tokens earned
        last_reward_timestamp: u64,  // Prevent spam claiming
    }

    /// Global reward pool configuration
    struct RewardPool has key {
        admin: address,
        total_minted: u64,
        total_distributed: u64,
        base_reward: u64,            // Base reward per threat (100 MYCO)
        high_severity_multiplier: u64, // 3x for critical threats
        min_reputation: u64,         // Minimum 50 reputation to claim
    }

    /// Initialize the MycoReward token (called once by admin)
    public entry fun initialize(admin: &signer) {
        let admin_addr = signer::address_of(admin);
        
        // Ensure not already initialized
        assert!(!exists<Capabilities>(admin_addr), E_ALREADY_INITIALIZED);
        
        // Initialize the coin with metadata
        let (burn_cap, freeze_cap, mint_cap) = coin::initialize<MycoReward>(
            admin,
            string::utf8(b"MycoReward"),
            string::utf8(b"MYCO"),
            8, // 8 decimals
            true, // monitor_supply
        );

        // Store capabilities
        move_to(admin, Capabilities {
            mint_cap,
            burn_cap,
        });

        // Destroy freeze capability (we don't need freezing)
        coin::destroy_freeze_cap(freeze_cap);

        // Initialize reward pool configuration
        move_to(admin, RewardPool {
            admin: admin_addr,
            total_minted: 0,
            total_distributed: 0,
            base_reward: 100_00000000, // 100 MYCO (with 8 decimals)
            high_severity_multiplier: 3,
            min_reputation: 50,
        });
    }

    /// Register a new security node
    public entry fun register_security_node(node: &signer) {
        let node_addr = signer::address_of(node);
        
        // Register for MycoReward coin if not already registered
        if (!coin::is_account_registered<MycoReward>(node_addr)) {
            coin::register<MycoReward>(node);
        };

        // Initialize security node tracking
        if (!exists<SecurityNode>(node_addr)) {
            move_to(node, SecurityNode {
                address: node_addr,
                reputation_score: 75, // Start with 75/100 reputation
                threats_detected: 0,
                false_positives: 0,
                total_rewards_earned: 0,
                last_reward_timestamp: 0,
            });
        };
    }

    /// Mint and distribute rewards for threat detection
    /// Called by admin when a threat is validated
    public entry fun reward_threat_detection(
        admin: &signer,
        detector_address: address,
        threat_severity: u64, // 1=low, 2=medium, 3=high
        is_valid: bool,       // true if threat was real, false if false positive
    ) acquires Capabilities, SecurityNode, RewardPool {
        let admin_addr = signer::address_of(admin);
        
        // Verify admin authorization
        let pool = borrow_global_mut<RewardPool>(admin_addr);
        assert!(pool.admin == admin_addr, E_NOT_AUTHORIZED);

        // Get detector's security node data
        assert!(exists<SecurityNode>(detector_address), E_NOT_INITIALIZED);
        let node = borrow_global_mut<SecurityNode>(detector_address);

        if (is_valid) {
            // Valid threat detected - reward the detector
            node.threats_detected = node.threats_detected + 1;
            
            // Calculate reward based on severity
            let reward_amount = pool.base_reward;
            if (threat_severity == 3) {
                reward_amount = reward_amount * pool.high_severity_multiplier;
            } else if (threat_severity == 2) {
                reward_amount = reward_amount * 2;
            };

            // Check reputation requirement
            assert!(node.reputation_score >= pool.min_reputation, E_INSUFFICIENT_REPUTATION);

            // Mint tokens
            let caps = borrow_global<Capabilities>(admin_addr);
            let coins = coin::mint<MycoReward>(reward_amount, &caps.mint_cap);
            
            // Deposit to detector's account
            coin::deposit(detector_address, coins);

            // Update tracking
            node.total_rewards_earned = node.total_rewards_earned + reward_amount;
            pool.total_minted = pool.total_minted + reward_amount;
            pool.total_distributed = pool.total_distributed + reward_amount;

            // Increase reputation (max 100)
            if (node.reputation_score < 100) {
                node.reputation_score = node.reputation_score + 1;
            };

        } else {
            // False positive - penalize reputation
            node.false_positives = node.false_positives + 1;
            if (node.reputation_score > 10) {
                node.reputation_score = node.reputation_score - 5;
            };
        };
    }

    // View function: Get security node stats
    #[view]
    public fun get_node_stats(node_address: address): (u64, u64, u64, u64) acquires SecurityNode {
        if (!exists<SecurityNode>(node_address)) {
            return (0, 0, 0, 0)
        };
        
        let node = borrow_global<SecurityNode>(node_address);
        (
            node.reputation_score,
            node.threats_detected,
            node.total_rewards_earned,
            node.false_positives
        )
    }

    // View function: Get reward pool stats
    #[view]
    public fun get_pool_stats(admin_address: address): (u64, u64, u64) acquires RewardPool {
        if (!exists<RewardPool>(admin_address)) {
            return (0, 0, 0)
        };
        
        let pool = borrow_global<RewardPool>(admin_address);
        (
            pool.total_minted,
            pool.total_distributed,
            pool.base_reward
        )
    }

    /// Admin function: Update reward configuration
    public entry fun update_reward_config(
        admin: &signer,
        new_base_reward: u64,
        new_min_reputation: u64,
    ) acquires RewardPool {
        let admin_addr = signer::address_of(admin);
        let pool = borrow_global_mut<RewardPool>(admin_addr);
        
        assert!(pool.admin == admin_addr, E_NOT_AUTHORIZED);
        
        pool.base_reward = new_base_reward;
        pool.min_reputation = new_min_reputation;
    }
}