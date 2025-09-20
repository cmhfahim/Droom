from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('apps.core.urls', 'core'), namespace='core')),  
    path('users/', include(('apps.users.urls', 'users'), namespace='users')),  
    path('billing/', include(('apps.billing.urls', 'billing'), namespace='billing')),
    path('api/', include(('apps.api.urls', 'api'), namespace='api')),
    path('accounts/', include('django.contrib.auth.urls')),  
]
