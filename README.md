# TrustVerify - CLI Tool for File Integrity

TrustVerify is a Python-based CLI tool that allows a "Sender" to sign a file and a "Receiver" to verify its integrity and origin using hashing (SHA-256) and digital signatures (RSA).

## Setup
### 1. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install cryptography
```

## Usage Settings

### Step 1: Initialize Keys
Generates a new set of RSA keys (`private_key.pem` and `public_key.pem`).
```bash
python trustverify.py init-keys
```

### Step 2: Generate Manifest (Sender)
Generates `metadata.json` mapping all files in `<directory>` to their SHA-256 hashes.
```bash
python trustverify.py manifest <directory>
```

### Step 3: Check Local Files
Checks local files against `metadata.json` to ensure integrity.
```bash
python trustverify.py check <directory>
```

### Step 4: Sign the Manifest (Sender)
Signs the `metadata.json` using the Sender's Private Key, creating `signature.sig`.
```bash
python trustverify.py sign <directory> private_key.pem
```

### Step 5: Verify the Signature and Integrity (Receiver)
Verifies the signature of the `metadata.json` using the Sender's Public Key, and then checks the file integrity against the manifest.
```bash
python trustverify.py verify <directory> public_key.pem <directory>/signature.sig
```

## Live Demo Workflow
A completely automated test script is provided in `run_tests.sh`.
```bash
bash run_tests.sh
```
It demonstrates the entire flow, including tampering with a file to show a "Verification Failed" result.
