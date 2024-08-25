from django.urls import path

from apps.support.rest import views

urlpatterns = [
    path('create-message/', views.SupportMessageView.as_view(), name='create_message'),
]
