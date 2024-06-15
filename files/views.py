import pydicom
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from .forms import FileUploadForm
from .models import CustomFiles
from .course import handle_file_upload, display_dicom_file
from django.contrib.auth.decorators import login_required


def hello(request):
    return render(request, "files/index.html")


def home_view(request):
    return render(request, "files/home.html")


def upload_file_for_edition(request):
    if request.method == "POST":  # Проверяем, был ли отправлен POST запрос
        try:
            # Используем функцию для обработки загрузки файла
            fp = handle_file_upload(request)

            # После успешной загрузки, подготовка данных для отображения DICOM - изображение и теги
            image_base64, tags_html = display_dicom_file(fp.file.path)

            # Перенаправление на страницу отображения DICOM
            return render(request, "files/display.html",
                          {"image_base64": image_base64, "tags_html": tags_html})
        except ValidationError as e:
            messages.error(request, str(e))
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
        return render(request, "display.html", {"image_base64": image_base64, "tags_html": tags_html})
    except CustomFiles.DoesNotExist:

        # В случае отсутствия загруженных файлов пользователем, возвращаем сообщение об ошибке и перенаправляем на страницу загрузки файла
        messages.error(request, "Файл не найден или у вас нет загруженных файлов")
        return redirect("upload_file_for_edition")

# Функция для сохранения изменений в файле DICOM.
def save_dicom_file(request):
    if request.method == "POST":
        try:
            last_uploaded_file = CustomFiles.objects.filter(uploaded_by=request.user).latest('uploaded_at')  # Получение последнего загруженного файла текущего пользователя
            file_path = last_uploaded_file.file.path  # Получение пути к файлу
            ds = pydicom.dcmread(file_path, force=True)  # Чтение DICOM файла

            # Обновление значений тегов DICOM
            for key, value in request.POST.items():
                if key.startswith('(') and key.endswith(')'):
                    tag = pydicom.tag.Tag(key.strip('()').split(','))  # Преобразование строки в теги DICOM
                    if tag in ds:
                        ds[tag].value = value  # Обновление значения тега

            ds.save_as(file_path)  # Сохранение изменений в файл
            messages.success(request, "Изменения успешно сохранены.")
        except Exception as e:
            messages.error(request, f"Ошибка при сохранении файла DICOM: {e}")

    return redirect('display_file')  # Перенаправление на страницу отображения DICOM файла



