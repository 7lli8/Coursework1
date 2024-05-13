from django import forms
# from .models import File

class FileUploadForm(forms.Form):
    file = forms.FileField(label = "Файл")
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if not file:
            raise forms.ValidationError('Нужно выбрать файл для загрузки')
        return file



