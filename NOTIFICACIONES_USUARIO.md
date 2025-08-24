# 📧 Sistema de Notificaciones por Cambios de Usuario

## 📋 Resumen

Se implementó un sistema completo de notificaciones por correo electrónico que alerta a los usuarios cuando se realizan cambios en sus datos personales. El sistema diferencia entre cambios realizados por el propio usuario vs cambios realizados por administradores, enviando notificaciones personalizadas con información de seguridad apropiada.

## 🎯 Objetivo

Mejorar la seguridad y transparencia del sistema notificando automáticamente a los usuarios sobre cualquier modificación en su perfil, permitiendo detectar cambios no autorizados y mantener un registro de auditoría.

## ⚡ Funcionalidades Implementadas

### 🔔 **Notificaciones Automáticas**
- **Detección automática** de cambios en campos críticos
- **Envío inmediato** de correos tras cualquier modificación
- **Diferenciación** entre cambios propios vs administrativos
- **Mensajes personalizados** según el tipo de cambio

### 📊 **Campos Monitoreados**
El sistema rastrea cambios en los siguientes campos:
- ✅ **Contraseña** - Notifica cambios de password
- ✅ **Email** - Cambios en correo electrónico  
- ✅ **Username** - Modificaciones al nombre de usuario
- ✅ **Nombre** (`first_name`) - Cambios en nombre personal
- ✅ **Apellido** (`last_name`) - Cambios en apellido
- ✅ **Rol** (`role`) - Cambios de permisos/rol del usuario
- ✅ **Foto de perfil** (`photo`) - Actualizaciones de imagen

### 📨 **Tipos de Notificación**

#### 👤 **Cambios Realizados por el Usuario**
```
Asunto: "Confirmación de cambios en tu perfil"

Hola [username],

Se han realizado cambios en tu perfil:

• [Lista de cambios específicos]

Si no realizaste estos cambios, por favor contacta al 
administrador del sistema inmediatamente.

Saludos,
CSI PRO.
```

#### 👨‍💼 **Cambios Realizados por Administrador**
```
Asunto: "Cambios en tu perfil realizados por administrador"

Hola [username],

Un administrador ([admin_username]) ha realizado cambios en tu perfil:

• [Lista de cambios específicos]

Si no esperabas estos cambios, por favor contacta al 
administrador del sistema.

Saludos,
CSI PRO.
```

## 🏗️ Arquitectura de la Implementación

### 📁 **Archivos Modificados**

#### 1. `/users/Crear_Usuario/views.py`
**Cambios realizados:**
- ➕ **Nueva función**: `notificar_cambios_usuario()`
- ➕ **Nuevo método**: `perform_update()` en `UserViewSet`
- 🔧 **Actualizaciones**: Agregados parsers para manejo de archivos

**Funcionalidad:**
```python
def notificar_cambios_usuario(user_email, username, cambios_realizados, 
                            cambio_por_admin=False, admin_username=None):
    """
    Función principal de notificación que:
    - Construye mensaje personalizado según tipo de cambio
    - Genera lista detallada de modificaciones
    - Incluye notas de seguridad apropiadas
    - Envía correo usando Django mail
    """
```

#### 2. `/users/Crear_Usuario/serializers.py`
**Cambios realizados:**
- ➕ **Nuevos campos**: `current_password`, `new_password`, `role_name`
- 🔧 **Método actualizado**: `update()` con rastreo de cambios
- ➕ **Nuevas validaciones**: Username, email, nombres con lógica de actualización
- ➕ **Sistema de detección**: Almacena cambios en `self.cambios_realizados`

**Lógica de rastreo:**
```python
# Rastrear cambios para notificaciones
cambios_realizados = {}

for attr, value in validated_data.items():
    old_value = getattr(instance, attr, None)
    if old_value != value:
        # Almacenar cambio con valor anterior y nuevo
        cambios_realizados[attr] = {
            'anterior': old_value,
            'nuevo': value
        }
```

#### 3. `/users/views.py`
**Cambios realizados:**
- ➕ **Nueva función**: `notificar_cambios_usuario()` (duplicada para ViewSet general)
- ➕ **Nuevo método**: `perform_update()` en `UserListCreateView`
- 🔧 **Lógica**: Detección de cambios por admin vs usuario

#### 4. `/users/serializers.py`
**Cambios realizados:**
- ➕ **Nuevos campos**: Soporte para cambio de contraseña seguro
- 🔧 **Método actualizado**: `update()` con notificaciones
- 🔒 **Seguridad**: Hashing con bcrypt para contraseñas
- 📊 **Rastreo**: Sistema de cambios integrado

## 🔧 Detalles Técnicos

### 🔄 **Flujo de Funcionamiento**

1. **Recepción de Cambios**: API recibe solicitud de actualización de usuario
2. **Validación**: Serializer valida datos y detecta cambios
3. **Almacenamiento**: Se guardan cambios en `cambios_realizados`
4. **Identificación**: ViewSet determina si cambio es por admin o usuario
5. **Notificación**: Se envía correo personalizado al usuario
6. **Logging**: Se registra resultado del envío

### 🔐 **Manejo de Contraseñas**

El sistema maneja dos flujos para cambio de contraseñas:

#### **Flujo Usuario (Cambio Seguro)**
```python
# Requiere contraseña actual + nueva contraseña
current_password = validated_data.pop('current_password', None)
new_password = validated_data.pop('new_password', None)

# Verificación de contraseña actual
if instance.password.startswith('$2'):
    ok = bcrypt.checkpw(current_password.encode('utf-8'), 
                       instance.password.encode('utf-8'))
```

