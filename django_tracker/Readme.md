# Financial Tracker Project

## How to Start (Daily Checklist)

1.  **Pull** latest code from GitHub (use Sourcetree).
2.  **Activate** the virtual environment:
    ```powershell
    .\venv\Scripts\Activate.ps1
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

