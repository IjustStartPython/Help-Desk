"""
Module de validation des entrées utilisateur pour Help-Desk
Se concentre sur les champs texte libres où l'utilisateur peut entrer n'importe quoi
"""
import re
from datetime import datetime, date

class ValidationError(Exception):
    """Exception levée lors d'une erreur de validation"""
    pass


def validate_text_input(text, field_name, min_length=1, max_length=5000, allow_empty=False):
    """
    Valide une entrée de texte pour éviter les chaînes trop longues ou vides

    Args:
        text: Le texte à valider
        field_name: Le nom du champ (pour les messages d'erreur)
        min_length: Longueur minimale
        max_length: Longueur maximale
        allow_empty: Autoriser les chaînes vides

    Returns:
        str: Le texte validé et nettoyé

    Raises:
        ValidationError: Si le texte n'est pas valide
    """
    if text is None:
        if allow_empty:
            return ""
        raise ValidationError(f"{field_name} ne peut pas être vide")

    # Convertir en string et nettoyer les espaces
    text = str(text).strip()

    if not text and not allow_empty:
        raise ValidationError(f"{field_name} ne peut pas être vide")

    if len(text) < min_length and not allow_empty:
        raise ValidationError(f"{field_name} doit contenir au moins {min_length} caractère(s)")

    if len(text) > max_length:
        raise ValidationError(f"{field_name} ne peut pas dépasser {max_length} caractères")

    return text


def validate_task_title(title):
    """
    Valide le titre d'une tâche

    Args:
        title: Le titre à valider

    Returns:
        str: Le titre validé

    Raises:
        ValidationError: Si le titre n'est pas valide
    """
    return validate_text_input(title, "Le titre de la tâche", min_length=1, max_length=200)


def validate_note_content(content):
    """
    Valide le contenu d'une note

    Args:
        content: Le contenu à valider

    Returns:
        str: Le contenu validé

    Raises:
        ValidationError: Si le contenu n'est pas valide
    """
    return validate_text_input(content, "Le contenu de la note", min_length=1, max_length=10000)


def validate_prenom(prenom):
    """
    Valide un prénom

    Args:
        prenom: Le prénom à valider

    Returns:
        str: Le prénom validé

    Raises:
        ValidationError: Si le prénom n'est pas valide
    """
    prenom = validate_text_input(prenom, "Le prénom", min_length=2, max_length=50)

    # Vérifier que le prénom ne contient que des lettres, espaces, tirets et apostrophes
    if not re.match(r"^[a-zA-ZÀ-ÿ\s\-']+$", prenom):
        raise ValidationError("Le prénom ne peut contenir que des lettres, espaces, tirets et apostrophes")

    return prenom


def validate_birth_date(birth_date_str):
    """
    Valide une date de naissance

    Args:
        birth_date_str: La date en format string (YYYY-MM-DD)

    Returns:
        str: La date validée en format ISO

    Raises:
        ValidationError: Si la date n'est pas valide
    """
    try:
        # Parser la date
        birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d").date()

        # Vérifier que la date n'est pas dans le futur
        if birth_date > date.today():
            raise ValidationError("La date de naissance ne peut pas être dans le futur")

        # Vérifier que la personne n'a pas plus de 150 ans
        min_date = date.today().replace(year=date.today().year - 150)
        if birth_date < min_date:
            raise ValidationError("La date de naissance semble incorrecte")

        return birth_date.isoformat()

    except ValueError:
        raise ValidationError("Format de date invalide (utilisez YYYY-MM-DD)")


def validate_mood_notes(notes):
    """
    Valide les notes d'une entrée d'humeur (optionnelles)

    Args:
        notes: Les notes à valider

    Returns:
        str: Les notes validées

    Raises:
        ValidationError: Si les notes ne sont pas valides
    """
    return validate_text_input(notes, "Les notes", min_length=0, max_length=5000, allow_empty=True)
