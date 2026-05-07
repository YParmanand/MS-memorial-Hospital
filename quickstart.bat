@echo off
echo ============================================================
echo MS MEMORIAL NETRALAYA HOSPITAL - QUICK START SCRIPT
echo ============================================================
echo.

echo Step 1: Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error installing dependencies!
    pause
    exit /b 1
)
echo.

echo Step 2: Running migrations...
python manage.py makemigrations
python manage.py migrate
if %errorlevel% neq 0 (
    echo Error running migrations!
    pause
    exit /b 1
)
echo.

echo Step 3: Creating sample data...
python setup.py
if %errorlevel% neq 0 (
    echo Error creating sample data!
    pause
    exit /b 1
)
echo.

echo Step 4: Collecting static files...
python manage.py collectstatic --noinput
echo.

echo ============================================================
echo SETUP COMPLETE!
echo ============================================================
echo.
echo You can now start the server with:
echo python manage.py runserver
echo.
echo Then visit: http://localhost:8000/
echo.
echo Default Login Credentials:
echo Admin: admin@hospital.com / admin123
echo Doctor: madhav@hospital.com / doctor123
echo Patient: patient@hospital.com / patient123
echo.
pause
