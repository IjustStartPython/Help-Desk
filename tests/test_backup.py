"""
Tests unitaires pour le module de backup
"""
import pytest
import tempfile
import shutil
import time
from pathlib import Path
from utils.backup import BackupManager


@pytest.fixture
def temp_db():
    """Crée une base de données temporaire pour les tests"""
    temp_dir = tempfile.mkdtemp()
    db_path = Path(temp_dir) / "test.db"

    # Créer un fichier de test
    db_path.write_text("test database content")

    yield db_path

    # Nettoyer après le test
    shutil.rmtree(temp_dir)


@pytest.fixture
def backup_manager(temp_db):
    """Crée un gestionnaire de backup pour les tests"""
    backup_folder = temp_db.parent / "backups"
    return BackupManager(temp_db, backup_folder)


class TestBackupManager:
    """Tests pour le gestionnaire de backups"""

    def test_init_creates_backup_folder(self, temp_db):
        """Test que le dossier de backup est créé"""
        backup_folder = temp_db.parent / "backups"
        manager = BackupManager(temp_db, backup_folder)

        assert backup_folder.exists()
        assert backup_folder.is_dir()

    def test_create_backup(self, backup_manager, temp_db):
        """Test la création d'un backup"""
        backup_path = backup_manager.create_backup(prefix="test")

        assert backup_path.exists()
        assert backup_path.suffix == ".db"
        assert "test_" in backup_path.name
        # Vérifier que le contenu est identique
        assert backup_path.read_text() == temp_db.read_text()

    def test_create_backup_nonexistent_db(self, backup_manager):
        """Test que la création échoue si la DB n'existe pas"""
        backup_manager.db_path = Path("nonexistent.db")

        with pytest.raises(FileNotFoundError):
            backup_manager.create_backup()

    def test_list_backups(self, backup_manager):
        """Test le listage des backups"""
        # Créer plusieurs backups avec délai pour garantir des timestamps différents
        backup_manager.create_backup(prefix="backup1")
        time.sleep(0.01)
        backup_manager.create_backup(prefix="backup2")
        time.sleep(0.01)
        backup_manager.create_backup(prefix="backup3")

        backups = backup_manager.list_backups()

        assert len(backups) == 3
        # Vérifier que les backups sont triés du plus récent au plus ancien
        for i in range(len(backups) - 1):
            assert backups[i].stat().st_mtime >= backups[i + 1].stat().st_mtime

    def test_list_backups_empty(self, backup_manager):
        """Test le listage quand il n'y a pas de backups"""
        backups = backup_manager.list_backups()
        assert len(backups) == 0

    def test_restore_backup(self, backup_manager, temp_db):
        """Test la restauration d'un backup"""
        # Créer un backup
        backup_path = backup_manager.create_backup()

        # Modifier la DB originale
        temp_db.write_text("modified content")

        # Restaurer le backup
        backup_manager.restore_backup(backup_path)

        # Vérifier que la DB est restaurée
        assert temp_db.read_text() == "test database content"

    def test_restore_backup_nonexistent(self, backup_manager):
        """Test que la restauration échoue si le backup n'existe pas"""
        with pytest.raises(FileNotFoundError):
            backup_manager.restore_backup("nonexistent_backup.db")

    def test_clean_old_backups(self, backup_manager):
        """Test le nettoyage des anciens backups"""
        # Créer 15 backups avec de petits délais
        for i in range(15):
            backup_manager.create_backup(prefix=f"backup{i}")
            time.sleep(0.001)  # Très petit délai

        # Garder seulement les 5 plus récents
        deleted = backup_manager.clean_old_backups(keep_count=5)

        assert deleted == 10
        assert len(backup_manager.list_backups()) == 5

    def test_clean_old_backups_less_than_keep_count(self, backup_manager):
        """Test qu'aucun backup n'est supprimé si moins que keep_count"""
        # Créer 3 backups avec des noms différents pour éviter les collisions de timestamp
        backup_manager.create_backup(prefix="backup1")
        time.sleep(0.01)  # Petit délai pour éviter les collisions de timestamp
        backup_manager.create_backup(prefix="backup2")
        time.sleep(0.01)
        backup_manager.create_backup(prefix="backup3")

        # Vérifier qu'on a bien 3 backups
        backups_before = len(backup_manager.list_backups())
        assert backups_before == 3

        # Garder 10 backups
        deleted = backup_manager.clean_old_backups(keep_count=10)

        assert deleted == 0
        assert len(backup_manager.list_backups()) == 3

    def test_get_backup_info(self, backup_manager):
        """Test l'obtention d'informations sur un backup"""
        backup_path = backup_manager.create_backup(prefix="test")
        info = backup_manager.get_backup_info(backup_path)

        assert info is not None
        assert info["name"] == backup_path.name
        assert info["path"] == str(backup_path)
        assert info["size"] > 0
        assert "created" in info
        assert "created_str" in info

    def test_get_backup_info_nonexistent(self, backup_manager):
        """Test que None est retourné pour un backup inexistant"""
        info = backup_manager.get_backup_info("nonexistent.db")
        assert info is None

    def test_auto_backup(self, backup_manager):
        """Test le backup automatique"""
        result = backup_manager.auto_backup(keep_count=5)

        assert result["success"] is True
        assert "backup_path" in result
        assert result["total_backups"] == 1
        assert result["deleted_old_backups"] == 0

    def test_auto_backup_with_cleanup(self, backup_manager):
        """Test le backup automatique avec nettoyage"""
        # Créer 10 backups existants avec de petits délais
        for i in range(10):
            backup_manager.create_backup(prefix=f"old{i}")
            time.sleep(0.001)

        # Faire un auto backup qui garde seulement 5 backups
        result = backup_manager.auto_backup(keep_count=5)

        assert result["success"] is True
        assert result["total_backups"] == 5
        assert result["deleted_old_backups"] == 6
