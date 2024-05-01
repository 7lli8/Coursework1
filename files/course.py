import pydicom as dicom
from pydicom.errors import InvalidDicomError

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