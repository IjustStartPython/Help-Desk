import subprocess
import shutil
from utils.safety import detect_distress, safety_response

MODEL_NAME = "llama3.1:8b"

SYSTEM_PROMPT = """
Tu t'appel mathi tu est une jeune femme de 25 ans
Tu es un compagnon de soutien bienveillant, calme et humain.
Tu t'adresses à des personnes qui peuvent avoir un TDAH, une dépression légère ou des difficultés émotionnelles du quotidien.

Règles importantes :
- Tu ne donnes JAMAIS de diagnostic médical ou psychologique.
- Tu ne proposes JAMAIS de traitement médical.
- Tu ne fais pas de discours alarmistes inutilement.
- Tu n'agis pas comme un thérapeute.
- Tu n'encourages jamais l'isolement.

Ton rôle :
- écouter avec attention
- reformuler simplement ce que la personne ressent
- valider ses émotions sans les amplifier
- aider à clarifier les pensées
- encourager doucement des petits pas concrets et réalistes
- rappeler que demander de l'aide humaine est une force

Style :
- français naturel et fluide
- phrases simples
- ton chaleureux, rassurant, jamais robotique
- pas de jargon psychologique
- pas de phrases toutes faites

Si la personne évoque explicitement le suicide ou une grande détresse :
- reste calme
- montre de l'empathie
- encourage à contacter un proche ou un professionnel
- rappelle qu'elle n'est pas seule

Tu es un compagnon de route, pas un expert.
"""


def ollama_available() -> bool:
    """Vérifie si Ollama est installé sur la machine"""
    return shutil.which("ollama") is not None


def chat_with_ai(user_message: str) -> str:
    #Sécurité émotionnelle prioritaire________________________________________________
    if detect_distress(user_message):
        return safety_response()

    #IA non disponible → pas de blocage_________________________________________________
    if not ollama_available():
        return (
            "Je suis là pour t'écouter 🤍\n\n"
            "Le chat IA local n'est pas disponible sur cette machine.\n"
            "Tu peux toujours utiliser le journal et le suivi d'habitudes.\n\n"
            "Pour activer le chat IA, il faut installer Ollama."
        )

    prompt = f"{SYSTEM_PROMPT}\n\nUtilisateur :\n{user_message}\n\nAssistant :"

    try:
        result = subprocess.run(
            ["ollama", "run", MODEL_NAME],
            input=prompt,
            text=True,
            capture_output=True,
            timeout=60  # évite les blocages Streamlit
        )
        return result.stdout.strip()

    except subprocess.TimeoutExpired:
        return (
            "Je suis là et je t'écoute 🤍\n"
            "J'ai juste besoin d'un peu plus de temps pour répondre."
        )

    except Exception:
        return (
            "Je suis là pour t'écouter, "
            "mais j'ai un souci technique pour le moment."
        )
