#!/bin/bash

# Vérifie si Python est installé
if ! command -v python3 &> /dev/null; then
    echo "[ERREUR] Python n'est pas installé sur votre ordinateur. Veuillez installer Python."
    # shellcheck disable=SC2162
    read -p "Appuyez sur Entrée pour quitter..."
    exit 1
fi

# Vérifie si Pipenv est installé
if ! command -v pipenv &> /dev/null; then
    echo "[INFO] Pipenv n'est pas installé. Installation en cours..."
    pip3 install --user pipenv
    # shellcheck disable=SC2181
    if [ $? -ne 0 ]; then
        echo "[ERREUR] L'installation de Pipenv a échoué. Veuillez l'installer manuellement => pip install --user pipenv"
        # shellcheck disable=SC2162
        read -p "Appuyez sur Entrée pour quitter..."
        exit 1
    fi
fi

# Activation de l'environnement Pipenv
echo "[INFO] Activation de l'environnement Pipenv..."
pipenv install

# Vérifie si manage.py existe dans le répertoire
if [ ! -f "manage.py" ]; then
    echo "[ERREUR] Le fichier manage.py est introuvable."
    # shellcheck disable=SC2162
    read -p "Appuyez sur Entrée pour quitter..."
    exit 1
fi

# Lance le serveur
echo "[INFO] Lancement du programme..."
pipenv run python manage.py runserver &

# Attente pour laisser le temps au serveur de démarrer
sleep 3

# Pause
# shellcheck disable=SC2162
read -p "Appuyez sur Entrée pour quitter..."
