#!/usr/bin/env python
"""
Script de inicialización de datos para desarrollo.

Inserta:
- Roles (1=Admin, 2=Superadmin, 3=Colaborador)
- Estados de proyecto (1=Activo, 2=Inactivo, 3=Completado)
- Permisos referenciados por las vistas
- Asignación de todos los permisos al rol Admin y Superadmin
- Usuario admin inicial (username=admin, password=Admin123!) si no existe
- Usuario superadmin inicial (username=superadmin, password=SuperAdmin123!) si no existe

Uso:
  1) Ejecuta migraciones antes: `python manage.py migrate`
  2) Ejecuta este script desde la carpeta del backend: `python cargar_datos_iniciales.py`
"""

import os
import sys

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_manager.settings")
try:
    import django  # type: ignore
    django.setup()
except Exception as e:
    print("[ERROR] No se pudo inicializar Django. Asegúrate de ejecutar el script desde 'gestor_proyectos_csi_back/' y tener el entorno configurado.")
    raise

from users.models import RoleType, User
from projects.models import StatusType
from permissions.models import Permission, RolePermission
from django.core.management import call_command
import bcrypt


def ensure_roles():
    roles = [
        (1, "Admin"),
        (2, "Superadmin"),
        (3, "Colaborador"),
    ]
    for rid, name in roles:
        RoleType.objects.update_or_create(id=rid, defaults={"name": name})
    print("✅ Roles listos (1=Admin, 2=Superadmin, 3=Colaborador)")


def ensure_statuses():
    statuses = [
        (1, "Activo"),
        (2, "Inactivo"),
        (3, "Completado"),
    ]
    for sid, name in statuses:
        StatusType.objects.update_or_create(id=sid, defaults={"name": name})
    print("✅ Estados de proyecto listos (1=Activo, 2=Inactivo, 3=Completado)")


def ensure_permissions():
    perm_names = [
        # usuarios
        "view_user", "add_user", "change_user", "delete_user",
        # proyectos
        "view_projects", "add_project", "change_project", "delete_project",
        # áreas
        "view_areas", "add_area", "change_area", "delete_area",
        # repositorios
        "view_repository", "add_repository", "change_repository", "delete_repository",
        # grupos
        "view_groups", "add_group", "change_group", "delete_group",
    ]
    perms = {}
    for name in perm_names:
        p, _ = Permission.objects.get_or_create(name=name)
        perms[name] = p
    print(f"✅ Permisos creados/asegurados: {len(perms)}")
    return perms


def assign_permissions(perms):
    """Asigna todos los permisos a Admin y Superadmin, y solo los necesarios al Colaborador."""
    # Superadmin -> todos los permisos
    superadmin = RoleType.objects.get(id=2)
    created_count_sa = 0
    for p in perms.values():
        _, created = RolePermission.objects.get_or_create(role=superadmin, permission=p)
        if created:
            created_count_sa += 1
    print(f"✅ Permisos (todos) asignados a {superadmin.name} (nuevos: {created_count_sa})")

    # Admin -> todos excepto 'delete_user'
    admin = RoleType.objects.get(id=1)
    created_count_admin = 0
    for name, p in perms.items():
        if name == "delete_user":
            continue
        _, created = RolePermission.objects.get_or_create(role=admin, permission=p)
        if created:
            created_count_admin += 1
    # Asegurar que Admin NO tenga 'delete_user'
    RolePermission.objects.filter(role=admin, permission__name="delete_user").delete()
    print(f"✅ Permisos (sin 'delete_user') asignados a {admin.name} (nuevos: {created_count_admin})")

    # Colaborador -> sólo mínimos necesarios
    collaborator = RoleType.objects.get(id=3)
    # Basado en los permisos originales del colaborador
    # y el comando update_colaborador_permissions
    allowed = {
        "view_user",
        "change_user",
    }
    # Eliminar permisos extra si existían
    RolePermission.objects.filter(role=collaborator).exclude(permission__name__in=allowed).delete()
    # Asegurar los mínimos
    created_min = 0
    for name in allowed:
        p = perms.get(name)
        if p is None:
            p, _ = Permission.objects.get_or_create(name=name)
            perms[name] = p
        _, created = RolePermission.objects.get_or_create(role=collaborator, permission=p)
        if created:
            created_min += 1
    print(f"✅ Permisos mínimos asignados a {collaborator.name} (nuevos: {created_min})")


def ensure_admin_user():
    admin_role = RoleType.objects.get(id=1)
    raw_password = "Admin123!"
    hashed = bcrypt.hashpw(raw_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    user, created = User.objects.get_or_create(
        username="admin",
        defaults={
            "first_name": "Admin",
            "last_name": "Local",
            "email": "admin@example.com",
            "password": hashed,
            "role": admin_role,
        },
    )
    if created:
        print("✅ Usuario admin creado. Usuario=admin Password=Admin123!")
    else:
        print("ℹ️  Usuario admin ya existe")


def ensure_superadmin_user():
    superadmin_role = RoleType.objects.get(id=2)
    raw_password = "SuperAdmin123!"
    hashed = bcrypt.hashpw(raw_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    user, created = User.objects.get_or_create(
        username="superadmin",
        defaults={
            "first_name": "Super",
            "last_name": "Admin",
            "email": "superadmin@example.com",
            "password": hashed,
            "role": superadmin_role,
        },
    )
    if created:
        print("✅ Usuario superadmin creado. Usuario=superadmin Password=SuperAdmin123!")
    else:
        print("ℹ️  Usuario superadmin ya existe")


def update_colab_permissions():
    try:
        call_command("update_colaborador_permissions")
        print("✅ Permisos de colaborador actualizados (comando de management)")
    except Exception as e:
        print(f"ℹ️  No se pudo ejecutar update_colaborador_permissions: {e}")


def print_permissions_summary():
    from django.db.models import Value
    for rid in (1, 2, 3):
        try:
            role = RoleType.objects.get(id=rid)
        except RoleType.DoesNotExist:
            continue
        names = list(
            RolePermission.objects.filter(role=role)
            .select_related("permission")
            .order_by("permission__name")
            .values_list("permission__name", flat=True)
        )
        print(f"\n--- Permisos de {role.name} (id={rid}) [{len(names)}] ---")
        for n in names:
            print(f" • {n}")


def main():
    ensure_roles()
    ensure_statuses()
    perms = ensure_permissions()
    assign_permissions(perms)
    ensure_admin_user()
    ensure_superadmin_user()
    update_colab_permissions()
    print_permissions_summary()
    print("\n🎉 Datos iniciales de desarrollo listos.")


if __name__ == "__main__":
    main()
