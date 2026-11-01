@echo off
setlocal
cd /d "%~dp0"
echo BYTE NDT - NOZZLE REV0.4
if exist ".venv\Scripts\python.exe" goto dependencies
where py >nul 2>nul
if errorlevel 1 goto try_python
py -3 -m venv .venv
if errorlevel 1 goto failed
goto dependencies
:try_python
where python >nul 2>nul
if errorlevel 1 goto no_python
python -m venv .venv
if errorlevel 1 goto failed
:dependencies
echo Verification des dependances...
.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
if errorlevel 1 goto failed
echo Lancement du twin. Garder cette fenetre ouverte.
.venv\Scripts\python.exe -m streamlit run app.py --browser.gatherUsageStats false
if errorlevel 1 goto failed
goto end
:no_python
echo Python est introuvable. Installer Python 3.12 ou plus recent puis relancer ce fichier.
goto failed
:failed
echo Le lancement a echoue. Photographier le message ci-dessus pour le diagnostic.
pause
:end
endlocal
