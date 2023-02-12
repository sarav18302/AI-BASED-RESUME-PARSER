## models.py
from djongo import models
from djongo.storage import GridFSStorage
from django.conf import settings
grid_fs_storage = GridFSStorage(collection='myfiles', base_url=''.join([settings.BASE_URL, 'myfiles/']))


class Resumes(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    resume_pdf = models.AutoField(storage=grid_fs_storage)

    def __str__(self):
        return self.name,self.contact

