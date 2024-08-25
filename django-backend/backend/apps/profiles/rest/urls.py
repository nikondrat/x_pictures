from django.urls import path, include
from rest_framework.routers import SimpleRouter

from apps.profiles.rest import views

profile_router = SimpleRouter()
profile_router.register('', viewset=views.ProfileAPIViewSet, basename='profile_set')
# TODO Delete legacy
profile_router.register('liked-image-storage', viewset=views.ProfileLikedImageAPIViewSet,
                        basename='liked_image_storage_set')
profile_router.register('patreon', viewset=views.PatreonAPIViewSet,
                        basename='patreon_set')


storage_router = SimpleRouter()
storage_router.register('images', viewset=views.ProfileImageStorageAPIViewSet, basename='images_storage_set')
storage_router.register('videos', viewset=views.ProfileVideoStorageAPIViewSet, basename='videos_storage_set')

liked_storage_router = SimpleRouter()
liked_storage_router.register('images', viewset=views.ProfileLikedImageAPIViewSet,
                              basename='liked_images_storage_set')
liked_storage_router.register('videos', viewset=views.ProfileLikedVideoAPIViewSet,
                              basename='liked_videos_storage_set')

urlpatterns = [
    path('', include(profile_router.urls)),
    path('storage/', include(storage_router.urls)),
    path('storage/liked/', include(liked_storage_router.urls)),

    # TODO Delete legacy
    path('image-storage/<uuid:pk>/', views.delete_image_from_storage_view,
         name='profile_set-delete_image_from_storage'),
]
