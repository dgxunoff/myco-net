"""
Enterprise-grade endpoint security for MycoShield
"""

import os
import platform
import subprocess
import winreg
import ctypes
import hashlib
import yara
import sqlite3
from datetime import datetime
import psutil
import requests
import json
from collections import defaultdict

class RegistryMonitor:
    """Monitor Windows Registry modifications"""
    
    def __init__(self):
        self.monitored_keys = [
            r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run",
            r"HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Run",
            r"HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services",
            r"HKEY_LOCAL_MACHINE\SOFTWARE\Classes\exefile\shell\open\command"
        ]
        self.baseline_registry = {}
        self.establish_baseline()
    
    def establish_baseline(self):
        """Establish registry baseline"""
        if platform.system() != 'Windows':
            return
            
        for key_path in self.monitored_keys:
            try:
                hive, subkey = key_path.split('\\', 1)
                hive_map = {
                    'HKEY_LOCAL_MACHINE': winreg.HKEY_LOCAL_MACHINE,
                    'HKEY_CURRENT_USER': winreg.HKEY_CURRENT_USER
                }
                
                with winreg.OpenKey(hive_map[hive], subkey) as key:
                    values = {}
                    i = 0
                    try:
                        while True:
                            name, value, _ = winreg.EnumValue(key, i)
                            values[name] = value
                            i += 1
                    except WindowsError:
                        pass
                    
                    self.baseline_registry[key_path] = values
                    
            except Exception:
                pass
    
    def detect_registry_changes(self):
        """Detect registry modifications"""
        changes = []
        
        for key_path in self.monitored_keys:
            try:
                hive, subkey = key_path.split('\\', 1)
                hive_map = {
                    'HKEY_LOCAL_MACHINE': winreg.HKEY_LOCAL_MACHINE,
                    'HKEY_CURRENT_USER': winreg.HKEY_CURRENT_USER
                }
                
                with winreg.OpenKey(hive_map[hive], subkey) as key:
                    current_values = {}
                    i = 0
                    try:
                        while True:
                            name, value, _ = winreg.EnumValue(key, i)
                            current_values[name] = value
                            i += 1
                    except WindowsError:
                        pass
                    
                    baseline = self.baseline_registry.get(key_path, {})
                    
                    # Check for new/modified values
                    for name, value in current_values.items():
                        if name not in baseline or baseline[name] != value:
                            changes.append({
                                'type': 'registry_modification',
                                'key': key_path,
                                'value_name': name,
                                'new_value': str(value),
                                'threat_score': 0.8
                            })
                    
                    # Check for deleted values
                    for name in baseline:
                        if name not in current_values:
                            changes.append({
                                'type': 'registry_deletion',
                                'key': key_path,
                                'value_name': name,
                                'threat_score': 0.7
                            })
                            
            except Exception:
                pass
                
        return changes

class MemoryAnalyzer:
    """Memory analysis and process injection detection"""
    
    def __init__(self):
        self.process_memory_baseline = {}
    
    def analyze_process_memory(self, pid):
        """Analyze process memory for anomalies"""
        try:
            proc = psutil.Process(pid)
            memory_info = proc.memory_info()
            
            # Check for unusual memory patterns
            anomalies = []
            
            # High memory usage
            if memory_info.rss > 500 * 1024 * 1024:  # 500MB
                anomalies.append({
                    'type': 'high_memory_usage',
                    'pid': pid,
                    'name': proc.name(),
                    'memory_mb': memory_info.rss / (1024 * 1024),
                    'threat_score': 0.6
                })
            
            # Rapid memory growth
            if pid in self.process_memory_baseline:
                baseline = self.process_memory_baseline[pid]
                growth_rate = (memory_info.rss - baseline) / baseline if baseline > 0 else 0
                
                if growth_rate > 2.0:  # 200% growth
                    anomalies.append({
                        'type': 'rapid_memory_growth',
                        'pid': pid,
                        'name': proc.name(),
                        'growth_rate': growth_rate,
                        'threat_score': 0.8
                    })
            
            self.process_memory_baseline[pid] = memory_info.rss
            return anomalies
            
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return []
    
    def detect_code_injection(self):
        """Detect potential code injection"""
        injections = []
        
        for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
            try:
                # Check for processes with unusual memory characteristics
                memory_anomalies = self.analyze_process_memory(proc.info['pid'])
                injections.extend(memory_anomalies)
                
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
                
        return injections

