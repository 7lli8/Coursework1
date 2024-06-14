import base64
import io

import pandas as pd
import pydicom
import pydicom as dicom
from django.core.exceptions import ValidationError
from matplotlib import pyplot as plt
from pydicom.errors import InvalidDicomError

from files.forms import FileUploadForm
from files.models import CustomFiles


# path = "files/img/abo_DingoBrain_Ballard_010001.dcm"
# x = dicom.dcmread(path)
#
# print(x)


def read_dicom_file(path_file):#функция для считывания файла dicom
    try:
        tagset = dicom.dcmread(path_file)
        return tagset
    except TypeError:
        return "error"
    except InvalidDicomError:
        return ""


def edit_dicom_file(dataset, attribute, new_value):
    if dataset is not None:
        try:
            setattr(dataset, attribute, new_value)
            print("Тэг изменён")
            return True
        except Exception as e:
            print("Ошибка редактирования тэга:", e)
            return False
    else:
        print("Файл не может быть прочитан")
        return False

# edited = edit_dicom_file(x, "PatientName", "ВИКА")
# if edited:
#     # Сохранение изменений (необязательно)
#     x.save_as("edited_example.dcm")
# print(x)

def handle_file_upload(request):
    form = FileUploadForm(request.POST, request.FILES)  # Инициализация формы с данными из запроса (POST и FILES)
    if form.is_valid():  # Проверка валидности данных формы
        file = request.FILES['file']  # Получение загруженного файла из данных запроса
        uploaded_by = request.user if request.user.is_authenticated else None  # Определение пользователя, загрузившего файл
        fp = CustomFiles(file=form.cleaned_data["file"], file_name=file.name, uploaded_by=uploaded_by)  # Создание экземпляра CustomFiles для сохранения в базе данных
        fp.save()  # Сохранение файла в базе данных
    else:
        raise ValidationError("Неподдерживаемое расширение файла")  # Выброс исключения в случае невалидности формы


# Отображение DICOM файла в формате изображения и таблицы тегов
def display_dicom_file(file_path):
    try:
        ds = pydicom.dcmread(file_path, force=True)  # Чтение файла DICOM из указанного пути

        if hasattr(ds, 'pixel_array'):  # Проверка наличия массива пикселей в файле DICOM
            image_data = ds.pixel_array  # Получение данных изображения

            fig, ax = plt.subplots()  # Создание объектов для отображения изображения с использованием matplotlib
            ax.imshow(image_data, cmap='gray')  # Отображение изображения
            buf = io.BytesIO()  # Создание буфера для сохранения изображения
            plt.savefig(buf, format='png')  # Сохранение изображения в формате PNG в буфер
            plt.close(fig)  # Закрытие текущего изображения
            buf.seek(0)  # Переход к началу буфера
            image_base64 = base64.b64encode(buf.read()).decode('utf-8')  # Кодирование изображения в формат base64 для передачи через HTTP

            data = {elem.description(): elem.value for elem in ds if elem.VR != 'SQ'}  # Извлечение метаданных DICOM
            df = pd.DataFrame(list(data.items()), columns=['Атрибут', 'Значение'])  # Создание DataFrame для отображения метаданных в виде таблицы HTML

            return image_base64, df.to_html(classes='table table-striped', index=False)  # Возврат изображения и таблицы метаданных в формате HTML
        else:
            return None, None  # Возврат None, если изображение отсутствует в файле DICOM
    except Exception as e:
        print(f"Ошибка при отображении DICOM файла {file_path}: {e}")  # Вывод сообщения об ошибке в случае исключения
        return None, None  # Возврат None в случае ошибки