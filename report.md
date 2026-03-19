# TrustVerify - Project Report

## 1. Why Hashing Alone Isn't Enough to Prove Identity
Hashing provides **Integrity**. A hash function like SHA-256 takes an input file and produces a fixed-size string of characters. If even a single byte of the file is changed, the resulting hash will be drastically different. This allows us to detect *Data Tampering* or *Poisoning*.

However, a hash function alone does not provide **Authenticity** (Identity). If a malicious actor (Eve) intercepts a file sent by Alice, Eve can modify the file, recalculate its SHA-256 hash, and send the modified file and the new hash to Bob. Bob would calculate the hash, see that it matches the provided hash, and falsely believe the file is intact and came from Alice. Because anyone can calculate a SHA-256 hash, hashing alone provides no proof of *who* created the hash or the file.

## 2. How the Private/Public Key Relationship Ensures Non-Repudiation
To prove identity and achieve non-repudiation, we use **Digital Signatures** via Asymmetric Cryptography (like RSA). We generate a Key Pair:
- **Private Key**: Kept secret by the Sender.
- **Public Key**: Shared openly with everyone.

When the Sender (Alice) wants to prove she created the manifest, she hashes the `metadata.json` and then **encrypts the hash using her Private Key**. This encrypted hash is the "Digital Signature".

When the Receiver (Bob) gets the files, the manifest, and the signature, he **decrypts the signature using Alice's Public Key**, which yields the original hash calculated by Alice. Bob then calculates his own hash of the `metadata.json` and compares the two. If the hashes match, Bob is sure that the files are intact and the sender is indeed Alice.

**Non-Repudiation** is achieved because:
1. **Unforgeable Signatures**: ONLY Alice possesses her Private Key, so ONLY she could have created the signature. She cannot later deny (repudiate) having signed it.
2. **Tamper Detection**: If Eve tampered with the manifest, she could not create a valid new signature because she doesn't have Alice's Private Key. If she alters the manifest without updating the signature, Bob's hash will not match the decrypted hash, and the verification will fail.
