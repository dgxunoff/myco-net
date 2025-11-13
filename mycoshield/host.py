"""
Host-based monitoring and endpoint detection for MycoShield
"""

import psutil
import os
import platform
import hashlib
import time
import json
from datetime import datetime
from collections import defaultdict

class HostMonitor:
    """Monitor host system for suspicious activities"""
    
    def __init__(self):
        self.baseline_processes = set()
        self.process_history = defaultdict(list)
        self.file_hashes = {}
        self.suspicious_processes = set()
        
    def establish_baseline(self):
        """Establish baseline of normal system processes"""
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                self.baseline_processes.add(proc.info['name'])
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
    
    def detect_suspicious_processes(self):
        """Detect processes with suspicious behavior"""
        suspicious = []
        
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'create_time']):
            try:
                info = proc.info
                
                # New process not in baseline
                if info['name'] not in self.baseline_processes:
                    suspicious.append({
                        'type': 'new_process',
                        'pid': info['pid'],
                        'name': info['name'],
                        'cpu': info['cpu_percent'],
                        'memory': info['memory_percent'],
                        'threat_score': 0.6
                    })
                
                # High CPU/Memory usage
                if info['cpu_percent'] > 80 or info['memory_percent'] > 50:
                    suspicious.append({
                        'type': 'resource_abuse',
                        'pid': info['pid'],
                        'name': info['name'],
                        'cpu': info['cpu_percent'],
                        'memory': info['memory_percent'],
                        'threat_score': 0.7
                    })
                
                # Suspicious process names
                suspicious_names = ['nc.exe', 'ncat.exe', 'powershell.exe', 'cmd.exe', 'bash']
                if any(name in info['name'].lower() for name in suspicious_names):
                    suspicious.append({
                        'type': 'suspicious_binary',
                        'pid': info['pid'],
                        'name': info['name'],
                        'threat_score': 0.8
                    })
                    
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
                
        return suspicious
    
    def monitor_file_changes(self, watch_dirs=None):
        """Monitor critical file system changes"""
        if watch_dirs is None:
            if platform.system() == 'Windows':
                watch_dirs = ['C:\\Windows\\System32', 'C:\\Program Files']
            else:
                watch_dirs = ['/bin', '/usr/bin', '/etc']
        
        changes = []
        
        for watch_dir in watch_dirs:
            if not os.path.exists(watch_dir):
                continue
                
            try:
                for root, dirs, files in os.walk(watch_dir):
                    for file in files[:50]:  # Limit for performance
                        filepath = os.path.join(root, file)
                        try:
                            current_hash = self._get_file_hash(filepath)
                            
                            if filepath in self.file_hashes:
                                if self.file_hashes[filepath] != current_hash:
                                    changes.append({
                                        'type': 'file_modified',
                                        'path': filepath,
                                        'threat_score': 0.9
                                    })
                            
                            self.file_hashes[filepath] = current_hash
                            
                        except (OSError, PermissionError):
                            pass
                    break  # Only check top level for performance
                    
            except (OSError, PermissionError):
                pass
                
        return changes
    
    def _get_file_hash(self, filepath):
        """Get MD5 hash of file"""
        try:
            with open(filepath, 'rb') as f:
                return hashlib.md5(f.read(1024)).hexdigest()  # Only first 1KB for speed
        except:
            return None
    
    def get_system_metrics(self):
        """Get current system performance metrics"""
        return {
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_usage': psutil.disk_usage('/').percent if platform.system() != 'Windows' else psutil.disk_usage('C:\\').percent,
            'network_connections': len(psutil.net_connections()),
            'running_processes': len(psutil.pids())
        }

class LogAnalyzer:
    """Analyze system and application logs"""
    
    def __init__(self):
        self.log_patterns = {
            'failed_login': ['failed', 'authentication failed', 'login failed'],
            'privilege_escalation': ['sudo', 'runas', 'elevated', 'administrator'],
            'suspicious_commands': ['nc ', 'netcat', 'powershell -enc', 'base64', 'wget', 'curl']
        }
    
    def analyze_windows_events(self):
        """Analyze Windows Event Logs (simplified)"""
        suspicious_events = []
        
        try:
            import subprocess
            
            # Get recent security events
            cmd = 'wevtutil qe Security /c:50 /rd:true /f:text'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    for pattern_type, patterns in self.log_patterns.items():
                        if any(pattern.lower() in line.lower() for pattern in patterns):
                            suspicious_events.append({
                                'type': pattern_type,
                                'event': line.strip(),
                                'threat_score': 0.7,
                                'timestamp': datetime.now().isoformat()
                            })
                            
        except Exception:
            pass
            
        return suspicious_events
    
    def analyze_linux_logs(self):
        """Analyze Linux system logs"""
        suspicious_events = []
        log_files = ['/var/log/auth.log', '/var/log/syslog', '/var/log/messages']
        
        for log_file in log_files:
            if not os.path.exists(log_file):
                continue
                
            try:
                with open(log_file, 'r') as f:
                    # Read last 100 lines
                    lines = f.readlines()[-100:]
                    
                    for line in lines:
                        for pattern_type, patterns in self.log_patterns.items():
                            if any(pattern.lower() in line.lower() for pattern in patterns):
                                suspicious_events.append({
                                    'type': pattern_type,
                                    'event': line.strip(),
                                    'threat_score': 0.7,
                                    'timestamp': datetime.now().isoformat()
                                })
                                
            except (OSError, PermissionError):
                pass
                
        return suspicious_events

class MultiModalDetector:
    """Combine network, host, and log analysis"""
    
    def __init__(self, network_detector, host_monitor, log_analyzer):
        self.network_detector = network_detector
        self.host_monitor = host_monitor
        self.log_analyzer = log_analyzer
        
    def comprehensive_analysis(self, network_data=None):
        """Perform multi-source threat analysis"""
        
        # Network analysis
        network_threats = {}
        if network_data:
            network_threats = self.network_detector.detect_anomalies(
                network_data[0], network_data[1]
            )
        
        # Host analysis
        host_threats = {
            'processes': self.host_monitor.detect_suspicious_processes(),
            'files': self.host_monitor.monitor_file_changes(),
            'metrics': self.host_monitor.get_system_metrics()
        }
        
        # Log analysis
        system = platform.system().lower()
        if system == 'windows':
            log_threats = self.log_analyzer.analyze_windows_events()
        else:
            log_threats = self.log_analyzer.analyze_linux_logs()
        
        # Correlation and scoring
        return self._correlate_threats(network_threats, host_threats, log_threats)
    
    def _correlate_threats(self, network_threats, host_threats, log_threats):
        """Correlate threats across different sources"""
        
        correlated_threats = {
            'network': network_threats,
            'host': host_threats,
            'logs': log_threats,
            'correlation_score': 0.0,
            'recommended_action': 'MONITOR'
        }
        
        # Calculate correlation score
        network_score = max(network_threats.values()) if network_threats else 0
        host_score = max([t.get('threat_score', 0) for t in host_threats['processes']], default=0)
        log_score = max([t.get('threat_score', 0) for t in log_threats], default=0)
        
        # Weighted correlation
        correlated_threats['correlation_score'] = (
            network_score * 0.4 + 
            host_score * 0.4 + 
            log_score * 0.2
        )
        
        # Determine action
        if correlated_threats['correlation_score'] > 0.8:
            correlated_threats['recommended_action'] = 'ISOLATE'
        elif correlated_threats['correlation_score'] > 0.6:
            correlated_threats['recommended_action'] = 'MONITOR'
        else:
            correlated_threats['recommended_action'] = 'ALLOW'
            
        return correlated_threats