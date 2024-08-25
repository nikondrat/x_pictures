from django.urls import path, include
from rest_framework.routers import SimpleRouter

from apps.gallery.rest import views

app_name = 'gallery'

router = SimpleRouter()
router.register('images', viewset=views.ImageGalleryAPIViewSet, basename='images_set')

urlpatterns = [
    path('', include(router.urls)),
]
