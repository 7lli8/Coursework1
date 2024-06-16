from django.urls import path

from .views import home_view, upload_file_for_edition, display_file, save_dicom_file, upload_file_for_anonymization, download_file_view

urlpatterns = [
    path("", home_view, name="home"),
    path("upload_file_for_edition/", upload_file_for_edition, name="upload_file_for_edition"),
    path('display/', display_file, name='display_file'),  # URL отображения файла
    path('save_dicom_file/', save_dicom_file, name='save_dicom_file'),
    path('upload_file_for_anonymization/', upload_file_for_anonymization, name='upload_file_for_anonymization'),
    path('download_file/<int:file_id>/', download_file_view, name="download_file")
]
