from django.http import JsonResponse
from user.models import Account, SessionAccount

USER_INFO = "userinfo"


def create_user_if_not_exists_and_update(token: dict) -> Account:
    email = token[USER_INFO]["email"]
    name = token[USER_INFO]["name"]
    picture_url = token[USER_INFO]["picture"]
    session_token = token["id_token"]

    accounts = Account.objects.filter(email=email)
    if not accounts.exists():
        account = Account.objects.create_user(email=email, name=name, picture_url=picture_url)
        SessionAccount.objects.create(account=account, session_token=session_token)
        return account

    account = accounts.first()
    session = SessionAccount.objects.filter(account=account).first()
    session.session_token = session_token
    session.save()
    return account


def get_session_from_session_token(session_token: str) -> SessionAccount | None:
    success, error_json, account = True, None, None
    sessions = SessionAccount.objects.filter(session_token=session_token)
    if not sessions.exists():
        success = False
        error_json = JsonResponse(
            {"errors": "Account is not logged in or an invalid session token was provided"},
            status=401,
        )
    else:
        account = sessions.first().account
    return success, error_json, account
