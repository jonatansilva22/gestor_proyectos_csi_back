"""
URL configuration for project_manager project.

The urlpatterns list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    
Add an import:  from my_app import views
Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    
Add an import:  from other_app.views import Home
Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    
Import the include() function: from django.urls import include, path
Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from projects import urls as projects_urls
from repositories import urls as repositories_urls
from areas import urls as areas_urls
from tools import urls as tools_urls
from users.Crear_Usuario import urls as user_urls
from users.LogIn import urls as login_urls
from workgroups import urls as groups_urls
from dashboard import urls as dashboard_urls

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('api/', include(projects_urls)),
    path('api/', include(areas_urls)),
    path('api/', include(repositories_urls)),
    path('api/', include(tools_urls)),
    path('api/', include(user_urls)),
    path('api/', include(login_urls)),
    path('api/', include(groups_urls)),
    path('api/', include(dashboard_urls)),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)