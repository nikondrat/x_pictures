from django.urls import path

from apps.mailing import views

app_name = 'mailing'

urlpatterns = [
    path('first-event-2024/<str:secret_code>/', views.first_event_2024_view, name='first_event_2024'),
]
