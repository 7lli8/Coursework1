from django.shortcuts import render
from django.http import HttpResponse

from .course import edit_dicom_file, read_dicom_file


def hello(request):
    return render(request, "files/index.html")


def upload_file(request):
    if request.method == "GET":
        return HttpResponse("123")
    else:
        pass


def read_file(request):
    file = read_dicom_file("files/img/abo_DingoBrain_Ballard_010001.dcm")
    keys = [key for key in dir(file) if "_" not in key and key[0].isupper()]

    return render(request, "files/read.html", {
        "props": [f"{key}: {str(getattr(file, key))}" for key in keys]
    })