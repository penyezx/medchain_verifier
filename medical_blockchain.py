import hashlib
import json
import time

class MedicalBlock:
    def __init__(self, index, timestamp, reports, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.reports = reports  # Rapor listesi: [{'patient_id':.., 'hash':..}, ...]
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "reports": self.reports,
            "previous_hash": self.previous_hash
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

class MedicalBlockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        # Sistemin başlangıç bloğu
        return MedicalBlock(0, time.time(), [{"info": "Medical System Started"}], "0")

    def add_block(self, reports_list):
        """Toplu rapor mühürleme işlemi"""
        prev_block = self.chain[-1]
        new_block = MedicalBlock(len(self.chain), time.time(), reports_list, prev_block.hash)
        self.chain.append(new_block)
        return new_block

    def verify_report_integrity(self, input_hash):
        """Zincirde raporun hash değerini arar"""
        for block in self.chain:
            for report in block.reports:
                if report.get('report_hash') == input_hash:
                    return True, block, report
        return False, None, None

# Diğer dosyaların erişebileceği global nesne
medical_db = MedicalBlockchain()