from django import forms
# from .models import File

class FileUploadForm(forms.Form):
    file = forms.FileField()

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if not file:
            raise forms.ValidationError('Нужно выбрать файл для загрузки')
        return file

    def handle_uploaded_file(self, file):
        # Здесь можно обработать загруженный файл
        # Например, сохранить его на диск или выполнить другие операции
        with open(f'uploads/{file.name}', 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)