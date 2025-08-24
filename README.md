Guía rápida (ver guía completa en `../docs/backend-setup.md`)

1) Clonar y entrar al proyecto:
- `git clone https://github.com/jonatansilva22/gestor_proyectos_csi_back.git`
- `cd gestor_proyectos_csi_back`

2) Crear y activar entorno virtual:
- `python -m venv env`
- Windows: `env\Scripts\activate`
- macOS/Linux: `source env/bin/activate`

3) Instalar dependencias:
- `pip install -r requirements.txt`

4) Configurar `.env` (ver ejemplo y opciones en la guía completa):
- Variables necesarias: `SECRET_KEY`, `DEBUG`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`.

5) Aplicar migraciones:
- `python manage.py makemigrations`
- `python manage.py migrate`

6) Crear datos iniciales (roles, estados, permisos) y usuario admin:
- Sigue los pasos de “Datos iniciales” en `../docs/backend-setup.md` (uso de `manage.py shell`).

7) Ejecutar el servidor:
- `python manage.py runserver 0.0.0.0:8000`

Notas de colaboración:
- Trabajar en ramas feature: `git checkout -b nombre-de-su-rama`.
- Subir a la rama `develop` (no a `main`).
- Mantener `.gitignore` para evitar subir `env/`, `venv/`, `*.env`, `__pycache__/`, `media/`, `staticfiles/`, etc.
- Evitar subir archivos base compartidos (p. ej. `settings.py`, `urls.py`) sin coordinar.

Documentación relacionada:
- Guía de autenticación y perfil: `../docs/autenticacion_y_perfil.md`
