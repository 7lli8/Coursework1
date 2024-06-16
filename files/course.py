import base64
import io
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

            """ 
            НАДО УБРАТЬ
            !!!!!!!!!!!!!!!!!!!!!!!
            """


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

