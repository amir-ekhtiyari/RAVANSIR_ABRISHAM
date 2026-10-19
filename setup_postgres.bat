@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ============================================
echo   Ravan Seir Abrisham - PostgreSQL setup
echo ============================================
echo.
if exist ".env" goto haveenv
echo No .env file yet - creating one for PostgreSQL on this computer.
set "PGPASS="
set /p "PGPASS=PostgreSQL password for user postgres: "
(
  echo # Local settings for this computer - never commit this file.
  echo DJANGO_DEBUG=1
  echo POSTGRES_DB=ravansir_abrisham
  echo POSTGRES_USER=postgres
  echo POSTGRES_PASSWORD=%PGPASS%
  echo POSTGRES_HOST=localhost
  echo POSTGRES_PORT=5432
) > .env
set "PGPASS="
echo .env created.
echo.
:haveenv
if exist ".venv\Scripts\activate.bat" call ".venv\Scripts\activate.bat"
python -m pip install -r requirements.txt
if errorlevel 1 goto failed
python manage.py setup_postgres
if errorlevel 1 goto failed
echo.
echo Done. Start the site with:  python manage.py runserver
pause
exit /b 0
:failed
echo.
echo Something went wrong - see the message above.
pause
exit /b 1
