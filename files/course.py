import base64
import io
import pydicom
import pydicom as dicom
from django.core.exceptions import ValidationError
from matplotlib import pyplot as plt
from PIL import Image
from pydicom.errors import InvalidDicomError
import pydicom.valuerep
import pydicom.values
from files.forms import FileUploadForm
from files.models import CustomFiles
from dataclasses import dataclass


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


@dataclass
class DicomTag:
    tag: str
    name: str
    value: str | float | int
    readonly: bool
    type: str = "text"


#Отображение DICOM файла в формате изображения и таблицы тегов
def display_dicom_file(file_path: str) -> tuple[str, list[DicomTag]]:
    """
    Функция для отображения изображения и метаданных DICOM файла.

    Args:
    - file_path (str): Путь к файлу DICOM.

    Returns:
    - tuple: Кортеж содержащий данные в формате base64 для изображения и HTML для метаданных.
    """
    try:
        dicom_file = pydicom.dcmread(file_path, force=True)

        image = render_image_base64(dicom_file)
        tags = read_tags(dicom_file)

        return image, tags
    except Exception as e:
        print(f"Ошибка при отображении DICOM файла {file_path}: {e}")
        return "", []


def render_image_base64(file: pydicom.FileDataset) -> str:
    image_data = file.pixel_array

    im = Image.fromarray(image_data.astype("uint8"))

    buffer = io.BytesIO()
    im.save(buffer, "PNG")
    buffer.seek(0)

    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')

    return image_base64


def get_dicom_number_types() -> tuple[type]:
    return (int, float, pydicom.valuerep.DSfloat, pydicom.valuerep.DSdecimal, pydicom.valuerep.ISfloat)


def read_tags(file: pydicom.FileDataset) -> list[DicomTag]:
    tags = []
    for elem in file:
        # Исключаем тег Pixel Data (7FE0, 0010) из вывода
        if elem.tag != (0x7FE0, 0x0010) and elem.VR != 'SQ':
            tag_number = f"({elem.tag.group:04x}, {elem.tag.element:04x})"
            tags.append(DicomTag(
                tag=tag_number,
                name=elem.description(),
                value=elem.value,
                readonly=not isinstance(elem.value, (str, *get_dicom_number_types())),
                type="number" if isinstance(elem.value, get_dicom_number_types()) else "text",
            ))
    return tags


def update_file(file_path: str, file: pydicom.FileDataset, attributes: dict[str, str | int | float]) -> pydicom.FileDataset:
    for tag_name, value in attributes.items():
        tag = tuple(map(lambda x: int(x, 16), tag_name[1:-1].split(", ")))
        prev = file[tag].value
        editable = isinstance(prev, (str, *get_dicom_number_types()))
        if isinstance(prev, get_dicom_number_types()):
            if not value.strip():
                value = 0.0
            else:
                value = type(prev)(value)
        if editable and prev != value and ((abs(prev - value) > 10e-6) if isinstance(prev, float) and isinstance(value, float) else True):
            file[tag].value = value
    
    file.save_as(file_path)
    return file
    


def anonymization_file(dicom_file):
    tags = [(0x0010, 0x0010), # patientName - имя пациента
            (0x0010, 0x0020), # patientID - Id пациента
            (0x0010, 0x0021), # issuerOfPatientID - организация, выдавшая идентификатор пациента
            (0x0010, 0x0022), # typeOfPatientID - тип идентификатора пациента
            (0x0010, 0x0024), # issuerOfPatientIDQualifiersSequence - последовательность квалификаторов идентификатора пациента
            (0x0010, 0x0030), # patientBirthDate - дата рождения пациента
            (0x0010, 0x0032), # patientBirthTime - время рождения пациента
            (0x0010, 0x0033), # patientBirthDateInAlternativeCalendar - дата рождения в альтернативном календаре
            (0x0010, 0x0034), # patientDeathDateInAlternativeCalendar - дата смерти в альтернативном календаре
            (0x0010, 0x0040), # patientSex - пол пациента
            (0x0010, 0x0050), # patientInsurancePlanCodeSequence - страховой план пациента
            (0x0010, 0x1000), # otherPatientIDs - другие идентификаторы пациента
            (0x0010, 0x1001), # otherPatientNames - другие имена пациента
            (0x0010, 0x1002), # otherPatientIDsSequence - последовательность других идентификаторов пациента
            (0x0010, 0x1005), # patientBirthName - имя при рождении
            (0x0010, 0x1010), # patientAge - возраст пациента
            (0x0010, 0x1040), # patientAddress - адрес пациента
            (0x0010, 0x1050), # insurancePlanIdentification - идентификация страхового плана (устаревший)
            (0x0010, 0x1060), # patientMotherBirthName - имя матери при рождении
            (0x0010, 0x1080), # militaryRank - воинское звание
            (0x0010, 0x1081), # branchOfService - ветвь службы
            (0x0010, 0x1090), # medicalRecordLocator - локатор медицинской записи
            (0x0010, 0x1100), # referencedPatientPhotoSequence - ссылка на фотографию пациента
            (0x0010, 0x2000), # medicalAlerts - медицинские предупреждения
            (0x0010, 0x2110), # allergies - аллергии
            (0x0010, 0x2150), # countryOfResidence - страна проживания
            (0x0010, 0x2152), # regionOfResidence - регион проживания
            (0x0010, 0x2154), # patientTelephoneNumbers - телефонные номера пациента
            (0x0010, 0x2155), # patientTelecomInformation - информация о телекоммуникациях пациента
            (0x0010, 0x2160), # ethnicGroup - этническая группа
            (0x0010, 0x2180), # occupation - профессия
            (0x0010, 0x21A0), # smokingStatus - статус курения
            (0x0010, 0x21B0), # additionalPatientHistory - дополнительная история пациента
            (0x0010, 0x21F0), # patientReligiousPreference - религиозные предпочтения пациента
            (0x0010, 0x2295), # breedRegistrationNumber - номер регистрации породы
            (0x0010, 0x2297), # responsiblePerson - ответственное лицо
            (0x0010, 0x2299), # responsibleOrganization - ответственная организация
            (0x0010, 0x4000)] # patientComments - комментарии пациента
    dicom_file[(0x0010, 0x1030)].value = 0.0 # patientWeight - вес пацана
    for tag in tags:
        if tag in dicom_file:
            dicom_file[tag].value = "Anonymous"
    return dicom_file

