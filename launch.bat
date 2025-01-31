@echo off
REM Vérifie si Python est installé
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo [ERREUR] Python n'est pas installé sur votre ordinateur. Veuillez installer Python.
    pause
    exit /b
)

REM Vérifie si Pipenv est installé
pipenv --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo [INFO] Pipenv n'est pas installé. Installation en cours...
    pip install --user pipenv
    IF ERRORLEVEL 1 (
        echo [ERREUR] L'installation de Pipenv a échoué. Veuillez l'installer manuellement => pip install --user pipenv
        pause
        exit /b
    )
)

REM Activation de l'environnement Pipenv
echo [INFO] Activation de l'environnement Pipenv...
pipenv install

REM Vérifie si manage.py existe dans le répertoire
IF NOT EXIST "manage.py" (
    echo [ERREUR] Le fichier manage.py est introuvable.
    pause
    exit /b
)

REM Lance le serveur
echo [INFO] Lancement du programme...
start python manage.py runserver

REM Timeout pour laisser le temps au serveur de démarrer
timeout /T 3 /NOBREAK >nul

REM Ouverture du navigateur
echo [INFO] Ouverture de l'application sur le navigateur...
start http://127.0.0.1:8000/api/register/

REM Pause
pause