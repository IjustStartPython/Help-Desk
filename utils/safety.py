def detect_distress(message: str) -> bool:
    keywords = ["suicide", "je veux mourir", "inutile", "je veux en finir", "désespéré"]
    msg_lower = message.lower()
    return any(k in msg_lower for k in keywords)

def safety_response():
    return (" Je vois que tu vis un moment difficile."
            " Je suis là pour t'écouter, mais si tu es dans cette détresse parle en à un proche ou un professionnel de santé."
            " Tu n'es pas seul, crois-moi.")