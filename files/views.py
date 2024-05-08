from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

from .course import edit_dicom_file, read_dicom_file
from .forms import FileUploadForm


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

    return render(
        request,
        "files/read.html",
        {"props": [f"{key}: {str(getattr(file, key))}" for key in keys]},
    )


def upload_file2(request):
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data.get("file")
            form.handle_uploaded_file(file)
            # Дальнейшая обработка загруженного файла
            return render(request, "files/upload_file.html", {"form": form})
    else:
        form = FileUploadForm()
    return render(request, "files/upload_file.html", {"form": form})


def home_view(request):
    return render(request, "files/home.html")
