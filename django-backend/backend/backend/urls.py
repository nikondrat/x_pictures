from django.conf import settings
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/admin/', admin.site.urls),
    # OpenAPI schema
    path('api/', include('core.common.openapi.urls'), name='openapi'),
    # Core
    path('api/users/', include('core.users.rest.urls'), name='users'),
    # Apps
    path('api/support/', include('apps.support.rest.urls'), name='support'),
    # V2 apps
    path('api/shop/', include('apps.shop.rest.urls'), name='shop'),
    path('api/jobs/', include('apps.jobs.rest.urls'), name='jobs'),
    path('api/profiles/', include('apps.profiles.rest.urls'), name='profiles'),
    path('api/gallery/', include('apps.gallery.rest.urls'), name='gallery'),
    path('b/mailing/', include('apps.mailing.urls'), name='mailing'),
    path('api/face2img/', include('apps.face2img.rest.urls'), name='face2img'),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = [
        path('__debug__/', include('debug_toolbar.urls')),
    ] + urlpatterns
