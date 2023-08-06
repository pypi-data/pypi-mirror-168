import logging
import time
from urllib.parse import quote, urlencode
from typing import Optional
from re import Pattern

from django.http import HttpResponseRedirect, HttpRequest, JsonResponse, HttpResponse
from django.utils.module_loading import import_string
from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import cached_property
from django.contrib.auth import BACKEND_SESSION_KEY
from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib import auth
from django.urls import reverse


import requests
from mozilla_django_oidc.utils import absolutify, add_state_and_nonce_to_session
from mozilla_django_oidc.middleware import SessionRefresh as SessionRefreshOIDC
from dnoticias_services.authentication.keycloak import get_user_keycloak_info
from mozilla_django_oidc.utils import absolutify, import_from_settings
from mozilla_django_oidc.auth import OIDCAuthenticationBackend

from .utils import set_cookie, get_cookie_equivalency, get_cookie_configuration
from .backends import ExtraClaimsOIDCAuthenticationBackend

User = get_user_model()
logger = logging.getLogger(__name__)


def get_refresh_redirect_url(request):
    OIDC_OP_AUTHORIZATION_ENDPOINT = import_from_settings('OIDC_OP_AUTHORIZATION_ENDPOINT')
    OIDC_RP_CLIENT_ID = import_from_settings('OIDC_RP_CLIENT_ID')
    OIDC_STATE_SIZE = import_from_settings('OIDC_STATE_SIZE', 32)
    OIDC_AUTHENTICATION_CALLBACK_URL = import_from_settings(
        'OIDC_AUTHENTICATION_CALLBACK_URL',
        'oidc_authentication_callback',
    )
    OIDC_RP_SCOPES = import_from_settings('OIDC_RP_SCOPES', 'openid email')
    OIDC_USE_NONCE = import_from_settings('OIDC_USE_NONCE', True)
    OIDC_NONCE_SIZE = import_from_settings('OIDC_NONCE_SIZE', 32)

    auth_url = OIDC_OP_AUTHORIZATION_ENDPOINT
    client_id = OIDC_RP_CLIENT_ID
    state = get_random_string(OIDC_STATE_SIZE)


    # Build the parameters as if we were doing a real auth handoff, except
    # we also include prompt=none.
    params = {
        'response_type': 'code',
        'client_id': client_id,
        'redirect_uri': absolutify(
            request,
            reverse(OIDC_AUTHENTICATION_CALLBACK_URL)
        ),
        'state': state,
        'scope': OIDC_RP_SCOPES,
        'prompt': 'none',
    }

    params.update(import_from_settings('OIDC_AUTH_REQUEST_EXTRA_PARAMS', {}))

    if OIDC_USE_NONCE:
        nonce = get_random_string(OIDC_NONCE_SIZE)
        params.update({
            'nonce': nonce
        })

    add_state_and_nonce_to_session(request, state, params)

    request.session['oidc_login_next'] = request.get_full_path()

    query = urlencode(params, quote_via=quote)

    return '{url}?{query}'.format(url=auth_url, query=query)


class BaseAuthMiddleware:
    @cached_property
    def exempt_url_patterns(self) -> set:
        """Urls that should not be processed by this middleware.
        This is a list of regular expressions.

        :return: set of regular expressions
        :rtype: set
        """
        exempt_patterns = set()

        for url_pattern in settings.AUTH_EXEMPT_URLS:
            if isinstance(url_pattern, Pattern):
                exempt_patterns.add(url_pattern)

        return exempt_patterns

    @cached_property
    def exempt_session_url_patterns(self) -> set:
        """Urls that should not be processed by this middleware in DCS password update session

        :return: set of regular expressions
        :rtype: set"""
        exempt_patterns = set()
        patterns = getattr(settings, "SESSION_CHECK_EXEMPT_URLS", [])

        for url_pattern in patterns:
            if isinstance(url_pattern, Pattern):
                exempt_patterns.add(url_pattern)

        return exempt_patterns 

    def _is_processable(self, request: HttpRequest):
        pass


