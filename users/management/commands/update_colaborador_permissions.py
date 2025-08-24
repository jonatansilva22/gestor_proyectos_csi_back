from django.core.management.base import BaseCommand
from users.models import RoleType
from permissions.models import Permission, RolePermission

class Command(BaseCommand):
    help = 'Actualiza los permisos del rol colaborador'
    
    def handle(self, *args, **options):
        try:
            # Obtener o crear permisos necesarios
            view_user_perm, created = Permission.objects.get_or_create(name='view_user')
            if created:
                self.stdout.write(f"✅ Permiso 'view_user' creado")
            else:
                self.stdout.write(f"ℹ️  Permiso 'view_user' ya existe")
            
            change_user_perm, created = Permission.objects.get_or_create(name='change_user')
            if created:
                self.stdout.write(f"✅ Permiso 'change_user' creado")
            else:
                self.stdout.write(f"ℹ️  Permiso 'change_user' ya existe")
            
            # Buscar rol colaborador (ID 3)
            try:
                colaborador_role = RoleType.objects.get(id=3)
                self.stdout.write(f"🔍 Rol encontrado: {colaborador_role.name} (ID: {colaborador_role.id})")
            except RoleType.DoesNotExist:
                self.stdout.write(self.style.ERROR("❌ Rol colaborador (ID: 3) no encontrado"))
                return
            
            # Asignar permisos al rol colaborador
            view_permission, created = RolePermission.objects.get_or_create(
                role=colaborador_role,
                permission=view_user_perm
            )
            if created:
                self.stdout.write(f"✅ Asignado 'view_user' al rol colaborador")
            else:
                self.stdout.write(f"ℹ️  'view_user' ya asignado al rol colaborador")
            
            change_permission, created = RolePermission.objects.get_or_create(
                role=colaborador_role,
                permission=change_user_perm
            )
            if created:
                self.stdout.write(f"✅ Asignado 'change_user' al rol colaborador")
            else:
                self.stdout.write(f"ℹ️  'change_user' ya asignado al rol colaborador")
            
            # Mostrar resumen de permisos del colaborador
            colaborador_permissions = RolePermission.objects.filter(role=colaborador_role)
            self.stdout.write(f"\n📋 Permisos actuales del rol colaborador:")
            for perm in colaborador_permissions:
                self.stdout.write(f"   • {perm.permission.name}")
            
            self.stdout.write(self.style.SUCCESS(f"\n🎉 ¡Permisos del colaborador actualizados correctamente!"))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error: {str(e)}"))