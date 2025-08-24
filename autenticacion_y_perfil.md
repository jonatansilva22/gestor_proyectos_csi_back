# Autenticación (Login) y Edición de Perfil – Backend

Esta guía explica cómo autenticar usuarios con JWT y cómo consultar/editar el perfil desde la API.

## Autenticación con JWT
- Endpoint: `POST /api/login/`
- Cuerpo JSON:
  - `identifier`: email o username del usuario
  - `password`: contraseña en texto plano
- Respuesta 200:
```
{
  "message": "Login exitoso",
  "token": "<JWT>",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "first_name": "Admin",
    "last_name": "Local"
  }
}
```
- Autenticación en endpoints protegidos: `Authorization: Bearer <JWT>`
- Expiración del token: 24 horas
- Errores comunes:
  - 401 `{"error": "Credenciales inválidas"}`
  - 400 errores de validación del payload

Ejemplo cURL:
```
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"identifier":"admin","password":"Admin123!"}'
```

## Recursos de Usuario (Perfil)
- Base: ` /api/create-user/ ` (router DRF)
- Autenticación: requerida (JWT)
- Permisos por defecto: `IsAuthenticated` + permisos por nombre (ver sección Permisos)
- Comportamiento por rol:
  - Superadmin (id=2): acceso total, puede eliminar usuarios
  - Admin (id=1): acceso casi total, excepto eliminar usuarios
  - Colaborador (id=3): solo puede ver/editar su propio perfil

### Endpoints
- Listar usuarios: `GET /api/create-user/` (requiere `view_user`)
- Ver un usuario: `GET /api/create-user/{id}/` (requiere `view_user` y, si es colaborador, solo su propio `id`)
- Crear usuario: `POST /api/create-user/` (requiere `add_user`) – destinado a Admin/Superadmin
- Editar usuario (total/parcial):
  - `PUT /api/create-user/{id}/`
  - `PATCH /api/create-user/{id}/` (recomendado)
  - Requiere `change_user` y, si es colaborador, solo su propio `id`
- Eliminar usuario: `DELETE /api/create-user/{id}/` (requiere `delete_user`) – solo Superadmin

### Campos soportados en edición
- Texto: `username`, `first_name`, `last_name`, `email`
- Password: ver “Cambio de contraseña”
- Imagen: `photo` (multipart/form-data)
- Rol: `role` (solo Admin/Superadmin)

### Cambio de contraseña
Existen dos flujos en el serializer de usuario:
1) Cambio seguro por el propio usuario (recomendado):
   - Enviar `current_password` y `new_password` (ambos obligatorios)
   - La nueva contraseña se valida y se guarda hasheada con `bcrypt`
2) Cambio directo por Admin/Superadmin:
   - Enviar `password` (la API la hashea con `bcrypt`)

Ejemplos cURL:
- Actualización de nombre/apellido (JSON):
```
curl -X PATCH http://localhost:8000/api/create-user/3/ \
  -H "Authorization: Bearer <JWT>" \
  -H "Content-Type: application/json" \
  -d '{"first_name":"Carlos","last_name":"Pérez"}'
```

- Cambio de contraseña por el propio usuario (JSON):
```
curl -X PATCH http://localhost:8000/api/create-user/3/ \
  -H "Authorization: Bearer <JWT>" \
  -H "Content-Type: application/json" \
  -d '{"current_password":"MiPass1!","new_password":"MiPass2!"}'
```

- Cambio de contraseña por Admin (JSON):
```
curl -X PATCH http://localhost:8000/api/create-user/7/ \
  -H "Authorization: Bearer <JWT_ADMIN>" \
  -H "Content-Type: application/json" \
  -d '{"password":"NuevaPass123!"}'
```

- Subir/actualizar foto de perfil (multipart/form-data):
```
curl -X PATCH http://localhost:8000/api/create-user/3/ \
  -H "Authorization: Bearer <JWT>" \
  -H "Content-Type: multipart/form-data" \
  -F photo=@"/ruta/a/mi_foto.jpg"
```

### Respuestas y validaciones
- 200: actualización exitosa; el backend puede enviar email de notificación de cambios (si `EMAIL_*` está configurado)
- 400: errores de validación (por ejemplo, nombre vacío o contraseña insegura)
- 401: token ausente/expirado/incorrecto
- 403: falta de permisos (por ejemplo, colaborador intentando editar otro usuario)

### Permisos esperados
- Usuarios: `view_user`, `add_user`, `change_user`, `delete_user`
- El Colaborador (id=3) solo tiene `view_user` y `change_user` por defecto
- Solo Superadmin posee `delete_user`

### Detalles técnicos
- Autenticación DRF: `users.LogIn.authentication.JWTAuthentication`
- Generación del JWT: en la vista `users/LogIn/views.py` con expiración a 24h
- Validación y hashing de password: en `users/serializers.py` usando `bcrypt`
- Restricciones por rol para acceso a perfiles: `users/utils/validations.py` (UserPermissionValidatedViewSet)

---

Con esto puedes iniciar sesión, obtener el token y administrar el perfil respetando roles y permisos.
