from django import forms
from .models import Document

class PostForm(forms.ModelForm):
    class Meta:
        model=Document
        fields='__all__'

def handle_uploaded_file(f):
    with open('web/media/files/data.xlsx', 'wb+') as destination:
        for chunk in f.chunks():
            print(chunk)
            destination.write(chunk)

class UploadFileForm(forms.Form):
    # title = forms.CharField(max_length=50)
    file = forms.FileField()