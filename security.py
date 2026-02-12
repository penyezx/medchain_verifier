import hashlib
import ecdsa

def calculate_pdf_hash(file_path):
    """PDF dosyasının dijital parmak izini hesaplar"""
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception:
        return None

def generate_doctor_keys():
    """Dijital imza için anahtar üretir"""
    sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
    vk = sk.get_verifying_key()
    return sk, vk