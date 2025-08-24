# Guía para correr el backend (Django)

Esta guía describe cómo levantar el backend de manera confiable en local, incluyendo requisitos, configuración de entorno, base de datos, datos iniciales y prueba de acceso.

## Requisitos
- Python 3.11 o 3.12.
- MySQL 8.x o MariaDB 10.x (puerto por defecto 3306; en este proyecto el `.env` de ejemplo usa 3307).
- Pip + venv.
- Compiladores/bibliotecas nativas para `mysqlclient` y `Pillow`:
  - Windows: Microsoft C++ Build Tools (VS 2019+). Si falla `mysqlclient`, instalar también MySQL Connector/C.
  - Linux: `libmysqlclient-dev` o `default-libmysqlclient-dev`, `build-essential`, `python3-dev`.
  - macOS: Xcode Command Line Tools, y MySQL instalado (Homebrew recomendado).

## Estructura y stack
- Framework: Django 5.2 + Django REST Framework.
- Autenticación: JWT personalizada (`users.LogIn.authentication.JWTAuthentication`).
- Base de datos: MySQL/MariaDB.
- Archivos relevantes:
  - `gestor_proyectos_csi_back/manage.py`
  - `gestor_proyectos_csi_back/project_manager/settings.py`
  - `.env` en la raíz de `gestor_proyectos_csi_back/` (usado por `python-decouple`).

## Variables de entorno (`.env`)
Crear un archivo `.env` dentro de `gestor_proyectos_csi_back/` con este contenido (ajusta credenciales/puertos):

```
# Django
SECRET_KEY=django-insecure-csi-proyecto-gestor-2024-dev-key-change-for-production
DEBUG=True

# MySQL/MariaDB
DB_NAME=gestor_proyectos_csi
DB_USER=root
DB_PASSWORD=tu-password
DB_HOST=localhost
DB_PORT=3306

# Email (opcional, para notificaciones)
EMAIL_HOST=smtp-mail.outlook.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@outlook.com
EMAIL_HOST_PASSWORD=your-email-password

# CORS (informativo)
FRONTEND_URL=http://localhost:5173
```

Notas:
- `DEBUG=True` para desarrollo local.
- Si tu servidor MySQL escucha en otro puerto (p. ej. 3307), actualízalo en `DB_PORT`.

## Preparar base de datos
1) Crear base de datos y usuario (ejemplo MySQL):
```
CREATE DATABASE gestor_proyectos_csi CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'root'@'localhost' IDENTIFIED BY 'tu-password'; -- si no existe
GRANT ALL PRIVILEGES ON gestor_proyectos_csi.* TO 'root'@'localhost';
FLUSH PRIVILEGES;
```

2) Crear y activar entorno virtual, instalar dependencias:
```
cd gestor_proyectos_csi_back
python -m venv env
# Windows
env\Scripts\activate
# macOS/Linux
# source env/bin/activate
pip install -r requirements.txt
```

3) Aplicar migraciones:
```
python manage.py makemigrations
python manage.py migrate
```

## Datos iniciales (roles, estados, permisos y usuario admin)
El proyecto usa catálogos que deben existir antes de usar la API:
- 3 roles con IDs convencionales: 1=Admin, 2=Superadmin, 3=Colaborador.
- 3 estados de proyecto con IDs fijos (usados por el dashboard): 1=Activo, 2=Inactivo, 3=Completado.
- Permisos utilizados por las vistas.
- Un usuario inicial con rol Admin y contraseña hasheada con bcrypt.

La forma más simple es usando el shell de Django (ORM):

```
python manage.py shell
```
Dentro del shell, ejecuta (puedes pegar todo el bloque):

