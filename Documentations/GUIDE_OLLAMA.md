
# 🤖 Guide d'installation d'Ollama

> Pour activer le chat IA local dans Help-Desk

## Qu'est-ce qu'Ollama ?

**Ollama** est un logiciel qui permet de faire tourner des modèles d'IA (comme ChatGPT) **directement sur ton ordinateur**, sans envoyer tes données sur Internet.

---

## Installation

### Windows

#### 1️⃣ Télécharger Ollama

Va sur [ollama.ai](https://ollama.ai/download) et télécharge l'installeur Windows.

#### 2️⃣ Installer

Double-clique sur le fichier `.exe` et suis les instructions.

#### 3️⃣ Vérifier l'installation

Ouvre un terminal et tape :
```bash
ollama --version
```
### Linux

#### 1️⃣ Installer avec le script officiel

curl -fsSL https://ollama.ai/install.sh | sh

#### 2️⃣ Vérifier

ollama --version

### macOS

#### 1️⃣ Télécharger Ollama
Va sur [ollama.ai](https://ollama.com/download/mac) 

#### 2️⃣ Installer

Glisser dans Applications

#### 3️⃣ Vérifier

ollama --version

## Télécharger le modèle IA
    Help-Desk utilise le modèle llama3.1:8b (recommandé pour un bon équilibre performance/qualité).

#### 1️⃣ Télécharger le modèle

ollama pull llama3.1:8b
    Patience : Le téléchargement peut prendre 5-10 minutes (environ 4,7 Go).

#### 2️⃣ Vérifier que le modèle est prêt

ollama list

## Utilisation avec Help-Desk

### Windows/Linux/Mac :

ollama serve

### Lancer Help-Desk

streamlit run main.py

    Va dans "Chat IA" → Ça devrait fonctionner !

## Dépannage

1. Erreur "Connection refused"

Problème : Ollama n'est pas démarré.

Solution :
```bash
ollama serve
```
Laisse ce terminal ouvert.

2. Le modèle ne répond pas

Problème : Le modèle n'est pas téléchargé.

Solution :
```bash
ollama pull llama3.1:8b
```

3. Performances lentes

Problème : Ton PC est trop ancien pour faire tourner l'IA localement.

Solutions :

    Utilise un modèle plus léger :
```bash
ollama pull llama3.1:3b
```

## Configuration avancée

### Changer de modèle
Pour utiliser un autre modèle (ex: mistral), modifie utils/ollama_client.py :

```bash
MODEL = "mistral"  # Au lieu de llama3.1:8b
```

### Modèles disponibles
Liste complète : ollama.ai/library
Recommandations :

    llama3.1:8b (défaut, bon équilibre)
    llama3.1:3b (plus rapide, moins précis)
    mistral (alternatif, très performant)

## Désinstaller Ollama

### Windows
Panneau de configuration → Désinstaller un programme → Ollama

### Linux 
```bash
sudo systemctl stop ollama
sudo systemctl disable ollama
sudo rm /usr/local/bin/ollama
```

### macOS
Glisse Ollama depuis Applications vers la Corbeille.

## Ressources

    Site officiel : ollama.ai
    Documentation : github.com/ollama/ollama







