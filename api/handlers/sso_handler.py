from urllib.parse import quote_plus, urlencode

from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse


class SSOHandler:
    def __init__(self, auth0_client_id, auth0_client_secret, auth0_domain):
        self.oauth = OAuth()
        self.oauth.register(
            "auth0",
            client_id=auth0_client_id,
            client_secret=auth0_client_secret,
            client_kwargs={
                "scope": "openid profile email",
            },
            server_metadata_url=f"https://{auth0_domain}/.well-known/openid-configuration",
        )

    def callback(self, request):
        token = self.oauth.auth0.authorize_access_token(request)
        request.session["user"] = token
        user_info = request.session["user"]["userinfo"]
        user, created = User.objects.get_or_create(email=user_info["email"])
        if created:
            user = User.objects.get(email=user_info["email"])
            user.username = user_info.get("nickname")
            user.first_name = user_info.get("given_name")
            user.last_name = user_info.get("family_name")
            user.email = user_info.get("email")
            user.save()
            messages.success(
                request,
                "The profile has been successfully created! Please contact the administrator to activate your profile.",
            )
            return redirect(request.build_absolute_uri(reverse("admin:index")))
        login(request, user)
        return redirect(request.build_absolute_uri(reverse("admin:index")))

    def login(self, request):
        return self.oauth.auth0.authorize_redirect(
            request, request.build_absolute_uri(reverse("sso_callback"))
        )

    def logout(self, request):
        request.session.clear()
        return redirect(
            f"https://{settings.AUTH0_DOMAIN}/v2/logout?"
            + urlencode(
                {
                    "returnTo": request.build_absolute_uri(
                        reverse("admin:index")
                    ),
                    "client_id": settings.AUTH0_CLIENT_ID,
                },
                quote_via=quote_plus,
            ),
        )
