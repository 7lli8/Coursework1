from django.urls import path

from .views import hello, upload_file, read_file

urlpatterns = [
    path("", hello),
    path("upload/", upload_file),
    path("read/", read_file),
]
