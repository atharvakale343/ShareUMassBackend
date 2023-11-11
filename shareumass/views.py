import json
from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.shortcuts import redirect, render, redirect
from django.urls import reverse
from urllib.parse import quote_plus, urlencode

from shareumass.utils import create_user_if_not_exists
from .authorization import RequestToken, authorized, can, getRequestToken
from django.http import HttpRequest, JsonResponse

oauth = OAuth()

oauth.register(
    "auth0",
    client_id=settings.AUTH0_CLIENT_ID,
    client_secret=settings.AUTH0_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f"https://{settings.AUTH0_DOMAIN}/.well-known/openid-configuration",
)


def index(request):
    return render(
        request,
        "index.html",
        context={
            "session": request.session.get("user"),
            "pretty": json.dumps(request.session.get("user"), indent=4),
        },
    )


def callback(request):
    token = oauth.auth0.authorize_access_token(request)
    request.session["user"] = token

    email = token["email"]
    create_user_if_not_exists(token)
    return redirect(f"{settings.FRONTEND_SERVICE_URL}?token={token['id_token']}&email={email}")


def login(request):
    return oauth.auth0.authorize_redirect(request, request.build_absolute_uri(reverse("callback")))


def logout(request):
    request.session.clear()
    return redirect(
        f"https://{settings.AUTH0_DOMAIN}/v2/logout?"
        + urlencode(
            {
                "returnTo": settings.FRONTEND_SERVICE_URL,
                "client_id": settings.AUTH0_CLIENT_ID,
            },
            quote_via=quote_plus,
        ),
    )


def public(request: HttpRequest()) -> JsonResponse:
    token: RequestToken | None = getRequestToken(request)

    return JsonResponse(
        data={
            "message": "Hello from a public endpoint! You don't need to be authenticated to see this.",
            "token": token.dict() if token is not None else None,
        }
    )


@authorized
def private(request: HttpRequest, token: RequestToken) -> JsonResponse:
    return JsonResponse(
        data={
            "message": "Hello from a private endpoint! You need to be authenticated to see this.",
            "token": token.dict(),
        }
    )


@can("read:messages")
def privateScoped(request: HttpRequest, token: RequestToken) -> JsonResponse:
    return JsonResponse(
        data={
            "message": "Hello from a private endpoint! You need to be authenticated and have a scope of read:messages to see this.",
            "token": token.dict(),
        }
    )
