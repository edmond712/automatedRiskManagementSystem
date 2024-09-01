from django import forms

class FileUploadForm(forms.Form):
    project_file = forms.FileField()
    mitigation_matrix = forms.FileField(label='Выберите Excel файл с матрицей снижения рисков')

