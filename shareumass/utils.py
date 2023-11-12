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
    sessions = SessionAccount.objects.filter(session_token=session_token)
    if not sessions.exists():
        return None
    return sessions.first().account