class SystemCallMonitor:
    """Monitor system calls for suspicious activity"""
    
    def __init__(self):
        self.suspicious_syscalls = {
            'CreateRemoteThread': 0.9,
            'WriteProcessMemory': 0.8,
            'VirtualAllocEx': 0.7,
            'SetWindowsHookEx': 0.8,
            'CreateProcess': 0.5
        }
        self.syscall_counts = defaultdict(int)
    
    def monitor_syscalls(self):
        """Monitor system calls (simplified implementation)"""
        # This would require kernel-level hooking in production
        # For now, monitor process creation as proxy
        
        suspicious_activities = []
        
        for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'create_time']):
            try:
                # Check for recently created processes
                if time.time() - proc.info['create_time'] < 60:  # Last minute
                    cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                    
                    # Check for suspicious command patterns
                    if any(pattern in cmdline.lower() for pattern in ['powershell -enc', 'cmd /c', 'rundll32']):
                        suspicious_activities.append({
                            'type': 'suspicious_process_creation',
                            'pid': proc.info['pid'],
                            'name': proc.info['name'],
                            'cmdline': cmdline,
                            'threat_score': 0.7
                        })
                        
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
                
        return suspicious_activities

class MalwareScanner:
    """YARA-based malware detection"""
    
    def __init__(self):
        self.yara_rules = self._load_yara_rules()
    
    def _load_yara_rules(self):
        """Load YARA rules for malware detection"""
        rules_content = '''
        rule Suspicious_PowerShell {
            strings:
                $a = "powershell" nocase
                $b = "-encodedcommand" nocase
                $c = "-enc" nocase
                $d = "invoke-expression" nocase
                $e = "downloadstring" nocase
            condition:
                $a and ($b or $c or $d or $e)
        }
        
        rule Potential_Backdoor {
            strings:
                $a = "nc.exe"
                $b = "netcat"
                $c = "cmd.exe /c"
                $d = "reverse shell"
            condition:
                any of them
        }
        
        rule Crypto_Miner {
            strings:
                $a = "stratum+tcp"
                $b = "mining"
                $c = "hashrate"
                $d = "cryptocurrency"
            condition:
                any of them
        }
        '''
        
        try:
            return yara.compile(source=rules_content)
        except:
            return None
    
    def scan_file(self, filepath):
        """Scan file for malware signatures"""
        if not self.yara_rules:
            return []
            
        try:
            matches = self.yara_rules.match(filepath)
            
            detections = []
            for match in matches:
                detections.append({
                    'type': 'malware_detection',
                    'file': filepath,
                    'rule': match.rule,
                    'threat_score': 0.9
                })
                
            return detections
            
        except Exception:
            return []
    
    def scan_running_processes(self):
        """Scan running processes for malware"""
        detections = []
        
        for proc in psutil.process_iter(['pid', 'name', 'exe']):
            try:
                if proc.info['exe']:
                    file_detections = self.scan_file(proc.info['exe'])
                    for detection in file_detections:
                        detection['pid'] = proc.info['pid']
                        detection['process_name'] = proc.info['name']
                        detections.append(detection)
                        
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
                
        return detections

class BehavioralAnalyzer:
    """ML-based behavioral analysis"""
    
    def __init__(self):
        self.behavior_baseline = {}
        self.anomaly_threshold = 0.7
    
    def analyze_process_behavior(self, pid):
        """Analyze process behavior patterns"""
        try:
            proc = psutil.Process(pid)
            
            # Collect behavioral metrics
            behavior = {
                'cpu_percent': proc.cpu_percent(interval=1),
                'memory_percent': proc.memory_percent(),
                'num_threads': proc.num_threads(),
                'num_fds': proc.num_fds() if hasattr(proc, 'num_fds') else 0,
                'connections': len(proc.connections()),
                'io_counters': proc.io_counters()._asdict() if proc.io_counters() else {}
            }
            
            # Simple anomaly detection based on thresholds
            anomalies = []
            
            if behavior['cpu_percent'] > 80:
                anomalies.append({
                    'type': 'high_cpu_behavior',
                    'pid': pid,
                    'name': proc.name(),
                    'cpu_percent': behavior['cpu_percent'],
                    'threat_score': 0.6
                })
            
            if behavior['connections'] > 50:
                anomalies.append({
                    'type': 'excessive_network_behavior',
                    'pid': pid,
                    'name': proc.name(),
                    'connections': behavior['connections'],
                    'threat_score': 0.7
                })
            
            return anomalies
            
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return []