class SessionRefresh(SessionRefreshOIDC):
    def is_refreshable_url(self, request: HttpRequest) -> bool:
        """Takes a request and returns whether it triggers a refresh examination

        :param request:
        :returns: boolean
        """
        # Do not attempt to refresh the session if the OIDC backend is not used
        backend_session = request.session.get(BACKEND_SESSION_KEY)
        is_oidc_enabled = True
        if backend_session:
            auth_backend = import_string(backend_session)
            is_oidc_enabled = issubclass(auth_backend, OIDCAuthenticationBackend)

        return (
            request.method == 'GET' and
            not any(pat.match(request.path) for pat in self.exempt_url_patterns) and
            request.user.is_authenticated and
            is_oidc_enabled and
            request.path not in self.exempt_urls
        )

    def process_request(self, request: HttpRequest) -> HttpResponse:
        """Takes a request and checks if it can be refreshed (redirects to keycloak silently).

        :param request: The request to be processed
        :returns: The response to the request
        :rtype: HttpResponse
        """
        if not self.is_refreshable_url(request):
            logger.debug('The request is not refreshable')
            return

        # This will use the keycloak token expiration saved in redis session instead of the
        # one saved in django session. This is because we need to refresh the keycloak token
        # for all django sessions instead of just one.
        expiration = request.session.get('oidc_id_token_expiration', 0)
        now = time.time()

        if expiration > now:
            # The id_token is still valid, so we don't have to do anything.
            logger.debug('id token is still valid (%s > %s)', expiration, now)
            return

        logger.debug('id token has expired')

        redirect_url = get_refresh_redirect_url(request)

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Almost all XHR request handling in client-side code struggles
            # with redirects since redirecting to a page where the user
            # is supposed to do something is extremely unlikely to work
            # in an XHR request. Make a special response for these kinds
            # of requests.
            # The use of 403 Forbidden is to match the fact that this
            # middleware doesn't really want the user in if they don't
            # refresh their session.
            response = JsonResponse({'refresh_url': redirect_url}, status=403)
            response['refresh_url'] = redirect_url
            return response

        return HttpResponseRedirect(redirect_url)


class AccessTokenCheck(BaseAuthMiddleware, MiddlewareMixin):
    def _is_processable(self, request: HttpRequest) -> bool:
        """Takes a request and checks if the path can be processed using the regex urls set
        in settings

        :param request: The request to be processed
        :returns: True if the request can be processed, False otherwise
        :rtype: bool
        """
        return (
            not any(pat.match(request.path) for pat in self.exempt_url_patterns) and
            not request.user.is_authenticated
        )

    def process_request(self, request: HttpRequest) -> Optional[HttpResponse]:
        """Processes the request if the request can be processed, then checks if the 
        access token is valid.

        :param request: The request to be processed
        :returns: The response to the request
        :rtpe: HttpResponse, optional
        """
        if not self._is_processable(request):
            return

        access_token_expiration_key = get_cookie_equivalency('oidc_access_token_expiration')
        access_token_expiration_value = (
            request.COOKIES.get(access_token_expiration_key)
            or request.session.get("oidc_access_token_expiration")
        )
        actual_timestamp = int(time.time())

        if access_token_expiration_value and int(access_token_expiration_value) > actual_timestamp:
            logger.info(
                "Access token is still valid (%s > %s)",
                access_token_expiration_value,
                actual_timestamp
            )
            return

        cookies = request.COOKIES
        access_token = cookies.get(get_cookie_equivalency('oidc_access_token'))

        if not access_token:
            return

        redirect_url = get_refresh_redirect_url(request)

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            response = JsonResponse({'refresh_url': redirect_url}, status=403)
            response['refresh_url'] = redirect_url
            return response

        return HttpResponseRedirect(redirect_url)


