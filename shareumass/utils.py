from user.models import Account


def create_user_if_not_exists(token: dict):
    email = token["email"]
    name = token["name"]
    if not Account.objects.get(email=email):
        Account.objects.create_user(email, name)
