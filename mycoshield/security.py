"""
Security enforcement and incident response for MycoShield
"""

import subprocess
import platform
import logging
import json
import smtplib
from datetime import datetime
try:
    from email.mime.text import MIMEText as MimeText
    from email.mime.multipart import MIMEMultipart as MimeMultipart
except ImportError:
    class MimeText:
        def __init__(self, *args, **kwargs): pass
    class MimeMultipart:
        def __init__(self, *args, **kwargs): pass

class SecurityEnforcer:
    """Real network security enforcement with blockchain integration"""
    
    def __init__(self, config=None):
        self.config = config or {}
        self.blocked_ips = set()
        self.incident_log = []
        self.setup_logging()
        
        # Initialize blockchain integration if enabled
        if self.config.get('aptos', {}).get('enabled', False):
            try:
                from .blockchain_integration import BlockchainSecurityOrchestrator
                self.blockchain = BlockchainSecurityOrchestrator()
                self.blockchain_enabled = True
            except ImportError:
                self.blockchain_enabled = False
        else:
            self.blockchain_enabled = False
        
    def setup_logging(self):
        logging.basicConfig(
            filename='mycoshield_incidents.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('MycoShield')
    
    def isolate_node(self, ip_address, threat_score, action_type="ISOLATE"):
        """Execute real isolation actions"""
        
        if action_type == "ISOLATE":
            # Block IP in firewall
            self._block_ip_firewall(ip_address)
            
            # Log incident
            incident = self._log_incident(ip_address, threat_score, "ISOLATED")
            
            # Alert security team
            self._send_security_alert(incident)
            
            return True
        
        elif action_type == "MONITOR":
            # Enhanced monitoring
            self._enable_enhanced_monitoring(ip_address)
            self._log_incident(ip_address, threat_score, "MONITORING")
            
        return False
    
    def _block_ip_firewall(self, ip_address):
        """Block IP using system firewall"""
        
        if ip_address in self.blocked_ips:
            return
            
        system = platform.system().lower()
        
        try:
            if system == "windows":
                # Windows Firewall
                cmd = f'netsh advfirewall firewall add rule name="MycoShield_Block_{ip_address}" dir=in action=block remoteip={ip_address}'
                subprocess.run(cmd, shell=True, check=True)
                
            elif system == "linux":
                # iptables
                cmd = f'sudo iptables -A INPUT -s {ip_address} -j DROP'
                subprocess.run(cmd, shell=True, check=True)
                
            elif system == "darwin":  # macOS
                # pfctl
                cmd = f'echo "block in from {ip_address}" | sudo pfctl -f -'
                subprocess.run(cmd, shell=True, check=True)
                
            self.blocked_ips.add(ip_address)
            self.logger.info(f"BLOCKED IP: {ip_address}")
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to block {ip_address}: {e}")
    
    def _enable_enhanced_monitoring(self, ip_address):
        """Enable enhanced monitoring for suspicious IP"""
        
        # Log monitoring decision
        self.logger.info(f"ENHANCED MONITORING: {ip_address}")
        
        # Could integrate with SIEM systems here
        monitoring_rule = {
            "ip": ip_address,
            "timestamp": datetime.now().isoformat(),
            "action": "monitor",
            "alert_threshold": 0.5
        }
        
        # Save monitoring rules
        try:
            with open('monitoring_rules.json', 'r') as f:
                rules = json.load(f)
        except FileNotFoundError:
            rules = []
            
        rules.append(monitoring_rule)
        
        with open('monitoring_rules.json', 'w') as f:
            json.dump(rules, f, indent=2)
    
    def _log_incident(self, ip_address, threat_score, action):
        """Log security incident"""
        
        incident = {
            "timestamp": datetime.now().isoformat(),
            "ip_address": ip_address,
            "threat_score": float(threat_score),
            "action_taken": action,
            "system": platform.system(),
            "incident_id": f"MYC_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{ip_address.replace('.', '_')}"
        }
        
        self.incident_log.append(incident)
        self.logger.critical(f"SECURITY INCIDENT: {json.dumps(incident)}")
        
        # Save to incident database
        try:
            with open('security_incidents.json', 'r') as f:
                incidents = json.load(f)
        except FileNotFoundError:
            incidents = []
            
        incidents.append(incident)
        
        with open('security_incidents.json', 'w') as f:
            json.dump(incidents, f, indent=2)
        
        # Log to blockchain if enabled
        if self.blockchain_enabled:
            try:
                blockchain_tx = self.blockchain.incident_response.log_security_incident(incident)
                incident['blockchain_tx'] = blockchain_tx
                self.logger.info(f"Incident logged to blockchain: {blockchain_tx}")
            except Exception as e:
                self.logger.error(f"Blockchain logging failed: {e}")
            
        return incident
    
    def _send_security_alert(self, incident):
        """Send alert to security team"""
        
        # Email configuration from config
        email_config = self.config.get('email', {})
        
        if not email_config.get('enabled', False):
            return
            
        try:
            msg = MimeMultipart()
            msg['From'] = email_config.get('from_email', 'mycoshield@company.com')
            msg['To'] = email_config.get('security_team', 'security@company.com')
            msg['Subject'] = f"🚨 MycoShield Security Alert - {incident['incident_id']}"
            
            body = f"""
MYCOSHIELD SECURITY ALERT

Incident ID: {incident['incident_id']}
Timestamp: {incident['timestamp']}
Threat IP: {incident['ip_address']}
Threat Score: {incident['threat_score']:.3f}
Action Taken: {incident['action_taken']}

The MycoShield system has detected and responded to a potential security threat.
Please review the incident logs for additional details.

This is an automated alert from the MycoShield Mycelium Network Defense System.
            """
            
            msg.attach(MimeText(body, 'plain'))
            
            server = smtplib.SMTP(email_config.get('smtp_server', 'localhost'), 
                                email_config.get('smtp_port', 587))
            server.starttls()
            
            if email_config.get('username'):
                server.login(email_config['username'], email_config['password'])
                
            server.send_message(msg)
            server.quit()
            
            self.logger.info(f"Security alert sent for incident {incident['incident_id']}")
            
        except Exception as e:
            self.logger.error(f"Failed to send security alert: {e}")
    
    def unblock_ip(self, ip_address):
        """Remove IP from firewall block list"""
        
        if ip_address not in self.blocked_ips:
            return
            
        system = platform.system().lower()
        
        try:
            if system == "windows":
                cmd = f'netsh advfirewall firewall delete rule name="MycoShield_Block_{ip_address}"'
                subprocess.run(cmd, shell=True, check=True)
                
            elif system == "linux":
                cmd = f'sudo iptables -D INPUT -s {ip_address} -j DROP'
                subprocess.run(cmd, shell=True, check=True)
                
            elif system == "darwin":
                # pfctl rules are temporary by default
                pass
                
            self.blocked_ips.remove(ip_address)
            self.logger.info(f"UNBLOCKED IP: {ip_address}")
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to unblock {ip_address}: {e}")
    
    def get_incident_summary(self):
        """Get summary of security incidents"""
        
        total_incidents = len(self.incident_log)
        blocked_count = sum(1 for i in self.incident_log if i['action_taken'] == 'ISOLATED')
        monitored_count = sum(1 for i in self.incident_log if i['action_taken'] == 'MONITORING')
        
        return {
            "total_incidents": total_incidents,
            "blocked_ips": blocked_count,
            "monitored_ips": monitored_count,
            "currently_blocked": len(self.blocked_ips),
            "recent_incidents": self.incident_log[-5:] if self.incident_log else []
        }

class NetworkMonitor:
    """Enhanced network monitoring for suspicious activities"""
    
    def __init__(self):
        self.monitoring_rules = self._load_monitoring_rules()
        
    def _load_monitoring_rules(self):
        try:
            with open('monitoring_rules.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def check_monitored_ips(self, current_connections):
        """Check if monitored IPs are showing suspicious behavior"""
        
        alerts = []
        
        for rule in self.monitoring_rules:
            monitored_ip = rule['ip']
            
            # Check current connections for this IP
            ip_connections = [conn for conn in current_connections 
                            if conn.get('orig_h') == monitored_ip or conn.get('resp_h') == monitored_ip]
            
            if len(ip_connections) > 10:  # Threshold for suspicious activity
                alerts.append({
                    "ip": monitored_ip,
                    "alert": "High connection volume detected",
                    "connection_count": len(ip_connections),
                    "timestamp": datetime.now().isoformat()
                })
                
        return alerts