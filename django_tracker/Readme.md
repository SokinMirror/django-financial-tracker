# Financial Tracker Project

## How to Start (Daily Checklist)

1.  **Pull** latest code from GitHub (use Sourcetree).

2.  **Activate** the virtual environment:
    ```powershell
    ./venv/scripts/activate.ps1
    ```
3.  **Run** the server:
    ```powershell
    python manage.py runserver
    ```

## Other Useful Commands

**When models.py changes:**
```powershell
python manage.py makemigrations
python manage.py migrate

**When installing a new package:**
pip install <package-name>
pip freeze > requirements.txt

## Install PostgreSQL

    Install PostgreSQL (Step 1).
    Create the financial_tracker database using pgAdmin (Step 2).
    Open Sourcetree and "Pull" your project. This will download the new requirements.txt and settings.py.
    Open the project in VS Code and open the terminal.
    Create the venv: python -m venv venv
    Activate it: .\venv\Scripts\Activate.ps1
    Install packages: pip install -r requirements.txt (This will now install psycopg2-binary).
    Run migrate: python manage.py migrate (This builds the tables on your work PC's database).
    Create a superuser for your work database: python manage.py createsuperuser
    Run server: python manage.py runserver

