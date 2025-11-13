"""
Enterprise MycoShield - Full endpoint security platform
"""

import time
import threading
from datetime import datetime
from .endpoint import (RegistryMonitor, MemoryAnalyzer, SystemCallMonitor, 
                      MalwareScanner, BehavioralAnalyzer, UserActivityMonitor,
                      DeviceFingerprinter, ApplicationMonitor)
from .host import HostMonitor, LogAnalyzer
from .security import SecurityEnforcer

class EnterpriseMycoShield:
    """Enterprise-grade security platform"""
    
    def __init__(self, config=None):
        self.config = config or {}
        
        # Initialize all security modules
        self.network_detector = None  # Set externally
        self.host_monitor = HostMonitor()
        self.log_analyzer = LogAnalyzer()
        self.security_enforcer = SecurityEnforcer(config)
        
        # Enterprise modules
        self.registry_monitor = RegistryMonitor()
        self.memory_analyzer = MemoryAnalyzer()
        self.syscall_monitor = SystemCallMonitor()
        self.malware_scanner = MalwareScanner()
        self.behavioral_analyzer = BehavioralAnalyzer()
        self.user_monitor = UserActivityMonitor()
        self.device_fingerprinter = DeviceFingerprinter()
        self.app_monitor = ApplicationMonitor()
        
        # Threat aggregation
        self.threat_database = []
        self.active_threats = {}
        
        # Monitoring control
        self.monitoring_active = False
        self.monitoring_thread = None
    
    def start_monitoring(self):
        """Start continuous monitoring"""
        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop)
        self.monitoring_thread.daemon = True
        self.monitoring_thread.start()
    
    def stop_monitoring(self):
        """Stop monitoring"""
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join()
    
    def _monitoring_loop(self):
        """Main monitoring loop"""
        while self.monitoring_active:
            try:
                # Perform comprehensive scan
                threats = self.comprehensive_scan()
                
                # Process threats
                self._process_threats(threats)
                
                # Sleep before next scan
                time.sleep(self.config.get('scan_interval', 30))
                
            except Exception as e:
                print(f"Monitoring error: {e}")
                time.sleep(5)
    
    def comprehensive_scan(self):
        """Perform comprehensive security scan"""
        
        all_threats = {
            'timestamp': datetime.now().isoformat(),
            'network': {},
            'host': {},
            'registry': [],
            'memory': [],
            'syscalls': [],
            'malware': [],
            'behavior': [],
            'users': [],
            'device': [],
            'applications': []
        }
        
        # Network threats (if network detector available)
        if self.network_detector:
            try:
                # This would be called with actual network data
                all_threats['network'] = {}  # Placeholder
            except Exception as e:
                print(f"Network scan error: {e}")
        
        # Host-based threats
        try:
            all_threats['host'] = {
                'processes': self.host_monitor.detect_suspicious_processes(),
                'files': self.host_monitor.monitor_file_changes(),
                'metrics': self.host_monitor.get_system_metrics()
            }
        except Exception as e:
            print(f"Host scan error: {e}")
        
        # Registry monitoring
        try:
            all_threats['registry'] = self.registry_monitor.detect_registry_changes()
        except Exception as e:
            print(f"Registry scan error: {e}")
        
        # Memory analysis
        try:
            all_threats['memory'] = self.memory_analyzer.detect_code_injection()
        except Exception as e:
            print(f"Memory scan error: {e}")
        
        # System call monitoring
        try:
            all_threats['syscalls'] = self.syscall_monitor.monitor_syscalls()
        except Exception as e:
            print(f"Syscall scan error: {e}")
        
        # Malware scanning
        try:
            all_threats['malware'] = self.malware_scanner.scan_running_processes()
        except Exception as e:
            print(f"Malware scan error: {e}")
        
        # Behavioral analysis
        try:
            behavior_threats = []
            import psutil
            for proc in psutil.process_iter(['pid']):
                try:
                    threats = self.behavioral_analyzer.analyze_process_behavior(proc.info['pid'])
                    behavior_threats.extend(threats)
                except:
                    pass
            all_threats['behavior'] = behavior_threats
        except Exception as e:
            print(f"Behavior scan error: {e}")
        
        # User activity monitoring
        try:
            self.user_monitor.track_user_session()
            all_threats['users'] = self.user_monitor.detect_privilege_escalation()
        except Exception as e:
            print(f"User scan error: {e}")
        
        # Device fingerprinting
        try:
            all_threats['device'] = self.device_fingerprinter.detect_device_changes()
        except Exception as e:
            print(f"Device scan error: {e}")
        
        # Application monitoring
        try:
            app_threats = []
            
            # Web logs (if available)
            web_logs = ['/var/log/apache2/access.log', '/var/log/nginx/access.log', 
                       'C:\\inetpub\\logs\\LogFiles\\W3SVC1\\*.log']
            
            for log_file in web_logs:
                try:
                    threats = self.app_monitor.analyze_web_logs(log_file)
                    app_threats.extend(threats)
                except:
                    pass
            
            all_threats['applications'] = app_threats
        except Exception as e:
            print(f"Application scan error: {e}")
        
        return all_threats
    
    def _process_threats(self, threats):
        """Process and respond to detected threats"""
        
        # Calculate overall threat score
        threat_scores = []
        
        # Collect all threat scores
        for category, category_threats in threats.items():
            if category == 'timestamp':
                continue
                
            if isinstance(category_threats, dict):
                if 'processes' in category_threats:
                    threat_scores.extend([t.get('threat_score', 0) for t in category_threats['processes']])
                if 'files' in category_threats:
                    threat_scores.extend([t.get('threat_score', 0) for t in category_threats['files']])
            elif isinstance(category_threats, list):
                threat_scores.extend([t.get('threat_score', 0) for t in category_threats])
        
        # Calculate max threat score
        max_threat_score = max(threat_scores) if threat_scores else 0
        
        # Store in threat database
        threat_record = {
            'timestamp': threats['timestamp'],
            'max_threat_score': max_threat_score,
            'threat_count': len(threat_scores),
            'categories': list(threats.keys())
        }
        
        self.threat_database.append(threat_record)
        
        # Keep only last 1000 records
        if len(self.threat_database) > 1000:
            self.threat_database = self.threat_database[-1000:]
        
        # Take action based on threat level
        if max_threat_score > 0.8:
            self._handle_critical_threat(threats)
        elif max_threat_score > 0.6:
            self._handle_moderate_threat(threats)
    
    def _handle_critical_threat(self, threats):
        """Handle critical threats"""
        
        # Extract IPs from network threats for blocking
        ips_to_block = []
        
        # Look for process-based threats to terminate
        processes_to_kill = []
        
        for category, category_threats in threats.items():
            if isinstance(category_threats, list):
                for threat in category_threats:
                    if threat.get('threat_score', 0) > 0.8:
                        
                        # Block malicious processes
                        if 'pid' in threat:
                            processes_to_kill.append(threat['pid'])
                        
                        # Block suspicious IPs (if available)
                        if 'ip_address' in threat:
                            ips_to_block.append(threat['ip_address'])
        
        # Execute blocking actions
        for ip in ips_to_block:
            self.security_enforcer.isolate_node(ip, 0.9, "ISOLATE")
        
        # Terminate malicious processes
        import psutil
        for pid in processes_to_kill:
            try:
                proc = psutil.Process(pid)
                proc.terminate()
                print(f"Terminated malicious process PID: {pid}")
            except:
                pass
    
    def _handle_moderate_threat(self, threats):
        """Handle moderate threats"""
        
        # Enhanced monitoring for moderate threats
        for category, category_threats in threats.items():
            if isinstance(category_threats, list):
                for threat in category_threats:
                    if 0.6 < threat.get('threat_score', 0) <= 0.8:
                        
                        # Log for investigation
                        print(f"Moderate threat detected: {threat}")
                        
                        # Increase monitoring frequency
                        if 'ip_address' in threat:
                            self.security_enforcer.isolate_node(threat['ip_address'], 
                                                              threat['threat_score'], "MONITOR")
    
    def get_security_dashboard(self):
        """Get comprehensive security dashboard data"""
        
        # Recent threats summary
        recent_threats = self.threat_database[-10:] if self.threat_database else []
        
        # Current system status
        current_scan = self.comprehensive_scan()
        
        # Calculate statistics
        total_threats = sum(len(threats) if isinstance(threats, list) else 0 
                          for threats in current_scan.values())
        
        critical_threats = 0
        moderate_threats = 0
        
        for category, category_threats in current_scan.items():
            if isinstance(category_threats, list):
                for threat in category_threats:
                    score = threat.get('threat_score', 0)
                    if score > 0.8:
                        critical_threats += 1
                    elif score > 0.6:
                        moderate_threats += 1
        
        return {
            'system_status': 'CRITICAL' if critical_threats > 0 else 'WARNING' if moderate_threats > 0 else 'HEALTHY',
            'total_threats': total_threats,
            'critical_threats': critical_threats,
            'moderate_threats': moderate_threats,
            'recent_scans': recent_threats,
            'current_threats': current_scan,
            'monitoring_active': self.monitoring_active,
            'device_fingerprint': self.device_fingerprinter.device_profile['fingerprint'][:16] + '...'
        }