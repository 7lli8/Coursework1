from django.urls import path

from . import views
from .views import home_view, upload_file_for_edition, hello, display_file, save_dicom_file

urlpatterns = [
    path("", home_view, name="home"),
    path("upload_file_for_edition/", upload_file_for_edition),
    path("index/", hello),
    path('display/', views.display_file, name='display_file'),  # URL отображения файла
    path('save_dicom_file/', save_dicom_file, name='save_dicom_file')
]
