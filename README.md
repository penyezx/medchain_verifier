MedChain Verifier 🛡️
A decentralized authentication system designed to ensure the integrity and security of medical reports using Blockchain technology. This system addresses the vulnerabilities of centralized databases by providing an immutable and transparent verification mechanism.
+2

🌟 Key Features
Immutability: Once a report is sealed, it cannot be altered or deleted.

SHA-256 Security: Uses unique digital fingerprints for PDF document identification.
+1

Privacy-First: Only document hashes are stored on the blockchain, not the files themselves.

Modern GUI: A dark-mode dashboard for easy report sealing and instant verification.
+2

🛠️ Tech Stack
Language: Python.

Interface: Tkinter (GUI toolkit).
+1

Cryptography: Hashlib (SHA-256) and ECDSA digital signatures.

Data Handling: JSON for block serialization.
+1

📂 Core Modules
medical_blockchain.py: Contains the decentralized ledger logic and block creation.

security.py: Handles raw binary data processing and PDF hashing.

interface.py: Manages the user interface and functional dashboards.

🚀 Quick Start
Dependencies: pip install ecdsa

Run App: python interface.py

Seal: Enter Patient ID, select PDF, and click Zincire İşle (Seal to Chain).

Verify: Upload a PDF in the Doğrulama Merkezi (Verification Center) to check its validity.

