## models.py
from djongo import models


class Resumes(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    resume_pdf = models.AutoField()

    def __str__(self):
        return self.name,self.contact