class TokenMiddleware(BaseAuthMiddleware, MiddlewareMixin):
    """Just generates the cookie if the user is logged in"""
    def __init__(self, get_response):
        self.get_response = get_response

    def _is_processable(self, request: HttpRequest) -> bool:
        """Takes a request and checks if the path can be processed using the regex urls set

        :param request: The request to be processed
        :returns: True if the request can be processed, False otherwise
        :rtype: bool
        """
        return (
            not any(pat.match(request.path) for pat in self.exempt_url_patterns) and
            request.user.is_authenticated
        )

    def _can_check_dcs_session(self, request: HttpRequest) -> bool:
        """Check if the request requires to check the sessionid on dcs

        :param request: httpRequest
        :return: True if the request if processable and the function proceeds to check the ssid
        :rtype: bool
        """
        return (
            not any(pat.match(request.path) for pat in self.exempt_url_patterns)\
            and not any(pat.match(request.path) for pat in self.exempt_session_url_patterns)\
            and not request.user.is_authenticated\
            and request.COOKIES.get("sessionid")
        )

    def __is_user_migrated(self, email: str) -> bool:
        """Check on keycloak if the user has been migrated

        :param email: The user email that we will verify if has been migrated
        :return: True if the user has been migrated
        :rtype: bool
        """
        user_info = get_user_keycloak_info(email)
        return bool(user_info.get("attributes", {}).get("user_migrated", False))

    def check_dcs_cookies(self, request: HttpRequest, http_response: HttpResponse) -> HttpResponse:
        """Check the dcs cookies and redirects to password reset view

        :param request: httpRequest
        :param http_response: httpResponse
        :return: httpResponse
        :rtype: httpResponse
        """
        cookies = request.COOKIES
        session_id = cookies.get("sessionid")
        has_dcs_session_api = getattr(settings, "DCS_SESSION_MIGRATE_API_URL", False)

        # If we dont have a session_id cookie, we just return the initial response
        if not session_id or not has_dcs_session_api:
            return http_response

        dcs_session_api = getattr(settings, "DCS_SESSION_MIGRATE_API_URL")
        # We ask to the DCS the email associated to that session_id. This returns an email if the
        # sessionid is not anon, the user does not have @dnoticias.pt in his email and is not part
        # of the staff or superuser.
        response = requests.post(dcs_session_api, {"session_id": session_id})
        body = response.json()
        logger.debug("[DCS Session] Returned %s", body)

        if response.status_code == 200:
            if not body.get("error"):
                # Gets the email from body
                email = body.get("email")

                if not self.__is_user_migrated(email):
                    # We make an HttpResponseRedirect to the change password view
                    http_response = HttpResponseRedirect(reverse("password-recovery"))

                    request.session["migration_email"] = email
                    request.session["migration_next_url"] = request.build_absolute_uri()
                    request.session.save()

                # Deletes the sessionid cookie
                extra_data = get_cookie_configuration()
                extra_data.pop('expires', None)
                extra_data.pop('secure', None)
                extra_data.pop('httponly', None)
                http_response.delete_cookie('sessionid', **extra_data)

        return http_response

    def process_response(self, request: HttpRequest, response: HttpResponse) -> HttpResponse:
        """Processes the response if the request can be processed. This will check if the
        user is logged in to set the cookies needed to make all the systems work.

        :param request: The request to be processed
        :param response: The response to the request
        :returns:returns: The response to the request
        :rtype: HttpResponse
        """
        if self._can_check_dcs_session(request):
            response = self.check_dcs_cookies(request, response)

        if self._is_processable(request):
            oidc_login_cookie = get_cookie_equivalency('oidc_login_next')
            keycloak_session_cookie = get_cookie_equivalency('keycloak_session_id')
            access_token_cookie = get_cookie_equivalency('oidc_access_token')
            access_token_expiration_cookie = get_cookie_equivalency('oidc_access_token_expiration')

            oidc_login_value = request.session.get('oidc_login_next', '')
            keycloak_session_value = request.session.get('keycloak_session_id', {})
            access_token_value = request.session.get('oidc_access_token', '')
            access_token_expiration_value = request.session.get('oidc_access_token_expiration', '')

            response = set_cookie(oidc_login_cookie, oidc_login_value, response)
            response = set_cookie(access_token_cookie, access_token_value, response)
            response = set_cookie(
                access_token_expiration_cookie,
                access_token_expiration_value,
                response
            )

            if keycloak_session_value:
                response = set_cookie(keycloak_session_cookie, keycloak_session_value, response)

        return response