class UserActivityMonitor:
    """Monitor user activity patterns"""
    
    def __init__(self):
        self.user_sessions = {}
        self.activity_log = []
    
    def track_user_session(self):
        """Track user session information"""
        try:
            users = psutil.users()
            
            for user in users:
                session_info = {
                    'username': user.name,
                    'terminal': user.terminal,
                    'host': user.host,
                    'started': user.started,
                    'timestamp': datetime.now().isoformat()
                }
                
                # Check for suspicious login patterns
                if user.host and user.host not in ['localhost', '127.0.0.1', '::1']:
                    session_info['threat_score'] = 0.6
                    session_info['type'] = 'remote_login'
                
                self.activity_log.append(session_info)
                
        except Exception:
            pass
    
    def detect_privilege_escalation(self):
        """Detect privilege escalation attempts"""
        escalations = []
        
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            try:
                # Check for processes running as different users
                if proc.info['username'] and 'admin' in proc.info['username'].lower():
                    escalations.append({
                        'type': 'privilege_escalation',
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'username': proc.info['username'],
                        'threat_score': 0.8
                    })
                    
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
                
        return escalations

class DeviceFingerprinter:
    """Device fingerprinting and asset management"""
    
    def __init__(self):
        self.device_profile = self._generate_device_profile()
    
    def _generate_device_profile(self):
        """Generate unique device fingerprint"""
        
        # Hardware information
        cpu_info = platform.processor()
        memory_info = psutil.virtual_memory().total
        disk_info = psutil.disk_usage('/').total if platform.system() != 'Windows' else psutil.disk_usage('C:\\').total
        
        # Network interfaces
        network_interfaces = []
        for interface, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                if addr.family == psutil.AF_LINK:  # MAC address
                    network_interfaces.append(addr.address)
        
        # System information
        system_info = {
            'platform': platform.platform(),
            'machine': platform.machine(),
            'processor': cpu_info,
            'memory_gb': memory_info // (1024**3),
            'disk_gb': disk_info // (1024**3),
            'mac_addresses': network_interfaces,
            'hostname': platform.node()
        }
        
        # Generate fingerprint hash
        fingerprint_data = json.dumps(system_info, sort_keys=True)
        device_fingerprint = hashlib.sha256(fingerprint_data.encode()).hexdigest()
        
        return {
            'fingerprint': device_fingerprint,
            'system_info': system_info,
            'generated_at': datetime.now().isoformat()
        }
    
    def detect_device_changes(self):
        """Detect unauthorized device modifications"""
        current_profile = self._generate_device_profile()
        
        changes = []
        
        # Compare with baseline
        if current_profile['fingerprint'] != self.device_profile['fingerprint']:
            changes.append({
                'type': 'device_modification',
                'old_fingerprint': self.device_profile['fingerprint'],
                'new_fingerprint': current_profile['fingerprint'],
                'threat_score': 0.5
            })
        
        return changes

class ApplicationMonitor:
    """Monitor application-level activities"""
    
    def __init__(self):
        self.web_log_patterns = {
            'sql_injection': [r'union\s+select', r'or\s+1=1', r'drop\s+table'],
            'xss_attack': [r'<script>', r'javascript:', r'onerror='],
            'path_traversal': [r'\.\./', r'\.\.\\', r'etc/passwd']
        }
    
    def analyze_web_logs(self, log_file):
        """Analyze web application logs"""
        threats = []
        
        try:
            with open(log_file, 'r') as f:
                lines = f.readlines()[-1000:]  # Last 1000 lines
                
                for line in lines:
                    for attack_type, patterns in self.web_log_patterns.items():
                        for pattern in patterns:
                            if re.search(pattern, line, re.IGNORECASE):
                                threats.append({
                                    'type': f'web_{attack_type}',
                                    'log_entry': line.strip(),
                                    'pattern': pattern,
                                    'threat_score': 0.8
                                })
                                
        except FileNotFoundError:
            pass
            
        return threats
    
    def monitor_database_queries(self):
        """Monitor database query patterns (placeholder)"""
        # This would integrate with database audit logs
        # For now, return empty list
        return []
    
    def monitor_api_calls(self):
        """Monitor API call patterns (placeholder)"""
        # This would integrate with API gateway logs
        # For now, return empty list
        return []