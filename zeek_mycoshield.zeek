@load base/protocols/conn

module MycoShield;

export {
    redef enum Log::ID += { LOG };
    
    type Info: record {
        ts: time &log;
        uid: string &log;
        id: conn_id &log;
        proto: transport_proto &log;
        service: string &log &optional;
        duration: interval &log &optional;
        orig_bytes: count &log &optional;
        resp_bytes: count &log &optional;
        conn_state: string &log;
        local_orig: bool &log &optional;
        local_resp: bool &log &optional;
        missed_bytes: count &log &optional;
        history: string &log &optional;
        orig_pkts: count &log &optional;
        orig_ip_bytes: count &log &optional;
        resp_pkts: count &log &optional;
        resp_ip_bytes: count &log &optional;
        tunnel_parents: set[string] &log &optional;
        threat_score: double &log &default=0.0;
    };
}

redef record connection += {
    mycoshield: Info &optional;
};

event zeek_init() &priority=5 {
    Log::create_stream(MycoShield::LOG, [$columns=Info, $path="mycoshield"]);
}

function calculate_threat_score(c: connection): double {
    local score = 0.0;
    
    # Port scanning detection
    if (c$id$resp_p in {21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995}) {
        if (c$conn$conn_state == "S0" || c$conn$conn_state == "REJ") {
            score += 0.3;
        }
    }
    
    # Unusual ports
    if (c$id$resp_p > 60000) {
        score += 0.2;
    }
    
    # Short connections with no data
    if (c$conn?$duration && c$conn$duration < 1sec && 
        (!c$conn?$orig_bytes || c$conn$orig_bytes == 0)) {
        score += 0.4;
    }
    
    # High volume connections
    if (c$conn?$orig_bytes && c$conn$orig_bytes > 1000000) {
        score += 0.3;
    }
    
    # Suspicious IPs (simulated)
    local suspicious_nets = {
        10.0.0.0/8,
        172.16.0.0/12,
        203.0.113.0/24
    };
    
    if (c$id$resp_h in suspicious_nets) {
        score += 0.5;
    }
    
    return score;
}

event connection_state_remove(c: connection) {
    local info: MycoShield::Info;
    
    info$ts = network_time();
    info$uid = c$uid;
    info$id = c$id;
    info$proto = get_conn_transport_proto(c$id);
    
    if (c$conn?$service) {
        info$service = c$conn$service;
    }
    
    if (c$conn?$duration) {
        info$duration = c$conn$duration;
    }
    
    if (c$conn?$orig_bytes) {
        info$orig_bytes = c$conn$orig_bytes;
    }
    
    if (c$conn?$resp_bytes) {
        info$resp_bytes = c$conn$resp_bytes;
    }
    
    info$conn_state = c$conn$conn_state;
    
    if (c$conn?$local_orig) {
        info$local_orig = c$conn$local_orig;
    }
    
    if (c$conn?$local_resp) {
        info$local_resp = c$conn$local_resp;
    }
    
    if (c$conn?$missed_bytes) {
        info$missed_bytes = c$conn$missed_bytes;
    }
    
    if (c$conn?$history) {
        info$history = c$conn$history;
    }
    
    if (c$conn?$orig_pkts) {
        info$orig_pkts = c$conn$orig_pkts;
    }
    
    if (c$conn?$orig_ip_bytes) {
        info$orig_ip_bytes = c$conn$orig_ip_bytes;
    }
    
    if (c$conn?$resp_pkts) {
        info$resp_pkts = c$conn$resp_pkts;
    }
    
    if (c$conn?$resp_ip_bytes) {
        info$resp_ip_bytes = c$conn$resp_ip_bytes;
    }
    
    info$threat_score = calculate_threat_score(c);
    
    Log::write(MycoShield::LOG, info);
}