```
from users.models import RoleType, User
from projects.models import StatusType
from permissions.models import Permission, RolePermission
import bcrypt

# 1) Roles
roles = [
    (1, 'Admin'),
    (2, 'Superadmin'),
    (3, 'Colaborador'),
]
for rid, name in roles:
    RoleType.objects.update_or_create(id=rid, defaults={'name': name})

# 1b) Estados de proyecto (IDs fijos esperados por el dashboard)
statuses = [
    (1, 'Activo'),
    (2, 'Inactivo'),
    (3, 'Completado'),
]
for sid, name in statuses:
    StatusType.objects.update_or_create(id=sid, defaults={'name': name})

# 2) Permisos usados por las vistas (mínimo sugerido)
perm_names = [
    # usuarios
    'view_user','add_user','change_user','delete_user',
    # proyectos
    'view_projects','add_project','change_project','delete_project',
    # áreas
    'view_areas','add_area','change_area','delete_area',
    # repositorios
    'view_repository','add_repository','change_repository','delete_repository',
    # grupos de trabajo
    'view_groups','add_group','change_group','delete_group',
]
perms = {}
for name in perm_names:
    p, _ = Permission.objects.get_or_create(name=name)
    perms[name] = p

# 3) Asignar todos los permisos al rol Admin (id=1)
admin_role = RoleType.objects.get(id=1)
for p in perms.values():
    RolePermission.objects.get_or_create(role=admin_role, permission=p)

# 4) Crear usuario admin con contraseña hasheada (bcrypt)
raw_password = 'Admin123!'
hashed = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
admin_user, created = User.objects.get_or_create(
    username='admin',
    defaults={
        'first_name': 'Admin',
        'last_name': 'Local',
        'email': 'admin@example.com',
        'password': hashed,
        'role': admin_role,
    }
)
print('Usuario admin listo. Password =', raw_password)
```

Luego sal del shell (`exit()`).

4) Actualizar permisos del colaborador (opcional):
```
python manage.py update_colaborador_permissions
```

Importante:
- No uses el archivo `update_colaborador_permissions.sql` en MySQL: contiene sintaxis `ON CONFLICT` de PostgreSQL y fallará. Usa el comando de management anterior.
- El sitio de admin de Django está deshabilitado en `settings.py`; por eso la creación del usuario inicial se hace con el shell.

## Ejecutar el servidor
Con el entorno activo dentro de `gestor_proyectos_csi_back/`:
```
python manage.py runserver 0.0.0.0:8000
```
El backend expone la API bajo `/api/`.

En modo `DEBUG`, los archivos de `MEDIA` se sirven desde `http://localhost:8000/media/`.

## Probar login y llamadas autenticadas
1) Login (JWT):
```
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"identifier":"admin","password":"Admin123!"}'
```
Copia el valor de `token` de la respuesta.

2) Llamada autenticada de ejemplo (listar usuarios):
```
curl http://localhost:8000/api/create-user/ \
  -H "Authorization: Bearer TU_TOKEN_AQUI"
```
Ten en cuenta que el acceso a vistas requiere que el rol tenga los permisos correspondientes.

## Problemas comunes y soluciones
- Error al instalar `mysqlclient`:
  - Windows: instala Microsoft C++ Build Tools; si persiste, instala MySQL Connector/C.
  - Linux: `sudo apt-get install default-libmysqlclient-dev build-essential python3-dev`.
  - macOS: `brew install mysql` y asegúrate de tener las herramientas de línea de comandos de Xcode.
- Puerto/credenciales de MySQL incorrectos: ajusta `DB_HOST/DB_PORT/DB_USER/DB_PASSWORD` en `.env`.
- No puedes crear usuarios por API al inicio: primero crea roles/usuario admin vía shell; luego autentícate y usa los endpoints.
- Errores de correo: el backend intenta enviar emails en algunos flujos (p. ej., cambios de usuario). Puedes dejar los valores de email de prueba o configurar cuentas reales.

---

Con esto deberías poder correr el backend sin errores y con un flujo mínimo de autenticación listo.

## Atajo: script de datos iniciales
Después de aplicar migraciones, puedes cargar todo lo necesario con un solo comando desde `gestor_proyectos_csi_back/`:

```
python cargar_datos_iniciales.py
```

Esto creará roles (1,2,3), estados (1,2,3), permisos, asignará todos al rol Admin y generará el usuario `admin` con contraseña `Admin123!`.
