from django.db import models

# Create your models here.


class ImageUploaded(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField(blank=False, null=True)

    class Meta:
        db_table = 'image_uploaded'
        ordering = ('id', )
        verbose_name = "Image Uploaded"
        verbose_name_plural = "Images Uploaded"

    def __str__(self):
        return str(self.id) + ' - ' + str(self.date)


class LogError(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField(blank=False, null=True)
    description = models.CharField(
        max_length=500, blank=False, null=False, default=''
    )

    class Meta:
        db_table = 'log_error'
        ordering = ('id', )
        verbose_name = "Log Error"
        verbose_name_plural = "Log Errors"
