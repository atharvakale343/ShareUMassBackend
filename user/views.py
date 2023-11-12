from shareumass.authorization import RequestToken, authorized_view
from shareumass.utils import get_session_from_session_token


from django.forms import model_to_dict
from django.http import HttpRequest, JsonResponse
from rest_framework.views import APIView


class GetAccount(APIView):
    @authorized_view
    def get(self, request: HttpRequest, token: RequestToken) -> JsonResponse:
        session_token = str(token)

        success, error_json, account = get_session_from_session_token(session_token)
        if not success:
            return error_json

        dict_user = model_to_dict(account)
        return JsonResponse(
            dict_user,
            status=200,
        )
