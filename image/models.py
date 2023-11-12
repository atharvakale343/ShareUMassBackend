from django.db import models


class Image(models.Model):
    posting_id = models.IntegerField()
    image_data = models.FileField()
