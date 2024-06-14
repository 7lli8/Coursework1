from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from .forms import FileUploadForm
from .models import CustomFiles
from .course import handle_file_upload, read_dicom_file, display_dicom_file
from django.contrib.auth.decorators import login_required


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
def home_view(request):
    return render(request, "files/home.html")


# Функция для загрузки файла (только для авторизованных пользователей)
def upload_file2(request):
    if request.method == "POST":  # Проверяем, был ли отправлен POST запрос
        form = FileUploadForm(request.POST, request.FILES)  # Инициализируем форму загрузки файлов с данными из запроса
        if form.is_valid():  # Проверяем валидность данных формы
            file = request.FILES['file']  # Получаем загруженный файл из формы
            uploaded_by = request.user if request.user.is_authenticated else None  # Определяем пользователя, загрузившего файл (если он авторизован)
            fp = CustomFiles(file=form.cleaned_data["file"],
                             file_name=file.name,
                             uploaded_by=uploaded_by)  # Создаем экземпляр CustomFiles для сохранения файла в базе данных
            fp.save()  # Сохраняем файл в базе данных

            # После успешной загрузки, подготовка данных для отображения DICOM
            image_base64, tags_html = display_dicom_file(fp.file.path)

            # Перенаправление на страницу отображения DICOM
            return render(request, "files/display.html",
                                {"image_base64": image_base64, "tags_html": tags_html})
    else:
        form = FileUploadForm()  # Если метод запроса не POST, создаем пустую форму загрузки файлов

    # Рендеринг страницы загрузки файла с формой
    return render(request, "files/upload_file.html", {"form": form})


def display_file(request):
    try:
        # Получение последнего загруженного файла текущего пользователя
        last_uploaded_file = CustomFiles.objects.filter(uploaded_by=request.user).latest('uploaded_at')
        file_path = last_uploaded_file.file.path  # Получение пути к файлу
        image_base64, tags_html = display_dicom_file(file_path)  # Получение изображения и данных DICOM для отображения

        # Рендеринг страницы отображения DICOM файла
        return render(request, "files/display.html", {"image_base64": image_base64, "tags_html": tags_html})
    except CustomFiles.DoesNotExist:
        # В случае отсутствия загруженных файлов пользователем, возвращаем сообщение об ошибке и перенаправляем на страницу загрузки файла
        messages.error(request, "Файл не найден или у вас нет загруженных файлов")
        return redirect("upload_file2")





