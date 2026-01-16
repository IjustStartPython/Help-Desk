"""
Module de gestion des backups de la base de données
"""
import os
import shutil
from datetime import datetime
from pathlib import Path


class BackupManager:
    """Gère les backups de la base de données"""

    def __init__(self, db_path, backup_folder="data/backups"):
        """
        Initialise le gestionnaire de backups

        Args:
            db_path: Chemin vers la base de données
            backup_folder: Dossier où stocker les backups
        """
        self.db_path = Path(db_path)
        self.backup_folder = Path(backup_folder)

        # Créer le dossier de backup s'il n'existe pas
        self.backup_folder.mkdir(parents=True, exist_ok=True)

        # Configurer les permissions du dossier (700 = rwx------)
        if os.name != 'nt':  # Unix/Linux/Mac
            os.chmod(self.backup_folder, 0o700)

    def create_backup(self, prefix="backup"):
        """
        Crée un backup de la base de données

        Args:
            prefix: Préfixe pour le nom du fichier de backup

        Returns:
            Path: Chemin vers le fichier de backup créé

        Raises:
            FileNotFoundError: Si la base de données n'existe pas
            IOError: Si la copie échoue
        """
        if not self.db_path.exists():
            raise FileNotFoundError(f"La base de données {self.db_path} n'existe pas")

        # Générer le nom du fichier de backup avec timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"{prefix}_{timestamp}.db"
        backup_path = self.backup_folder / backup_filename

        # Copier la base de données
        shutil.copy2(self.db_path, backup_path)

        # Configurer les permissions du fichier (600 = rw-------)
        if os.name != 'nt':  # Unix/Linux/Mac
            os.chmod(backup_path, 0o600)

        return backup_path

    def list_backups(self):
        """
        Liste tous les backups disponibles

        Returns:
            list: Liste des chemins de fichiers de backup, triés du plus récent au plus ancien
        """
        backups = list(self.backup_folder.glob("*.db"))
        # Trier par date de modification (plus récent en premier)
        backups.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        return backups

    def restore_backup(self, backup_path):
        """
        Restaure un backup de la base de données

        Args:
            backup_path: Chemin vers le fichier de backup à restaurer

        Raises:
            FileNotFoundError: Si le backup n'existe pas
            IOError: Si la restauration échoue
        """
        backup_path = Path(backup_path)

        if not backup_path.exists():
            raise FileNotFoundError(f"Le backup {backup_path} n'existe pas")

        # Créer un backup de la DB actuelle avant de restaurer
        if self.db_path.exists():
            self.create_backup(prefix="pre_restore_backup")

        # Restaurer le backup
        shutil.copy2(backup_path, self.db_path)

        # Configurer les permissions
        if os.name != 'nt':  # Unix/Linux/Mac
            os.chmod(self.db_path, 0o600)

    def clean_old_backups(self, keep_count=10):
        """
        Supprime les anciens backups en ne gardant que les N plus récents

        Args:
            keep_count: Nombre de backups à conserver (défaut: 10)

        Returns:
            int: Nombre de backups supprimés
        """
        backups = self.list_backups()

        # Garder seulement les N plus récents
        backups_to_delete = backups[keep_count:]

        deleted_count = 0
        for backup in backups_to_delete:
            try:
                backup.unlink()
                deleted_count += 1
            except Exception as e:
                print(f"Impossible de supprimer {backup}: {e}")

        return deleted_count

    def get_backup_info(self, backup_path):
        """
        Obtient des informations sur un backup

        Args:
            backup_path: Chemin vers le fichier de backup

        Returns:
            dict: Informations sur le backup (nom, taille, date)
        """
        backup_path = Path(backup_path)

        if not backup_path.exists():
            return None

        stat = backup_path.stat()
        return {
            "name": backup_path.name,
            "path": str(backup_path),
            "size": stat.st_size,
            "size_mb": round(stat.st_size / (1024 * 1024), 2),
            "created": datetime.fromtimestamp(stat.st_mtime),
            "created_str": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        }

    def auto_backup(self, keep_count=10):
        """
        Effectue un backup automatique et nettoie les anciens backups

        Args:
            keep_count: Nombre de backups à conserver

        Returns:
            dict: Résultat du backup (chemin et statistiques)
        """
        try:
            backup_path = self.create_backup(prefix="auto_backup")
            deleted_count = self.clean_old_backups(keep_count)

            return {
                "success": True,
                "backup_path": str(backup_path),
                "deleted_old_backups": deleted_count,
                "total_backups": len(self.list_backups())
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
