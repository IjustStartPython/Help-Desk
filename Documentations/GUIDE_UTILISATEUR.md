
# 📖 Guide Utilisateur Help-Desk

> Guide pas-à-pas pour installer et utiliser Help-Desk

## 🎯 Qu'est-ce que Help-Desk ?

Help-Desk est un **compagnon personnel local** qui t'aide à :
-  Suivre tes émotions jour après jour
-  Gérer tes habitudes et tâches
-  Rester concentré (mode focus TDAH)
-  Discuter avec une IA bienveillante (100% local)
-  Visualiser tes progrès

**Important :** Aucune donnée n'est envoyée sur Internet. Tout reste sur ton ordinateur.

---

##  Installation

### Prérequis

- **Windows 10/11**, **Linux**, ou **macOS**
- **Python 3.13 ou supérieur**
- (Optionnel) **Ollama** pour le chat IA

### Étapes

#### 1️⃣ Installer Python

**Windows :**
1. Télécharge Python depuis [python.org](https://www.python.org/downloads/)
2. ⚠️ Coche "Add Python to PATH" pendant l'installation
3. Vérifie : ouvre un terminal et tape `python --version`

**Linux/Mac :**
```bash
# Déjà installé sur la plupart des systèmes
python3 --version
```
#### 2️⃣ Télécharger Help-Desk
1. Avec Git(recommandé)
```bash
git clone https://github.com/IjustStartPython/Help-Desk.git
cd Help-Desk
```

2. Sans Git
   - Va sur https://github.com/IjustStartPython/Help-Desk.git
   - Clique sur "Code" -> "Download ZIP"
   - Décompresse le fichier
   - Ouvre le terminal dans le dossier

#### 3️⃣ Créer un environnement virtuel
# Windows
```bash
python -m venv venv
venv\Scripts\activate
```

# Linux/Mac
```bash
python3 -m venv venv
source venv/bin/activate
```

Tu verras (venv) apparaître dans ton terminal.

#### 4️⃣ Installer les dépendances
```bash
pip install -r requirements.txt
```

#### 5️⃣ (Optionnel) Installer Ollama pour le chat IA
Si tu veux l'IA locale, suis GUIDE_OLLAMA.md

### Premier lancement
```bash
streamlit run main.py
```
## Utilisation 

### Créer ton profil
   - Entre ton prénom
   - Choisis ta date de naissance
   - Ajoute des tags personnels (ex: "TDAH", "Anxiété", "Sport")
   - Clique sur "Créer mon profil"
  
### Utilisation quotidienne

1. Enregistre ton humeur 
   - Va dans "Journal d'humeur"
   - Sélectionne un émoji
   - Ajoute une note (optionnel)
   - Clique sur "Enregistrer"
Tu gagnes des points à chaque enregistrement !

2. Gerer les tasks
    - Rentre une tash a faire
    - Avant de cocher la case pour terminer la tache ajoute le nombres d'heure
    - Suis tes séries 

3. Utiliser le mode focus
    - Vas dans le menu à droite "Mode Focus"
    - Clique sur "Démarrer"
    - Concentre -toi pendant 25 minutes
    - L'écran devient immersif avec des encouragements

4. Discuter avec l'IA
    - Va dans "mathi"
    - Tape ton messsage 
    - L'assistant répond de manière bienveillante

5. Consulter tes statistiques
   - Va dans "Dashboard"
   - Visualise tes points, séries, badges
   - Vois ton évolution sur le temps.

6. Exporter tes données 
    - Va dans "Plus"
    - Clique sur "Exporter en PDF" ou "Excel"
    - Partage avec un professionnel si besoin

## Sécurité et confidentialité
Où sont mes données ?

- Windows : C:\Users\TonNom\AppData\Roaming\Help-Desk\

- Linux/Mac : ~/.local/share/Help-Desk/

### Activer le chiffrement (optionnel)
    1. Va dans "Plus"
    2. Clique sur "Activer le chiffrement"
    3. ⚠️ Important : Si tu perds la clé, tes données sont perdues !


#### Sauvegardes
- Automatiques : À chaque démarrage
- Manuelles : Dans "Paramètres" → "Sauvegardes"

