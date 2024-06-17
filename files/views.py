import pydicom
import re
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from django.core.files.base import File
from .forms import FileUploadForm
from .models import CustomFiles
from files.course import handle_file_upload, display_dicom_file, anonymization_file, render_image_base64, read_tags, update_file
from django.contrib.auth.decorators import login_required


def home_view(request):
    return render(request, "files/home.html")


@login_required
def display_file(request, file_id):
    file = get_object_or_404(CustomFiles.objects.filter(uploaded_by=request.user), pk=file_id)
    dicom_file = pydicom.dcmread(file.file.path, force=True)

    if request.method == "POST":
        attributes = {key: value for key, value in request.POST.items() if re.fullmatch(r"\(\d+, \d+\)", key)}
        dicom_file = update_file(file.file.path, dicom_file, attributes)
        file.save()
        file.refresh_from_db()
    
    
    image_base64 = render_image_base64(dicom_file)
    tags = read_tags(dicom_file)

    return render(
        request,
        "files/display.html",
        {"image_base64": image_base64, "tags": tags, "file_id": file.pk},
    )



def upload_file_for_edition(request):
    if request.method == "POST":  # Проверяем, был ли отправлен POST запрос
        try:
            # Используем функцию для обработки загрузки файла
            fp = handle_file_upload(request)

            return redirect("display_file", file_id=fp.pk)
        except ValidationError as e:
            messages.error(request, str(e))
    else:
        form = (
            FileUploadForm()
        )  # Если метод запроса не POST, создаем пустую форму загрузки файлов

    # Рендеринг страницы загрузки файла с формой
    return render(request, "files/upload_file.html", {"form": form})


def upload_file_for_anonymization(request):
    if request.method == "POST":  # Проверяем, был ли отправлен POST запрос
        try:
            # Используем функцию для обработки загрузки файла
            fp = handle_file_upload(request)
            new_file = anonymization_file(pydicom.dcmread(fp.file.path))
            new_file.save_as(fp.file.path)
            fp.refresh_from_db()
            return redirect("display_file", file_id=fp.pk)
        except ValidationError as e:
            messages.error(request, str(e))
    else:
        form = (
            FileUploadForm()
        )  # Если метод запроса не POST, создаем пустую форму загрузки файлов

    # Рендеринг страницы загрузки файла с формой
    return render(request, "files/upload_file_for_anonymization.html", {"form": form})


@login_required
def download_file_view(request, file_id):
    file = get_object_or_404(CustomFiles.objects.filter(uploaded_by=request.user), pk=file_id)
    response = HttpResponse(file.file.read(), content_type="application/octet-stream")
    response['Content-Disposition'] = 'inline; filename=' + file.file_name
    return response


