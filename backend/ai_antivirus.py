import os
import hashlib
import joblib

# Defensive AI Antivirus Module
class StrongDefensiveAntivirus:
    def __init__(self):
        # Example: Load local ML model (train with malware dataset offline)
        try:
            self.model = joblib.load('malware_classifier.pkl')
        except:
            self.model = None
    def scan_file(self, file_path):
        try:
            with open(file_path, 'rb') as f:
                contents = f.read()
            # Simple heuristic: Check for suspicious signatures/hashes
            suspicious_hashes = [
                # Add known malware hashes
                'e99a18c428cb38d5f260853678922e03',  # Example MD5
            ]
            file_hash = hashlib.md5(contents).hexdigest()
            if file_hash in suspicious_hashes:
                self.quarantine(file_path)
                return 'Blocked: Known malicious signature.'
            # Optional: Use ML model if present
            if self.model:
                features = self.extract_features(contents)
                threat_score = self.model.predict_proba([features])[0][1]
                if threat_score > 0.85:
                    self.quarantine(file_path)
                    return 'Blocked: ML-classified malware.'
            return 'Safe.'
        except Exception as e:
            return f'Error scanning: {e}'
    def quarantine(self, file_path):
        quarantined_dir = 'quarantined_files'
        os.makedirs(quarantined_dir, exist_ok=True)
        os.rename(file_path, os.path.join(quarantined_dir, os.path.basename(file_path)))
    def extract_features(self, contents):
        # Dummy feature extractor: file size, entropy, printable char ratio
        size = len(contents)
        entropy = self.calculate_entropy(contents)
        printable = sum(c >= 32 and c <= 126 for c in contents) / size
        return [size, entropy, printable]
    def calculate_entropy(self, data):
        import math
        if not data: return 0
        occurences = [0]*256
        for byte in data:
            occurences[byte] += 1
        entropy = -sum((count/len(data)) * math.log2(count/len(data)) for count in occurences if count)
        return entropy

# Offensive Malware Repellent Module
class StrongOffensiveRepeller:
    def __init__(self):
        pass
    def repel_malicious_processes(self):
        import psutil
        flagged_names = ['encryptor', 'ransom', 'miner', 'trojan', 'backdoor']
        for proc in psutil.process_iter(['pid', 'name', 'exe']):
            try:
                pname = proc.info['name'].lower()
                if any(flag in pname for flag in flagged_names):
                    proc.terminate()
                    self.log_action(f"Terminated suspected malware: {pname}")
            except Exception:
                pass
    def log_action(self, msg):
        with open('antivirus_actions.log', 'a') as log:
            log.write(msg+'\n')

# Example usage
if __name__ == '__main__':
    defender = StrongDefensiveAntivirus()
    # defender.scan_file('suspicious.exe')
    repeller = StrongOffensiveRepeller()
    repeller.repel_malicious_processes()
