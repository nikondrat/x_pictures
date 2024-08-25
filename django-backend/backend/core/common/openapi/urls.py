from django.urls import path

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
    # Only jobs
    path('schema-jobs/', SpectacularAPIView.as_view(), name='schema_jobs'),
    path('schema-jobs/docs/', SpectacularSwaggerView.as_view(url_name='schema_jobs'), name='jobs_docs'),
    # Only gallery
    path('schema-gallery/', SpectacularAPIView.as_view(), name='schema_galley'),
    path('schema-gallery/docs/', SpectacularSwaggerView.as_view(url_name='schema_galley'), name='gallery_docs'),
    # Only user & profile
    path('schema-users/', SpectacularAPIView.as_view(), name='schema_galley'),
    path('schema-users/docs/', SpectacularSwaggerView.as_view(url_name='schema_galley'), name='gallery_docs'),
]
