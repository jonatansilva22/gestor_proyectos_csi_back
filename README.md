Instrucciones:

Clonar repo con git bash:
-git clone https://github.com/jonatansilva22/gestor_proyectos_csi_back.git
-cd gestor_proyectos_csi_back

Crear y activar un entorno virtual:
-python -m venv env
-env\Scripts\activate

Instalar dependencias del proyecto:
pip install -r requirements.txt

Configurar .env a nivel raiz:
-SECRET_KEY=
-DEBUG=True

-DB_NAME=
-DB_USER=
-DB_PASSWORD=
-DB_HOST=
-DB_PORT=

Abrir terminal del proyecto y poner los siguientes comandos para generar tablas en la DB a partir de los modelos:
-python manage.py makemigrations
-python manage.py migrate

Crear rama:
-git checkout -b nombre-de-su-rama

Subir a github:
-Subir a la rama develop (No a la rama main) 
-En el archivo .gitignore agregar los siguientes archivos para que no se suban:
# Django
*.log
*.pot
*.pyc
__pycache__
db.sqlite3
media/
staticfiles/

# Entornos virtuales
env/
venv/
*.env

# Visual Studio Code
.vscode/

# Archivos de configuración de Windows
Thumbs.db

-No subir archivos que utilicemos todos como el settings.py, urls.py y otros (si modificar esos archivos porque son necesarios para que las funcionalidades que se implementen pero NO subir a github, en su lugar notificarme de los cambios que se hagan en esos archivos para que no haya conflictos al momento de juntarlos).
