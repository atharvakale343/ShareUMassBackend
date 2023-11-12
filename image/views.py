from django.shortcuts import render
from django.core.files.base import ContentFile
from image.models import Image
import base64


def create_db_entry(posting_id, image_data):
    format, img_str = image_data.split(";base64,")
    ext = format.split("/")[-1]
    store_data = ContentFile(base64.b64decode(img_str), name="img." + ext)
    img = Image(posting_id=posting_id, image_data=store_data)
    img.save(using="images")


def get_db_entry(posting_id):
    return (
        Image.objects.filter(posting_id=posting_id).using("images").first().image_data
    )
