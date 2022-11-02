from django.db import models
from django.db.models import Model
# Create your models here.

class Document(models.Model):
    uploadedFile = models.FileField('첨부파일',upload_to = "files/")
