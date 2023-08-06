import logging
from time import time

from django.views.decorators.clickjacking import xframe_options_exempt
from django.core.exceptions import SuspiciousOperation
from django.http.response import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import View, FormView
from django.http import Http404, HttpResponse
from django.urls import reverse_lazy
from django.shortcuts import render
from django.conf import settings
from django.contrib import auth

from mozilla_django_oidc.views import (
    OIDCLogoutView,
    OIDCAuthenticationCallbackView
)


from .forms import PasswordRecoveryDCSForm
from .utils import (
    delete_oidc_cookies,
    delete_user_sessions,
    get_cookie_equivalency,
    refresh_keycloak_token,
)

logger = logging.getLogger(__name__)


class SilentCheckSSOView(View):
    @method_decorator(xframe_options_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        """Get the actual timestamp and the oidc access token expiration timestamp defined before
        to check if a refresh is needed. If the refresh is needed, the user is redirected to the 
        login page, if the session is still valid on KC, the user will be redirected again to this
        page, and the middlewares will be executed and set the new session data with the new
        access token cookies.
        """
        actual_timestamp = int(time())
        expiration_timestamp = request.session.get("oidc_access_token_expiration", 0)
        return render(request, "authentication/silent-check-sso.html", locals())


class DnoticiasOIDCLogoutView(OIDCLogoutView):
    http_method_names = ['get', 'post']

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    @property
    def redirect_url(self) -> str:
        """
        This function was created using the keycloak redirect URL as a LOGOUT_REDIRECT_URL
        /auth/realms/<realm>/protocol/openid-connect/logout?redirect_uri=<URL>

        If we provide a next value via POST, the redirect_uri will be that value.
        If we do not have a next value, the redirect_uri will be the base url.
        """
        logout_url = self.get_settings('LOGOUT_REDIRECT_URL', None)
        base_url = self.get_settings('BASE_URL', None)
        next_url = self.request.POST.get('next') or self.request.GET.get('next', '') or base_url

        if not logout_url:
            logout_url = ''
            logger.warning("No LOGOUT_REDIRECT_URL configured!")

        if not base_url:
            base_url = '/'
            logger.warning("No BASE_URL configured! Using / as default...")

        return logout_url + next_url if logout_url else base_url

    def post(self, request) -> HttpResponseRedirect:
        """
        This method extends the original oidc logout method and aditionally deletes
        the authentication cookies
        """
        keycloak_session_id = request.session.get("keycloak_session_id")
        cookies: dict = request.COOKIES

        if not keycloak_session_id:
            keycloak_session_id = cookies.get(get_cookie_equivalency("keycloak_session_id"))

        delete_user_sessions(keycloak_session_id)
        super().post(request)

        return delete_oidc_cookies(self.redirect_url, request.COOKIES)


class DnoticiasOIDCAuthenticationCallbackView(OIDCAuthenticationCallbackView):
    def login_failure(self, delete_cookies: bool = False) -> HttpResponse:
        response = HttpResponseRedirect(self.failure_url)

        if delete_cookies:
            response = delete_oidc_cookies(self.failure_url, self.request.COOKIES)

        return response

    def get(self, request):
        """Callback handler for OIDC authorization code flow"""

        if request.GET.get('error'):
            # Ouch! Something important failed.

            # Delete the state entry also for failed authentication attempts
            # to prevent replay attacks.
            if ('state' in request.GET
                    and 'oidc_states' in request.session
                    and request.GET['state'] in request.session['oidc_states']):
                del request.session['oidc_states'][request.GET['state']]
                request.session.save()

            # Make sure the user doesn't get to continue to be logged in
            # otherwise the refresh middleware will force the user to
            # redirect to authorize again if the session refresh has
            # expired.
            if request.user.is_authenticated:
                delete_user_sessions(request.COOKIES.get("keycloak_session_id"))
                auth.logout(request)
            assert not request.user.is_authenticated
        elif 'code' in request.GET and 'state' in request.GET:

            # Check instead of "oidc_state" check if the "oidc_states" session key exists!
            if 'oidc_states' not in request.session:
                return self.login_failure()

            # State and Nonce are stored in the session "oidc_states" dictionary.
            # State is the key, the value is a dictionary with the Nonce in the "nonce" field.
            state = request.GET.get('state')
            if state not in request.session['oidc_states']:
                msg = 'OIDC callback state not found in session `oidc_states`!'
                raise SuspiciousOperation(msg)

            # Get the nonce from the dictionary for further processing and delete the entry to
            # prevent replay attacks.
            nonce = request.session['oidc_states'][state]['nonce']
            del request.session['oidc_states'][state]

            # I've just rewrote the OIDC callback view to set the keycloak session data on django
            # session. This will save and set each django session in each client on a redis session
            # key, which is then used to delete the user sessions on KC and logout all the clients
            # at the same time.
            if request.session.get('oidc_refresh_token'):
                access_token, refresh_token, access_token_expiration = \
                    refresh_keycloak_token(request.session['oidc_refresh_token'])

                request.session["oidc_access_token_expiration"] = access_token_expiration
                request.session["oidc_access_token"] = access_token
                request.session["oidc_refresh_token"] = refresh_token

            # Authenticating is slow, so save the updated oidc_states.
            request.session.save()
            # Reset the session. This forces the session to get reloaded from the database after
            # fetching the token from the OpenID connect provider.
            # Without this step we would overwrite items that are being added/removed from the
            # session in parallel browser tabs.
            request.session = request.session.__class__(request.session.session_key)

            kwargs = {
                'request': request,
                'nonce': nonce,
            }

            self.user = auth.authenticate(**kwargs)

            if self.user and self.user.is_active:
                return self.login_success()

        return self.login_failure(delete_cookies=True)


class ApplicationDataView(View):
    # TODO: I think this is not used anymore.
    template_name = "authentication/app-data.html"

    def get(self, request, *args, **kwargs):
        next_url = request.GET.get("next_url")

        access_token = request.session.get("oidc_access_token")
        refresh_token = request.session.get("oidc_refresh_token")
        access_token_expires_in = request.session.get("oidc_expires_in")
        refresh_token_expires_in = request.session.get("oidc_refresh_expires_in")

        return render(request, self.template_name, locals())


class PasswordRecoveryDCSFormView(FormView):
    template_name = "authentication/password-recovery.html"
    form_class = PasswordRecoveryDCSForm

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get("migration_email"):
            raise Http404()

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        next_url = self.request.session.get("migration_next_url")
        login_url = reverse_lazy("oidc_authentication_init")
        return f"{login_url}?next_url={next_url}"

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        next_url = self.request.session.get('migration_next_url')
        reset_url = settings.OIDC_RESET_PASSWORD_URL
        context["password_recovery_url"] = f"{reset_url}?next={next_url}"
        return context

    def get_form_kwargs(self) -> dict:
        kwargs = super().get_form_kwargs()
        kwargs["email"] = self.request.session.get("migration_email")
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)
