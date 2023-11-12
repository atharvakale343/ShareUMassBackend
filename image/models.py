from django.db import models
from mongoengine import Document, FileField, IntField


class Image(Document):
    posting_id = IntField()
    image_data = FileField()
