from django.db import models
from files.validators import validate_file_extension
from users.models import CustomUser


class CustomFiles(models.Model):
    file = models.FileField(upload_to='uploads/', validators=[validate_file_extension])  # Поле для хранения загруженного файла
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Поле для хранения даты и времени загрузки файла
    uploaded_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='uploaded_files', blank=True,
                                    null=False)  # Внешний ключ для связи с пользователем, который загрузил файл
    file_name = models.CharField(max_length=255)

    def __str__(self):
        return self.file_name  # files path

    def save(self, *args, **kwargs):
        self.file_name = self.file.name
        super().save(*args, **kwargs)
