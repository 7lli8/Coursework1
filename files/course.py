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


def read_dicom_file(path_file):  #функция для считывания файла dicom
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


def handle_file_upload(request):
    form = FileUploadForm(request.POST, request.FILES)  # Инициализация формы с данными из запроса (POST и FILES)
    if form.is_valid():  # Проверка валидности данных формы
        file = request.FILES['file']  # Получение загруженного файла из данных запроса
        uploaded_by = request.user if request.user.is_authenticated else None  # Определение пользователя, загрузившего файл
        fp = CustomFiles(file=form.cleaned_data["file"], file_name=file.name,
                         uploaded_by=uploaded_by)  # Создание экземпляра CustomFiles для сохранения в базе данных
        fp.save()  # Сохранение файла в базе данных
        return fp
    else:
        raise ValidationError("Неподдерживаемое расширение файла")  # Выброс исключения в случае невалидности формы


#Отображение DICOM файла в формате изображения и таблицы тегов
def display_dicom_file(file_path):
    """
    Функция для отображения изображения и метаданных DICOM файла.

    Args:
    - file_path (str): Путь к файлу DICOM.

    Returns:
    - tuple: Кортеж содержащий данные в формате base64 для изображения и HTML для метаданных.
    """
    try:
        dicom_file = pydicom.dcmread(file_path, force=True)

        if hasattr(dicom_file, 'pixel_array'):
            image_data = dicom_file.pixel_array

            fig, ax = plt.subplots()
            ax.imshow(image_data, cmap='gray')
            buf = io.BytesIO()  #создаем буфер для временного хранения графики
            plt.savefig(buf, format='png')
            plt.close(fig) #закрываем фигуру - освобождаем память
            buf.seek(0) # указатель буфера в начало для записи в image_base64
            image_base64 = base64.b64encode(buf.read()).decode('utf-8')

            # Создаем HTML для редактируемой таблицы
            rows = ""
            for elem in dicom_file:
                # Исключаем тег Pixel Data (7FE0, 0010) из вывода
                if elem.tag != (0x7FE0, 0x0010) and elem.VR != 'SQ':
                    tag_number = f"({elem.tag.group:04x}, {elem.tag.element:04x})"
                    rows += f"<tr><td>{tag_number}</td><td>{elem.description()}</td><td><input type='text' name='{tag_number}' value='{elem.value}' class='form-control'></td></tr>"

            table_html = f"""
            <table class='table table-striped'>
                <thead>
                    <tr>
                        <th>Номер тега</th>
                        <th>Атрибут</th>
                        <th>Значение</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
            """

            return image_base64, table_html
        else:
            return None, None
    except Exception as e:
        print(f"Ошибка при отображении DICOM файла {file_path}: {e}")
        return None, None
