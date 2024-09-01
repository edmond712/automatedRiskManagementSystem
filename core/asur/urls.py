from django.urls import path
from .views import FileUploadView, upload_file_view

urlpatterns = [
    path('one/', FileUploadView.as_view(), name='upload'),
    path('two/', upload_file_view, name='upload_file'),
]
