from django.urls import path, include
from rest_framework.routers import SimpleRouter

from apps.jobs.rest import views

router = SimpleRouter()
router.register('undress', viewset=views.UndressAPIViewSet, basename='undress_set')
router.register('undress-without-mask', viewset=views.UndressWithoutMaskAPIViewSet,
                basename='undress_without_mask_set')
router.register('generate', viewset=views.GenerateAPIViewSet, basename='generate_set')
router.register('white-generate', viewset=views.WhiteGenerateAPIViewSet, basename='white_generate_set')
router.register('instagram-undress', viewset=views.InstagramUndressAPIViewSet,
                basename='instagram_undress_set')
router.register('video', viewset=views.VideoAPIViewSet, basename='video_set')

urlpatterns = [
    path('', include(router.urls)),
]
