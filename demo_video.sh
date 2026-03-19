#!/bin/bash
source venv/bin/activate

GREEN='\033[0;32m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m'

pause() {
    echo ""
    read -p ">> Press [ENTER] to continue to the next step..."
    echo ""
    clear
}

clear
echo -e "${CYAN}==========================================${NC}"
echo -e "${GREEN}  TrustVerify: File Integrity & Auth Demo ${NC}"
echo -e "${CYAN}==========================================${NC}"
echo "Welcome! In this Live Demo, we will observe Digital Signature and Hashing algorithms step by step."
pause

echo -e "${CYAN}STEP 1: Generate RSA Key Pair (Public / Private Keys)${NC}"
echo "+ Executing Command: python trustverify.py init-keys"
echo "------------------------------------------------------"
python trustverify.py init-keys
ls -lh *.pem
pause

echo -e "${CYAN}STEP 2: Create Test Directories and Files${NC}"
echo "+ Cleaning 'test_dir' directory and creating 2 sample files..."
echo "------------------------------------------------------"
rm -rf test_dir
mkdir test_dir
echo "Top secret project report 2026." > test_dir/file1.txt
echo "A regular data file." > test_dir/file2.txt
ls -l test_dir
pause

echo -e "${CYAN}STEP 3: Generate Manifest (Hashing)${NC}"
echo "+ Executing Command: python trustverify.py manifest test_dir"
echo "+ Purpose: Calculate SHA-256 hashes of the files and store them in a JSON manifest."
echo "------------------------------------------------------"
python trustverify.py manifest test_dir
cat test_dir/metadata.json
pause

echo -e "${CYAN}STEP 4: Digitally Sign the File (Signing)${NC}"
echo "+ Executing Command: python trustverify.py sign test_dir private_key.pem"
echo "+ Purpose: The sender encrypts (signs) the manifest hash with their Private Key to prove authenticity."
echo "------------------------------------------------------"
python trustverify.py sign test_dir private_key.pem
ls -lh test_dir/signature.sig
pause

echo -e "${CYAN}STEP 5: Successful Verification (Receiver Side)${NC}"
echo "+ Executing Command: python trustverify.py verify test_dir public_key.pem test_dir/signature.sig"
echo "+ Purpose: The receiver uses the sender's Public Key to verify the signature and checks file integrity."
echo "------------------------------------------------------"
python trustverify.py verify test_dir public_key.pem test_dir/signature.sig
pause

echo -e "${RED}STEP 6: HACKING / TAMPERING - A file is secretly modified!${NC}"
echo "+ Appended 'UNAUTHORIZED CODE: HACKED' line to 'file1.txt'."
echo "------------------------------------------------------"
echo "UNAUTHORIZED CODE: HACKED" >> test_dir/file1.txt
cat test_dir/file1.txt
pause

echo -e "${RED}STEP 7: Verifying the Manipulated File (Tampering Detection)${NC}"
echo "+ Executing Command: python trustverify.py verify test_dir public_key.pem test_dir/signature.sig"
echo "+ Purpose: Observe how the system immediately REJECTS the modified file even though the signature is valid."
echo "------------------------------------------------------"
python trustverify.py verify test_dir public_key.pem test_dir/signature.sig || true
echo ""
echo -e "${CYAN}==========================================${NC}"
echo -e "${GREEN}       DEMO COMPLETED SUCCESSFULLY!       ${NC}"
echo -e "${CYAN}==========================================${NC}"
