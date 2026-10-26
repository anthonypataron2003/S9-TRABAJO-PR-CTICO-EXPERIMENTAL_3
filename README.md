# Gestor de Tareas (Django + PostgreSQL)

Proyecto base para la Práctica 3 de GESCONSOF: flujo CI/CD con GitHub Actions y Docker.

## Ejecución local rápida (SQLite, solo para pruebas)

```bash
python -m venv venv
venv\\Scripts\\activate        # Windows  (Linux/Mac: source venv/bin/activate)
pip install -r requirements.txt
set USE_SQLITE=1               # Linux/Mac: export USE_SQLITE=1
python manage.py migrate
python manage.py test
python manage.py runserver
```

## Con PostgreSQL

Variables de entorno: DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT.
