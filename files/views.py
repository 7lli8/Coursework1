from django.shortcuts import render
from django.http import HttpResponse
from .course import edit_dicom_file, read_dicom_file
from .forms import FileUploadForm
from .models import CustomFiles


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
            #fp = CustomFiles(file = form.cleaned_data["file"])
            file = request.FILES['file']  # Получить загруженный файл
            uploaded_by = request.user if request.user.is_authenticated else None # Получить авторизованного пользователя или None
            fp = CustomFiles(file=form.cleaned_data["file"], file_name=file.name, uploaded_by=uploaded_by)  # Создать экземпляр модели с исходным именем файла и пользователем
            fp.save()
            # Дальнейшая обработка загруженного файла
            #return render(request, "files/upload_file.html", {"form": form})
    else:
        form = FileUploadForm()
    return render(request, "files/upload_file.html", {"form": form})


def home_view(request):
    return render(request, "files/home.html")
