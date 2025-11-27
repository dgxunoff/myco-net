module mycoshield::security_incidents {
    use std::signer;
    use std::vector;
    use aptos_framework::timestamp;

    struct IncidentLog has key {
        incidents: vector<SecurityIncident>
    }

    struct SecurityIncident has store, copy, drop {
        incident_id: vector<u8>,
        ip_address: vector<u8>,
        action_taken: vector<u8>,
        threat_score: u64,
        timestamp: u64,
        system_info: vector<u8>
    }

    public fun initialize(account: &signer) {
        move_to(account, IncidentLog { incidents: vector::empty() });
    }

    public fun log_incident(
        account: &signer,
        ip: vector<u8>,
        action: vector<u8>,
        score: u64,
        incident_id: vector<u8>
    ) acquires IncidentLog {
        let incident_log = borrow_global_mut<IncidentLog>(signer::address_of(account));
        let incident = SecurityIncident {
            incident_id,
            ip_address: ip,
            action_taken: action,
            threat_score: score,
            timestamp: timestamp::now_microseconds(),
            system_info: b"MycoShield"
        };
        vector::push_back(&mut incident_log.incidents, incident);
    }

    public fun get_incident_count(addr: address): u64 acquires IncidentLog {
        let incident_log = borrow_global<IncidentLog>(addr);
        vector::length(&incident_log.incidents)
    }
}