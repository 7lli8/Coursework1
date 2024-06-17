from django.urls import path

from .views import home_view, upload_file_for_edition, display_file, upload_file_for_anonymization, download_file_view

urlpatterns = [
    path("", home_view, name="home"),
    path("upload_file_for_edition/", upload_file_for_edition, name="upload_file_for_edition"),
    path('upload_file_for_anonymization/', upload_file_for_anonymization, name='upload_file_for_anonymization'),
    path('download_file/<int:file_id>/', download_file_view, name="download_file"),
    path("display/<int:file_id>/", display_file, name="display_file")
]
