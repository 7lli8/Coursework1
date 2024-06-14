from django.urls import path

from . import views
from .views import home_view, upload_file, read_file, upload_file2, hello, display_file

urlpatterns = [
    path("", home_view, name="home"),
    path("upload/", upload_file),
    path("read/", read_file),
    path("upload2/", upload_file2),
    path("index/", hello),
    path('display/', views.display_file, name='display_file'),  # URL отображения файла
]
