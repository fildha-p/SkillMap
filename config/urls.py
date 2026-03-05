from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Authentication (login, logout, password reset, etc.)
    path('accounts/', include('django.contrib.auth.urls')),

    # Your App
    path('skillmap/', include('skillmap.urls')),
]

# Serve media in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)