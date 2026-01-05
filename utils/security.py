from cryptography.fernet import Fernet
from pathlib import Path

KEY_FILE = Path("data/secret.key")

def get_cipher():
    """
    Génère ou charge une clé de chiffrement pour sécuriser les données sensibles.
    Note : Pour l'instant, cette fonction n'est pas utilisée dans l'application,
    mais elle est prête pour une future implémentation de chiffrement.
    """
    # Crée le dossier data s'il n'existe pas__________________________________________
    KEY_FILE.parent.mkdir(exist_ok=True)
    
    # Génère une nouvelle clé si elle n'existe pas____________________________________
    if not KEY_FILE.exists():
        KEY_FILE.write_bytes(Fernet.generate_key())
    
    # Retourne le cipher______________________________________________________________
    return Fernet(KEY_FILE.read_bytes())


def encrypt_data(data: str) -> bytes:
    """Chiffre des données sensibles"""
    cipher = get_cipher()
    return cipher.encrypt(data.encode())


def decrypt_data(encrypted_data: bytes) -> str:
    """Déchiffre des données"""
    cipher = get_cipher()
    return cipher.decrypt(encrypted_data).decode()