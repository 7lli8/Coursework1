# from django.db import models
# from django.contrib.auth.models import User
# class File(models.Model):
#     file = models.FileField(upload_to='files/')
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files')
#
#     def __str__(self):
#         return self.file.name
#
#     @property
#     def name(self):
#         return self.file.name