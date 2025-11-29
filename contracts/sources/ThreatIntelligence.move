module mycoshield::threat_intelligence {
    use std::signer;
    use std::vector;
    use aptos_framework::timestamp;

    struct ThreatData has key {
        threats: vector<ThreatEntry>
    }

    struct ThreatEntry has store, copy, drop {
        ip_address: vector<u8>,
        threat_score: u64,
        threat_type: vector<u8>,
        timestamp: u64,
        reporter: address
    }

    public fun initialize(account: &signer) {
        move_to(account, ThreatData { threats: vector::empty() });
    }

    public fun submit_threat(
        account: &signer,
        ip: vector<u8>,
        score: u64,
        threat_type: vector<u8>
    ) acquires ThreatData {
        let threat_data = borrow_global_mut<ThreatData>(signer::address_of(account));
        let entry = ThreatEntry {
            ip_address: ip,
            threat_score: score,
            threat_type,
            timestamp: timestamp::now_microseconds(),
            reporter: signer::address_of(account)
        };
        vector::push_back(&mut threat_data.threats, entry);
    }

    public fun get_threat_count(addr: address): u64 acquires ThreatData {
        let threat_data = borrow_global<ThreatData>(addr);
        vector::length(&threat_data.threats)
    }
}