from django.contrib.auth.models import Permission
from users.models import User


#REFERENCIA DE TODOS LOS PERMISOS

# Asocia los permisos con el ID del rol
ROLE_PERMISSIONS = {
    1: [  # Admin
        'view_projects',
        'view_project',
        'view_repository',
        'view_areas',
        'view_area',
        'view_groups',
        'view_group',
        'view_tools',
        'add_project',
        'change_project',
        'delete_project',
        'add_repository',
        'change_repository',
        'delete_repository',
        'add_area',
        'change_area',
        'delete_area',
        'add_group',
        'change_group',
        'delete_group',
        'add_tool',
        'change_tool',
        'delete_tool',
        'view_user',
        'add_user',
        'change_user',
        'view_users',
        # Admin puede crear, modificar y eliminar entidades, pero NO eliminar usuarios
    ],
    2: [ # SuperAdmin
        'view_projects',
        'view_project',
        'view_repository',
        'view_areas',
        'view_area',
        'view_groups',
        'view_group',
        'view_tools',
        'delete_user',
        'view_user',
        'add_user',
        'change_user',
        'view_users',
        'add_project',
        'change_project',
        'delete_project',
        'add_repository',
        'change_repository',
        'delete_repository',
        'add_area',
        'change_area',
        'delete_area',
        'add_group',
        'change_group',
        'delete_group',
        'add_tool',
        'change_tool',
        'delete_tool',
    ],
    3: [  # Usuario/Colaborador
        'view_projects',
        'view_project',
        'view_user',     # Puede ver datos de usuario (necesario para su perfil)
        'change_user',   # Puede modificar datos de usuario (para editar su perfil)
    ],
}

def assign_permissions_by_role(user: User):
    if not user.role:
        return
    role_id = user.role.id
    perms = ROLE_PERMISSIONS.get(role_id, [])
    # Limpia permisos anteriores
    if hasattr(user, 'user_permissions'):
        user.user_permissions.clear()
        for codename in perms:
            try:
                perm = Permission.objects.get(codename=codename)
                user.user_permissions.add(perm)
            except Permission.DoesNotExist:
                continue