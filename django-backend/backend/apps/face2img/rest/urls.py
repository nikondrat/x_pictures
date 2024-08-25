from django.urls import path, include
from rest_framework.routers import SimpleRouter

from apps.face2img.rest import views

router = SimpleRouter()
router.register('loras', viewset=views.LoraAPIViewSet, basename='loras_set')
router.register('packs', viewset=views.PackAPIViewSet, basename='packs_set')
router.register('jobs', viewset=views.Face2ImgJobAPIViewSet, basename='jobs_set')

urlpatterns = [
    path('', include(router.urls)),
]
