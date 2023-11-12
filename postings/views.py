from django.db import IntegrityError
from image.views import process_image_to_db, get_image_from_db
from postings.models import Posting
from shareumass.authorization import RequestToken, authorized, authorized_view
from shareumass.utils import get_session_from_session_token


from django.forms import model_to_dict
from django.http import HttpRequest, JsonResponse
from rest_framework.views import APIView

from user.models import Account
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector


def validate_posting_data(params: dict):
    success, error_json, posting_dict = True, None, None
    try:
        posting_dict = {
            "product_name": params["product_name"],
            "condition": params["condition"],
            "price": float(params["price"]),
            "description": params["description"],
            "residential_hall": params["residential_hall"],
            "categories": params["categories"].split(","),
        }
        success = True
    except KeyError as e:
        error_json = JsonResponse(
            {
                "message": "failed to create posting",
                "error": repr(e),
            },
            status=400,
        )
        success = False
    return success, error_json, posting_dict


def create_or_update_posting(account: Account, posting_dict: dict):
    success, error_json, posting = True, None, None

    if "id" in posting_dict:
        raise NotImplementedError
    else:
        try:
            posting = Posting.objects.create(account=account, **posting_dict)
        except IntegrityError as e:
            success = False
            error_json = JsonResponse(
                {
                    "message": "failed to create posting",
                    "error": repr(e),
                },
                status=400,
            )

    return success, error_json, posting


class UserPosting(APIView):
    @authorized_view
    def post(self, request: HttpRequest, token: RequestToken) -> JsonResponse:
        session_token = str(token)
        success, error_json, account = get_session_from_session_token(session_token)
        if not success:
            return error_json

        params = request.data

        success, error_json, posting_dict = validate_posting_data(params)
        if not success:
            return error_json

        success, error_json, posting = create_or_update_posting(account, posting_dict)
        if not success:
            return error_json

        success, error_json, image = process_image_to_db(posting_id=posting.id, image_data=params["image"])
        if not success:
            posting.delete()
            return error_json

        response = {
            "message": "posting successfully created",
            "posting": model_to_dict(posting),
        }
        return JsonResponse(
            response,
            status=200,
        )


class PostingsView(APIView):
    @authorized_view
    def post(self, request: HttpRequest, token: RequestToken) -> JsonResponse:
        session_token = str(token)
        success, error_json, account = get_session_from_session_token(session_token)
        if not success:
            return error_json

        params = request.data

        user_flag = params.get("user", False)
        query_text = params.get("queryText", None)

        search_postings = Posting.objects.all()

        if "residentialHall" in params and params["residentialHall"]:
            search_postings = search_postings.filter(
                residential_hall__icontains=params.get("residentialHall")
            )

        if "categories" in params and params["categories"]:
            search_postings = search_postings.filter(categories__overlap=params.get("categories"))

        if query_text:
            search_postings = search_postings.annotate(
                search=SearchVector(*["product_name", "description"])
            ).filter(search=query_text)

        if user_flag:
            search_postings = search_postings.filter(account=account)

        return JsonResponse(
            data={
                "message": "retrieved postings for logged in user",
                "postings": [
                    model_to_dict(result)
                    | {"picture": get_image_from_db(result.id)}
                    | {"sellerId": result.account.email}
                    for result in search_postings
                ],
            },
            status=200,
        )