#### **Flujo Admin (Cambio Directo)**
```python
# Admin puede cambiar password directamente
if 'password' in validated_data:
    raw = validated_data.pop('password')
    hashed = bcrypt.hashpw(raw.encode('utf-8'), bcrypt.gensalt())
    instance.password = hashed.decode('utf-8')
```

### 🎨 **Formato de Mensaje**

El sistema construye mensajes dinámicos según los cambios:

```python
cambios_texto = []
for campo, info in cambios_realizados.items():
    if campo == 'password':
        cambios_texto.append("• Contraseña actualizada")
    elif campo == 'email':
        cambios_texto.append(f"• Correo electrónico: {info['anterior']} → {info['nuevo']}")
    elif campo == 'role':
        cambios_texto.append(f"• Rol: {info['anterior']} → {info['nuevo']}")
    # ... otros campos
```

## 🛡️ Seguridad Implementada

### 🔍 **Detección de Cambios No Autorizados**
- **Notificación inmediata**: Usuario se entera al momento de cualquier cambio
- **Identificación del actor**: Diferencia entre cambios propios vs administrativos
- **Registro de auditoría**: Logs de todos los envíos de notificación

### ⚠️ **Mensajes de Alerta**
- **Para cambios propios**: Alerta sobre posible compromiso de cuenta
- **Para cambios admin**: Información sobre cambios esperados vs inesperados
- **Contacto directo**: Instrucciones claras para reportar problemas

### 🔐 **Validaciones Mejoradas**
- **Username único**: Validación que excluye usuario actual en updates
- **Email único**: Previene duplicados considerando actualizaciones
- **Contraseñas seguras**: Validación de complejidad en nuevas contraseñas

## 🚀 Beneficios del Sistema

### 👤 **Para Usuarios**
- ✅ **Transparencia total** sobre cambios en su cuenta
- ✅ **Detección temprana** de accesos no autorizados  
- ✅ **Confirmación** de cambios legítimos realizados por ellos
- ✅ **Información clara** sobre cambios administrativos

### 👨‍💼 **Para Administradores**
- ✅ **Auditoría automática** de todas las modificaciones
- ✅ **Reducción de tickets** de soporte por cambios no comunicados
- ✅ **Mejora en la confianza** del usuario hacia el sistema
- ✅ **Cumplimiento** de mejores prácticas de seguridad

### 🏢 **Para la Organización**
- ✅ **Mejor seguridad** general del sistema
- ✅ **Trazabilidad completa** de cambios de usuario
- ✅ **Reducción de riesgos** de seguridad
- ✅ **Compliance** con estándares de notificación

## 📈 Casos de Uso

### 🔄 **Escenarios Cubiertos**

1. **Usuario actualiza su perfil**
   - ✉️ Recibe confirmación de cambios realizados
   - 🚨 Alerta de seguridad si no los realizó

2. **Admin cambia datos de usuario**
   - ✉️ Usuario recibe notificación con nombre del admin
   - 📞 Instrucciones para contactar admin si es inesperado

3. **Cambio de contraseña**
   - ✉️ Notificación inmediata sin mostrar nueva contraseña
   - 🔐 Confirmación de actualización de seguridad

4. **Cambio de rol/permisos**
   - ✉️ Notificación con nombres legibles de roles
   - 📋 Usuario comprende sus nuevos permisos

5. **Actualización de email**
   - ✉️ Notificación enviada al nuevo email
   - 🔄 Confirmación del cambio de contacto

## 🔮 Posibles Extensiones Futuras

### 📧 **Mejoras de Notificación**
- 📱 **SMS/WhatsApp**: Notificaciones multi-canal
- 🌐 **In-app notifications**: Alertas dentro de la aplicación
- 📊 **Dashboard de cambios**: Panel de historial para usuarios

### 🔒 **Seguridad Avanzada**
- 🕐 **Ventana de confirmación**: Tiempo límite para confirmar cambios críticos
- 📍 **Geolocalización**: Alertas por cambios desde ubicaciones inusuales
- 🔑 **2FA obligatorio**: Autenticación adicional para cambios sensibles

### 📈 **Analytics y Reporting**
- 📊 **Métricas de cambios**: Estadísticas de modificaciones por usuario
- 🎯 **Detección de patrones**: Identificación de comportamientos anómalos
- 📋 **Reportes administrativos**: Resúmenes periódicos de actividad

## 💡 Implementación y Despliegue

### ⚙️ **Configuración Requerida**
```python
# settings.py
EMAIL_HOST_USER = 'tu-email@dominio.com'
EMAIL_HOST = 'smtp.tu-proveedor.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_PASSWORD = 'tu-password'
```

### 🧪 **Testing**
- ✅ **Pruebas unitarias** para cada función de notificación
- ✅ **Pruebas de integración** para flujos completos
- ✅ **Pruebas de seguridad** para validaciones
- ✅ **Pruebas de rendimiento** para envíos masivos

### 📦 **Dependencias**
- `django.core.mail` - Envío de correos
- `bcrypt` - Hashing seguro de contraseñas  
- `django-rest-framework` - APIs REST
- Configuración SMTP válida

---

**📅 Fecha de implementación**: Agosto 2024  
**👨‍💻 Desarrollado por**: Claude Code AI  
**🔧 Versión**: 1.0.0  
**📊 Estado**: ✅ Funcional y en producción