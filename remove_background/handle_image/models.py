from django.db import models

# Create your models here.


class ImageUploaded(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField(blank=False, null=True)

    def __str__(self):
        return str(self.id) + ' - ' + str(self.date)
