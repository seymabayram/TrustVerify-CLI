import argparse
import sys
import os
import hashlib
import json
from typing import Optional

from cryptography.hazmat.primitives.asymmetric import rsa, padding  # pyre-ignore
from cryptography.hazmat.primitives import hashes, serialization  # pyre-ignore


def generate_file_hash(file_path: str) -> Optional[str]:
    """Calculate the SHA-256 hash of a file efficiently by reading in chunks."""
    sha256 = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None


def init_keys(args: argparse.Namespace) -> None:
    """Generate and save 2048-bit RSA public and private keys."""
    print("Generating 2048-bit RSA keys...")
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public_key = private_key.public_key()

    with open("private_key.pem", "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))
    
    with open("public_key.pem", "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))
    print("Keys successfully generated: 'private_key.pem' and 'public_key.pem'")


def generate_manifest(args: argparse.Namespace) -> None:
    """Scan directory recursively, excluding hidden files/envs, and create a manifest of file hashes."""
    dir_path = args.dir
    if not os.path.isdir(dir_path):
        print(f"Error: Directory '{dir_path}' does not exist.")
        sys.exit(1)

    metadata = {}
    
    # Exclude system, hidden, and Python specific directories for greater efficiency
    EXCLUDED_DIRS = {'venv', '__pycache__', '.git', '.vscode'}
    EXCLUDED_FILES = {'metadata.json', 'signature.sig', 'private_key.pem', 'public_key.pem', '.gitignore'}

    for root, dirs, files in os.walk(dir_path):
        # Mutating dirs in-place to prevent os.walk from entering excluded directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in EXCLUDED_DIRS]

        for file in files:
            # Skip hidden files or project specific configurations
            if file in EXCLUDED_FILES or file.startswith('.'):
                continue
                
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, dir_path)
            
            file_hash = generate_file_hash(file_path)
            if file_hash:
                metadata[rel_path] = file_hash

    manifest_path = os.path.join(dir_path, "metadata.json")
    try:
        with open(manifest_path, "w") as f:
            json.dump(metadata, f, indent=4)
        print(f"Manifest created successfully with {len(metadata)} files at: {manifest_path}")
    except Exception as e:
        print(f"Error writing manifest: {e}")
        sys.exit(1)


def check_local(args: argparse.Namespace) -> bool:
    """Verify local files against the hashes stored in the manifest."""
    dir_path = args.dir
    manifest_path = os.path.join(dir_path, "metadata.json")
    
    if not os.path.isfile(manifest_path):
        print(f"Error: Manifest file '{manifest_path}' not found.")
        sys.exit(1)

    try:
        with open(manifest_path, "r") as f:
            metadata = json.load(f)
    except Exception as e:
        print(f"Error reading manifest: {e}")
        sys.exit(1)

    all_match = True
    print(f"Checking {len(metadata)} files in '{dir_path}' against manifest...")
    
    for rel_path, expected_hash in metadata.items():
        file_path = os.path.join(dir_path, rel_path)
        if not os.path.exists(file_path):
            print(f"FAIL: Missing file '{rel_path}'")
            all_match = False
            continue
            
        actual_hash = generate_file_hash(file_path)
        if actual_hash != expected_hash:
            print(f"FAIL: Hash mismatch for '{rel_path}'. File has been tampered with!")
            all_match = False
        else:
            print(f"OK: '{rel_path}'")

    if all_match:
        print("Success: All files match the manifest hashes. Integrity is intact.")
        return True
    else:
        print("Error: Integrity check failed! Unauthorized modifications detected.")
        if getattr(args, '_prevent_exit', False):
            return False
        sys.exit(1)


def sign_manifest(args: argparse.Namespace) -> None:
    """Encrypt the hash of the manifest file using the sender's private key."""
    dir_path = args.dir
    priv_key_path = args.private_key
    manifest_path = os.path.join(dir_path, "metadata.json")

    if not os.path.isfile(manifest_path) or not os.path.isfile(priv_key_path):
        print("Error: Missing manifest or private key file.")
        sys.exit(1)

    try:
        with open(priv_key_path, "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
            )
            
        with open(manifest_path, "rb") as f:
            manifest_data = f.read()

        signature = private_key.sign(
            manifest_data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        
        sig_path = os.path.join(dir_path, "signature.sig")
        with open(sig_path, "wb") as f:
            f.write(signature)
        print(f"Manifest securely signed. Signature saved to '{sig_path}'")
        
    except Exception as e:
        print(f"Error signing manifest: {e}")
        sys.exit(1)


def verify_signature(args: argparse.Namespace) -> None:
    """Verify the authenticity of the manifest using the public key, then check internal file integrity."""
    dir_path = args.dir
    pub_key_path = args.public_key
    sig_path = args.signature
    manifest_path = os.path.join(dir_path, "metadata.json")

    if not all(os.path.isfile(p) for p in [manifest_path, pub_key_path, sig_path]):
        print("Error: Missing manifest, public key, or signature file.")
        sys.exit(1)

    try:
        with open(pub_key_path, "rb") as key_file:
            public_key = serialization.load_pem_public_key(key_file.read())
            
        with open(manifest_path, "rb") as f:
            manifest_data = f.read()
            
        with open(sig_path, "rb") as f:
            signature = f.read()

        public_key.verify(
            signature,
            manifest_data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        print("Signature verification SUCCESSFUL. Manifest is authentic and from the sender.")
        
        # Now automatically verify the raw files against this authentic manifest
        args._prevent_exit = True
        is_valid = check_local(args)
        if not is_valid:
            sys.exit(1)
            
    except Exception as e:
        print(f"Signature verification FAILED! The manifest has been tampered with or the signature is invalid.")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="TrustVerify: A Secure CLI Tool for File Integrity and Authenticity")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available subcommands")

    # Command: init-keys
    parser_init = subparsers.add_parser("init-keys", help="Generate 2048-bit RSA public and private keys")
    parser_init.set_defaults(func=init_keys)

    # Command: manifest
    parser_manifest = subparsers.add_parser("manifest", help="Generate a metadata.json manifest of file hashes")
    parser_manifest.add_argument("dir", help="Target directory to scan")
    parser_manifest.set_defaults(func=generate_manifest)

    # Command: check
    parser_check = subparsers.add_parser("check", help="Check local files against metadata.json for integrity")
    parser_check.add_argument("dir", help="Target directory")
    parser_check.set_defaults(func=check_local)

    # Command: sign
    parser_sign = subparsers.add_parser("sign", help="Sign the manifest using a private key")
    parser_sign.add_argument("dir", help="Directory containing metadata.json")
    parser_sign.add_argument("private_key", help="Path to sender's private key file")
    parser_sign.set_defaults(func=sign_manifest)

    # Command: verify
    parser_verify = subparsers.add_parser("verify", help="Verify the manifest signature and check file integrity")
    parser_verify.add_argument("dir", help="Directory containing metadata.json")
    parser_verify.add_argument("public_key", help="Path to sender's public key file")
    parser_verify.add_argument("signature", help="Path to the signature file (.sig)")
    parser_verify.set_defaults(func=verify_signature)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
