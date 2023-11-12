from django.http import JsonResponse
from django.shortcuts import render
from django.core.files.base import ContentFile
from image.models import Image
import base64


def process_image_to_db(posting_id: int, image_data: str):
    success, error_json, image = True, None, None
    try:
        image = put_image_in_db(posting_id, image_data)
    except Exception as e:
        success = False
        error_json = JsonResponse(
            {
                "message": "failed to create post image to database",
                "error": repr(e),
            },
            status=400,
        )
    return success, error_json, image


def put_image_in_db(posting_id: int, image_data: str):
    format, img_str = image_data.split(";base64,")
    ext = format.split("/")[-1]

    store_data = ContentFile(base64.b64decode(img_str), name="img." + ext)

    img = Image()
    img.posting_id = posting_id
    img.image_data.put(store_data)

    img.save()
    return img


def get_image_from_db(posting_id: int):
    return (
        Image.objects(posting_id=posting_id).using("images").first().image_data.read()
    )
