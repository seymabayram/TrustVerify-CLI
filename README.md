IntegrityGuardians – TrustVerify CLI Tool
TrustVerify is a Python-based Command Line Interface (CLI) tool designed to ensure file integrity and authenticity. Using SHA-256 hashing and RSA digital signatures, it allows a sender to sign files and a receiver to verify that the files have not been tampered with and originate from the claimed sender.
🚀 Features
Generate SHA-256 hashes for files of any type (text, PDF, images).
Automatically create a metadata.json manifest containing filenames and their hashes.
Verify file integrity by comparing current file states against the manifest.
Generate RSA public/private key pairs.
Sign manifests using a private key to ensure authenticity.
Verify signed manifests with the sender’s public key.
📦 Installation
Clone the repository and install the required packages:
git clone <your-repo-link>
cd TrustVerify
pip install -r requirements.txt
🛠 Usage
1. Generate Manifest for a Folder
python src/main.py generate-manifest ./sample_files
This scans the folder and creates metadata.json with SHA-256 hashes of all files.
2. Check File Integrity
python src/main.py check-manifest ./sample_files
Compares current files with the manifest to detect unauthorized changes.
3. Generate RSA Key Pair
python src/main.py generate-keys
Creates a private_key.pem and public_key.pem for digital signing.
4. Sign the Manifest
python src/main.py sign-manifest metadata.json private_key.pem
Generates a digital signature for the manifest, proving authenticity.
5. Verify Signature
python src/main.py verify-signature metadata.json signature.sig public_key.pem
Verifies that the manifest has not been altered and confirms the sender’s identity.
🔐 How It Works
Hashing: SHA-256 ensures integrity by detecting any file modifications.
Digital Signatures: RSA signing guarantees authenticity and non-repudiation.
Only the sender can generate a valid signature with their private key.
The receiver verifies the signature using the sender’s public key.
Note: Hashing alone proves data integrity but cannot prove the origin of the data. Digital signatures solve this problem.
👥 Team – IntegrityGuardians
Şeyma Bayram
Mustafa Berkay Karagöz
Kerim Taşkın
🎥 Demo Video
A 2–5 minute unlisted video should demonstrate:
Generating and signing a manifest.
Modifying a file to simulate tampering.
Running verification to show a “Verification Failed” result.
Explanation of why hashing ensures integrity but not authenticity, and how digital signatures solve this.
⚡ Libraries Used
hashlib – SHA-256 hashing
cryptography – RSA key generation, signing, verification
json – Manifest handling
argparse – CLI interface
