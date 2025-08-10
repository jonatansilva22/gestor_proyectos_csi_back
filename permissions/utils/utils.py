from permissions.models import RolePermission

def user_has_permission(user, permission_name):
    if not user.role:
        return False
    return RolePermission.objects.filter(
        role=user.role,
        permission__name=permission_name
    ).exists()