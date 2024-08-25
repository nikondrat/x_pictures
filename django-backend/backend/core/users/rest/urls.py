from django.urls import path, include
from rest_framework.routers import SimpleRouter

from core.users.rest import views

router = SimpleRouter()

router.register('password-reset', viewset=views.PasswordResetAPIViewSet, basename='password_reset_set')
router.register('social-media', viewset=views.SocialMediaAuthAPIViewSet, basename='social_media_set')
router.register('marketing', viewset=views.MarketingAPIViewSet, basename='marketing_set')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.RegisterAPIView.as_view(), name='register'),
    path('login/', views.LoginAPIView.as_view(), name='login'),

    path('verification/<str:token>', views.verification_view, name='verification'),
    path('refresh-verification/', views.refresh_verification_view, name='refresh_verification'),
]
