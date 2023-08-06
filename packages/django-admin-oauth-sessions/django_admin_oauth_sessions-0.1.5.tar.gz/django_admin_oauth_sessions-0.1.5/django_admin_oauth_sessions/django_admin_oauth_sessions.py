from django.conf import settings
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import redirect
from django.urls import reverse

from django_admin_oauth_sessions.backends import DjangoAdminAuthKeycloak
from django_admin_oauth_sessions.utils import get_user_from_django_session


class DjangoAdminOAuthSessionMiddleware:
    def __init__(self, get_response):
        if not hasattr(settings, 'KEYCLOAK') or \
                not settings.KEYCLOAK.get('BASE_URL') \
                or not settings.KEYCLOAK.get('CLIENT_ID'):
            raise ImproperlyConfigured(
                "Keycloak configuration missing in"
                " setting file. Plz make sure that "
                "the following is there in keycloak"
                "setting BASE_URL,CLIENT_ID,CLIENT_SECRET"
                "acquire_service_token endpoint.")
        if not hasattr(settings, "TESTING"):
            raise ImproperlyConfigured(
                "Please Configure TESTING variable in django settings. "
                "This is to make sure that custom auth is not running "
                "from test env.")
        if getattr(settings, "CHECK_INTERNAL_USER", False) and \
                not hasattr(settings, "INTERNAL_USER_ROLE"):
            raise ImproperlyConfigured(
                "With CHECK_INTERNAL_USER enabled providing the value"
                " of INTERNAL_USER_ROLE is mandatory. Please provide"
                " INTERNAL_USER_ROLE in django settings")
        self.get_response = get_response
        if not settings.TESTING:
            self.custom_auth_obj = DjangoAdminAuthKeycloak()

    def __call__(self, request):
        try:
            if not settings.TESTING and hasattr(request, "COOKIES") \
                    and request.COOKIES.get("sessionid") \
                    and self.check_request_path(request):
                user = get_user_from_django_session(request)
                if not self.custom_auth_obj.authenticate(request,
                                                         user=user):
                    session_key = request.COOKIES.get("sessionid")
                    Session.objects.filter(
                        session_key=session_key).delete()
                    msg = messages.get_messages(request)
                    for message in msg:
                        pass
                    messages.error(request,
                                   "Access Denied, you do not have required"
                                   " permission to access this page")
                    return redirect(reverse('login'))
        except Session.DoesNotExist as e:
            pass
        except Exception as e:
            return redirect(reverse('login'))

        response = self.get_response(request)

        return response

    def check_request_path(self, request):
        parts = set(request.path.split("/"))

        if "login" in parts or "keycloak" in parts or "logout" in parts:
            return False
        if "admin" in parts:
            return True

        return False
