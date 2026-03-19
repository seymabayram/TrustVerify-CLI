#!/bin/bash
source venv/bin/activate
echo "--- 1. Generating Keys ---"
python trustverify.py init-keys

echo "--- 2. Creating Test Directory and Files ---"
mkdir -p test_dir
echo "Hello, secure world!" > test_dir/file1.txt
echo "Sensitive data here." > test_dir/file2.txt

echo "--- 3. Generating Manifest ---"
python trustverify.py manifest test_dir

echo "--- 4. Checking Local Manifest ---"
python trustverify.py check test_dir

echo "--- 5. Signing Manifest ---"
python trustverify.py sign test_dir private_key.pem

echo "--- 6. Verifying Signature ---"
python trustverify.py verify test_dir public_key.pem test_dir/signature.sig

echo "--- 7. Tampering with File ---"
echo "TAMPERED" >> test_dir/file1.txt

echo "--- 8. Verifying Signature After Tampering (Should fail locally) ---"
python trustverify.py verify test_dir public_key.pem test_dir/signature.sig
