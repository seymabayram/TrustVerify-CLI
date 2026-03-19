# 🛡️ TrustVerify: CLI File Integrity Tool

**TrustVerify** is a Python-based Command Line Interface (CLI) application designed to ensure the **Integrity** and **Authenticity** of files. By combining SHA-256 hashing algorithms with RSA digital signatures, it allows users to detect unauthorized modifications and verify the true origin of data.

---

## 👥 The Team: CipherRoots
This project was developed by the **CipherRoots** team:
* **Şeyma Bayram**
* **Mustafa Berkay Karagöz**
* **Kerim Taşkın**

---

## 🚀 Key Features

### Part 1: Hashing and Local Integrity
* **SHA-256 Generation:** Generates a unique cryptographic hash for any file type (Text, PDF, Image).
* **Manifest Generator:** Scans a directory and creates a `metadata.json` file containing filenames and their respective hashes.
* **Integrity Check:** Compares the current state of files against the manifest to detect data poisoning or tampering.

### Part 2: Digital Signatures (RSA)
* **Key Management:** Uses the `cryptography` library to generate secure Public/Private key pairs.
* **Digital Signing:** Takes the SHA-256 hash of the `metadata.json` and encrypts it using the user's Private Key to create a signature.
* **Verification:** A receiver can use the Sender's Public Key and the signature to verify that the manifest hasn't been altered and truly came from the Sender.

---

## 🛠️ Installation & Requirements

This tool requires **Python 3.x**. You will need to install the `cryptography` library:

```bash
pip install cryptography
Usage Instructions

Generate Keys: Create your RSA key pair for secure communication.

Create Manifest: Scan your target directory to generate the metadata.json hash list.

Sign: Use your Private Key to sign the manifest file.

Verify: Use the Public Key and the signature to check the integrity and origin of the files.

📝 Technical Report Summary
The project covers two fundamental cybersecurity concepts:

Why hashing alone isn't enough: While a hash proves a file hasn't changed (Integrity), it doesn't prove who sent it. Anyone can generate a new hash for a malicious file.

Non-repudiation: Digital signatures link a file to a specific Private Key. Since only the owner has access to their Private Key, they cannot deny having signed the document, ensuring authenticity.

📺 Video Demonstration
A live demo of the script is available on YouTube. The video includes:

Live Demo: Running the script to sign files.

Tamper Test: Deliberately modifying a file to show a "Verification Failed" result.

Conceptual Explanation: Why Digital Signatures are necessary for Authenticity.

🔗 [Link to Your Unlisted YouTube Video]

Course: Mini Project I
Submission Date: 29/03/2026
Status: Completed
