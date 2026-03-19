#!/bin/bash
source venv/bin/activate

GREEN='\033[0;32m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m'

pause() {
    echo ""
    read -p ">> Sonraki adima gecmek icin [ENTER] tusuna basin..."
    echo ""
    clear
}

clear
echo -e "${CYAN}==========================================${NC}"
echo -e "${GREEN}  TrustVerify: File Integrity & Auth Demo ${NC}"
echo -e "${CYAN}==========================================${NC}"
echo "Hos geldiniz! Bu canli demoda (Live Demo) adim adim Dijital Imza ve Hashing algoritmalarini gorecegiz."
pause

echo -e "${CYAN}ADIM 1: RSA Anahtar Ciftini Uretme (Public / Private Keys)${NC}"
echo "+ Calistirilan Komut: python trustverify.py init-keys"
echo "------------------------------------------------------"
python trustverify.py init-keys
ls -lh *.pem
pause

echo -e "${CYAN}ADIM 2: Test Dosyalarini Olusturma${NC}"
echo "+ Klasor test_dir temizleniyor ve 2 adet ornek dosya yaratiliyor..."
echo "------------------------------------------------------"
rm -rf test_dir
mkdir test_dir
echo "Cok gizli proje raporu 2026." > test_dir/file1.txt
echo "Siradan bir veri dosyasi." > test_dir/file2.txt
ls -l test_dir
pause

echo -e "${CYAN}ADIM 3: Manifest Uretme (Hashing)${NC}"
echo "+ Calistirilan Komut: python trustverify.py manifest test_dir"
echo "+ Amac: Dosyalarin SHA-256 kodlarini cikarip json dosyasinda saklamak."
echo "------------------------------------------------------"
python trustverify.py manifest test_dir
cat test_dir/metadata.json
pause

echo -e "${CYAN}ADIM 4: Veriyi Dijital Olarak Imzalama (Signing)${NC}"
echo "+ Calistirilan Komut: python trustverify.py sign test_dir private_key.pem"
echo "+ Amac: Göndericinin 'Gizli Anahtari' ile metadata.json dosyasini imzalayarak kimligini kanitlamasi."
echo "------------------------------------------------------"
python trustverify.py sign test_dir private_key.pem
pause

echo -e "${CYAN}ADIM 5: Basarili Dogrulama (Receiver Side Verification)${NC}"
echo "+ Calistirilan Komut: python trustverify.py verify test_dir public_key.pem test_dir/signature.sig"
echo "+ Amac: Alici dosyalari indirdiginde, Acik Anahtar (Public Key) ile dogrulama yapar."
echo "------------------------------------------------------"
python trustverify.py verify test_dir public_key.pem test_dir/signature.sig
pause

echo -e "${RED}ADIM 6: HACKING / TAMPERING - Bir dosya gizlice degistiriliyor!${NC}"
echo "+ 'file1.txt' dosyasinin altina 'IZINSIZ KOD: KORSAN' satiri eklendi."
echo "------------------------------------------------------"
echo "IZINSIZ KOD: KORSAN" >> test_dir/file1.txt
cat test_dir/file1.txt
pause

echo -e "${RED}ADIM 7: Manipule Edilmis Dosyayi Dogrulama Islemi (Korsan Siziş)${NC}"
echo "+ Calistirilan Komut: python trustverify.py verify test_dir public_key.pem test_dir/signature.sig"
echo "+ Amac: Sistemin, imzasi ayni kalsa bile içeriği değişen dosyayı anında RED etmesini görmek."
echo "------------------------------------------------------"
python trustverify.py verify test_dir public_key.pem test_dir/signature.sig || true
echo ""
echo -e "${CYAN}==========================================${NC}"
echo -e "${GREEN}        DEMO BASARIYLA TAMAMLANDI!        ${NC}"
echo -e "${CYAN}==========================================${NC}"
