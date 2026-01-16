"""
Tests unitaires pour le module de validation
"""
import pytest
from datetime import date, timedelta
from utils.validation import (
    validate_text_input,
    validate_task_title,
    validate_note_content,
    validate_prenom,
    validate_birth_date,
    validate_mood_notes,
    ValidationError
)


class TestTextValidation:
    """Tests pour la validation de texte générique"""

    def test_validate_text_input_valid(self):
        """Test avec une entrée valide"""
        result = validate_text_input("Test valide", "Champ")
        assert result == "Test valide"

    def test_validate_text_input_strips_whitespace(self):
        """Test que les espaces sont nettoyés"""
        result = validate_text_input("  Test  ", "Champ")
        assert result == "Test"

    def test_validate_text_input_empty_not_allowed(self):
        """Test qu'une chaîne vide est rejetée quand allow_empty=False"""
        with pytest.raises(ValidationError):
            validate_text_input("", "Champ", allow_empty=False)

    def test_validate_text_input_empty_allowed(self):
        """Test qu'une chaîne vide est acceptée quand allow_empty=True"""
        result = validate_text_input("", "Champ", allow_empty=True)
        assert result == ""

    def test_validate_text_input_too_long(self):
        """Test qu'une chaîne trop longue est rejetée"""
        with pytest.raises(ValidationError):
            validate_text_input("x" * 101, "Champ", max_length=100)

    def test_validate_text_input_too_short(self):
        """Test qu'une chaîne trop courte est rejetée"""
        with pytest.raises(ValidationError):
            validate_text_input("ab", "Champ", min_length=3)

    def test_validate_text_input_none_not_allowed(self):
        """Test que None est rejeté quand allow_empty=False"""
        with pytest.raises(ValidationError):
            validate_text_input(None, "Champ", allow_empty=False)

    def test_validate_text_input_none_allowed(self):
        """Test que None est converti en "" quand allow_empty=True"""
        result = validate_text_input(None, "Champ", allow_empty=True)
        assert result == ""


class TestTaskValidation:
    """Tests pour la validation des tâches"""

    def test_validate_task_title_valid(self):
        """Test avec un titre valide"""
        result = validate_task_title("Faire les courses")
        assert result == "Faire les courses"

    def test_validate_task_title_empty(self):
        """Test qu'un titre vide est rejeté"""
        with pytest.raises(ValidationError):
            validate_task_title("")

    def test_validate_task_title_too_long(self):
        """Test qu'un titre trop long est rejeté"""
        with pytest.raises(ValidationError):
            validate_task_title("x" * 201)


class TestNoteValidation:
    """Tests pour la validation des notes"""

    def test_validate_note_content_valid(self):
        """Test avec une note valide"""
        result = validate_note_content("Aujourd'hui je me sens bien")
        assert result == "Aujourd'hui je me sens bien"

    def test_validate_note_content_empty(self):
        """Test qu'une note vide est rejetée"""
        with pytest.raises(ValidationError):
            validate_note_content("")

    def test_validate_note_content_too_long(self):
        """Test qu'une note trop longue est rejetée"""
        with pytest.raises(ValidationError):
            validate_note_content("x" * 10001)


class TestPrenomValidation:
    """Tests pour la validation du prénom"""

    def test_validate_prenom_valid(self):
        """Test avec des prénoms valides"""
        assert validate_prenom("Jean") == "Jean"
        assert validate_prenom("Marie-Claire") == "Marie-Claire"
        assert validate_prenom("O'Connor") == "O'Connor"
        assert validate_prenom("José") == "José"

    def test_validate_prenom_too_short(self):
        """Test qu'un prénom trop court est rejeté"""
        with pytest.raises(ValidationError):
            validate_prenom("A")

    def test_validate_prenom_invalid_characters(self):
        """Test que les caractères invalides sont rejetés"""
        with pytest.raises(ValidationError):
            validate_prenom("Jean123")

    def test_validate_prenom_empty(self):
        """Test qu'un prénom vide est rejeté"""
        with pytest.raises(ValidationError):
            validate_prenom("")


class TestBirthDateValidation:
    """Tests pour la validation de la date de naissance"""

    def test_validate_birth_date_valid(self):
        """Test avec une date valide"""
        yesterday = (date.today() - timedelta(days=365)).isoformat()
        result = validate_birth_date(yesterday)
        assert result == yesterday

    def test_validate_birth_date_future(self):
        """Test qu'une date future est rejetée"""
        tomorrow = (date.today() + timedelta(days=1)).isoformat()
        with pytest.raises(ValidationError):
            validate_birth_date(tomorrow)

    def test_validate_birth_date_too_old(self):
        """Test qu'une date trop ancienne est rejetée"""
        too_old = (date.today() - timedelta(days=365 * 151)).isoformat()
        with pytest.raises(ValidationError):
            validate_birth_date(too_old)

    def test_validate_birth_date_invalid_format(self):
        """Test qu'un format invalide est rejeté"""
        with pytest.raises(ValidationError):
            validate_birth_date("31/12/2000")


class TestMoodNotesValidation:
    """Tests pour la validation des notes d'humeur"""

    def test_validate_mood_notes_valid(self):
        """Test avec des notes valides"""
        result = validate_mood_notes("Je me sens bien aujourd'hui")
        assert result == "Je me sens bien aujourd'hui"

    def test_validate_mood_notes_empty(self):
        """Test que les notes vides sont acceptées"""
        result = validate_mood_notes("")
        assert result == ""

    def test_validate_mood_notes_too_long(self):
        """Test que les notes trop longues sont rejetées"""
        with pytest.raises(ValidationError):
            validate_mood_notes("x" * 5001)
