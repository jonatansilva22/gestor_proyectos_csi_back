from rest_framework.decorators import api_view
from rest_framework.response import Response
from users.models import User
from projects.models import Project
from workgroups.models import WorkGroup
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard(request):
    # Totales por tipo de usuario
    usuarios = [
        {"nombre": "Superadmin", "total": User.objects.filter(role=2).count()},
        {"nombre": "Admin", "total": User.objects.filter(role=1).count()},
        {"nombre": "Colaborador", "total": User.objects.filter(role=3).count()}
    ]

    # Totales por estado de proyecto
    proyectos = [
        {"nombre": "Activo", "total": Project.objects.filter(status=1).count()},
        {"nombre": "Inactivo", "total": Project.objects.filter(status=2).count()},
        {"nombre": "Completado", "total": Project.objects.filter(status=3).count()},
        {"nombre": "Mantenimiento", "total": Project.objects.filter(status=4).count()},
    ]

    # Listado de grupos con nombre e id
    grupos = [{"id": g.id, "nombre": g.name} for g in WorkGroup.objects.all()]

    return Response({
        "Usuarios": usuarios,
        "Proyectos": proyectos,
        "Grupos": grupos
    })
