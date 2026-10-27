# Notas de despliegue simulado

Proyecto: Gestor de Tareas (Django + PostgreSQL)
Repositorio: https://github.com/anthonypataron2003/S9-TRABAJO-PR-CTICO-EXPERIMENTAL_3.git

## Requisitos
- Docker Desktop instalado y en ejecucion
- Git instalado

## Pasos
1. Crear una carpeta externa al proyecto original:
   ```powershell
   mkdir C:\deploy-simulado
   cd C:\deploy-simulado
   ```
2. Descargar el proyecto:
   ```powershell
   git clone -b ci-setup https://github.com/anthonypataron2003/S9-TRABAJO-PR-CTICO-EXPERIMENTAL_3.git
   cd S9-TRABAJO-PR-CTICO-EXPERIMENTAL_3
   ```
3. Levantar los servicios con Docker Compose:
   ```powershell
   docker compose up --build -d
   ```
4. Verificar los contenedores:
   ```powershell
   docker compose ps
   ```
5. Validar desde el navegador:
   - http://localhost:8000/ (aplicacion Gestor de Tareas)
   - http://localhost:8000/salud/ (debe responder {"status": "ok"})
6. Apagar el entorno:
   ```powershell
   docker compose down
   ```

## Artefacto del pipeline
El flujo de GitHub Actions genera el artefacto imagen-docker-django
(imagen Docker comprimida), disponible en la pestana Actions de cada ejecucion.
Para usarlo en otro equipo:
   ```powershell
   docker load -i django-cicd-image.tar.gz
   ```