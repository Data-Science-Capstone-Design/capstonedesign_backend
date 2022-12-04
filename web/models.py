from unicodedata import name
from django.db import models
from django.db.models import Model
# Create your models here.

class Document(models.Model):
    uploadedFile = models.FileField('첨부파일',upload_to = "files/")

# Create your models here.
class Candidate(models.Model):
    name = models.CharField(max_length=10)
    introduction = models.TextField()
    area = models.CharField(max_length=15)
    #party_number = models.IntegerField(default=0)
    def __str__(self):
        return 'name : {},introduction : {},area : {}'.format(self.name ,self.introduction, self.area)
