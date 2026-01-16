"""
Module de configuration du chiffrement des données sensibles

IMPORTANT : L'activation du chiffrement est optionnelle et nécessite une migration
des données existantes. Ce module fournit les outils pour activer/désactiver
le chiffrement de manière sécurisée.
"""
import sqlite3
from pathlib import Path
from utils.security import encrypt_data, decrypt_data


class EncryptionConfig:
    def __init__(self, db_path="data/journal.db"):
        self.db_path = Path(db_path)
        self.config_file = Path("data/encryption_enabled.txt")

    def is_encryption_enabled(self):
        return self.config_file.exists()

    def enable_encryption(self):
        """
        Active le chiffrement et migre les données existantes

        ATTENTION : Cette opération est irréversible sans la clé de chiffrement !

        Returns:
            dict: Résultat de l'activation
        """
        if self.is_encryption_enabled():
            return {
                "success": False,
                "error": "Le chiffrement est déjà activé"
            }

        try:
            # Créer une sauvegarde avant la migration
            from utils.backup import BackupManager
            backup_manager = BackupManager(self.db_path)
            backup_path = backup_manager.create_backup(prefix="pre_encryption_backup")

            # Migrer les données
            migrated = self._migrate_to_encrypted()

            # Marquer le chiffrement comme activé
            self.config_file.write_text("enabled")

            return {
                "success": True,
                "backup_path": str(backup_path),
                "migrated_records": migrated
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def disable_encryption(self):
        """
        Désactive le chiffrement et déchiffre les données existantes

        ATTENTION : Les données seront stockées en clair !

        Returns:
            dict: Résultat de la désactivation
        """
        if not self.is_encryption_enabled():
            return {
                "success": False,
                "error": "Le chiffrement n'est pas activé"
            }

        try:
            # Créer une sauvegarde avant la migration
            from utils.backup import BackupManager
            backup_manager = BackupManager(self.db_path)
            backup_path = backup_manager.create_backup(prefix="pre_decryption_backup")

            # Migrer les données
            decrypted = self._migrate_to_plain()

            # Marquer le chiffrement comme désactivé
            self.config_file.unlink()

            return {
                "success": True,
                "backup_path": str(backup_path),
                "decrypted_records": decrypted
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def _migrate_to_encrypted(self):
        """
        Migre les données en clair vers des données chiffrées

        Returns:
            dict: Nombre d'enregistrements migrés par table
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        migrated = {}

        # Chiffrer les notes d'humeur
        cursor.execute("SELECT id, notes FROM mood WHERE notes IS NOT NULL AND notes != ''")
        mood_notes = cursor.fetchall()
        for note_id, note_text in mood_notes:
            encrypted_note = encrypt_data(note_text)
            cursor.execute("UPDATE mood SET notes = ? WHERE id = ?", (encrypted_note, note_id))
        migrated["mood_notes"] = len(mood_notes)

        # Chiffrer les notes
        cursor.execute("SELECT id, content FROM notes WHERE content IS NOT NULL")
        notes = cursor.fetchall()
        for note_id, content in notes:
            encrypted_content = encrypt_data(content)
            cursor.execute("UPDATE notes SET content = ? WHERE id = ?", (encrypted_content, note_id))
        migrated["notes"] = len(notes)

        conn.commit()
        conn.close()

        return migrated

    def _migrate_to_plain(self):
        """
        Migre les données chiffrées vers des données en clair

        Returns:
            dict: Nombre d'enregistrements déchiffrés par table
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        decrypted = {}

        # Déchiffrer les notes d'humeur
        cursor.execute("SELECT id, notes FROM mood WHERE notes IS NOT NULL")
        mood_notes = cursor.fetchall()
        for note_id, encrypted_note in mood_notes:
            try:
                # Essayer de déchiffrer (si c'est bien chiffré)
                if isinstance(encrypted_note, bytes):
                    plain_note = decrypt_data(encrypted_note)
                    cursor.execute("UPDATE mood SET notes = ? WHERE id = ?", (plain_note, note_id))
            except Exception:
                # Si le déchiffrement échoue, laisser tel quel
                pass
        decrypted["mood_notes"] = len(mood_notes)

        # Déchiffrer les notes
        cursor.execute("SELECT id, content FROM notes WHERE content IS NOT NULL")
        notes = cursor.fetchall()
        for note_id, encrypted_content in notes:
            try:
                if isinstance(encrypted_content, bytes):
                    plain_content = decrypt_data(encrypted_content)
                    cursor.execute("UPDATE notes SET content = ? WHERE id = ?", (plain_content, note_id))
            except Exception:
                pass
        decrypted["notes"] = len(notes)

        conn.commit()
        conn.close()

        return decrypted


def get_encrypted_text(text):
    """
    Retourne le texte chiffré si le chiffrement est activé, sinon le texte en clair

    Args:
        text: Le texte à potentiellement chiffrer

    Returns:
        str ou bytes: Le texte (chiffré ou non)
    """
    config = EncryptionConfig()
    if config.is_encryption_enabled():
        return encrypt_data(text)
    return text


def get_decrypted_text(data):
    """
    Retourne le texte déchiffré si le chiffrement est activé, sinon le texte tel quel

    Args:
        data: Les données à potentiellement déchiffrer

    Returns:
        str: Le texte en clair
    """
    config = EncryptionConfig()
    if config.is_encryption_enabled() and isinstance(data, bytes):
        return decrypt_data(data)
    return str(data) if data else ""
