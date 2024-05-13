from django.db import models
from users.models import CustomUser

class UploadFiles(models.Model):
    file = models.FileField(upload_to='uploads/')  # Поле для хранения загруженного файла
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Поле для хранения даты и времени загрузки файла
    uploaded_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='uploaded_files', blank=True, null=True)  # Внешний ключ для связи с пользователем, который загрузил файл

    def __str__(self):
        return self.file.name  # files name