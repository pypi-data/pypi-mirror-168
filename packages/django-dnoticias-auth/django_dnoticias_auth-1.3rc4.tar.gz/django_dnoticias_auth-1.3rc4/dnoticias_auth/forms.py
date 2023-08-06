from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.conf import settings
from django import forms

import requests
from dnoticias_services.authentication.keycloak import (
    create_user,
    update_user,
    update_password,
    keycloak_user_exists,
)

User = get_user_model()


class PasswordRecoveryDCSForm(forms.Form):
    actual_password = forms.CharField(
        label=_("Senha atual"),
        max_length=128,
        widget=forms.PasswordInput
    )
    new_password = forms.CharField(
        label=_("Nova senha"),
        max_length=128,
        widget=forms.PasswordInput
    )
    repeat_password = forms.CharField(
        label=_("Repita a senha"),
        max_length=128,
        widget=forms.PasswordInput
    )

    def __init__(self, **kwargs):
        self.email = kwargs.pop("email", None)
        super().__init__(**kwargs)

    def is_valid(self) -> bool:
        """Checks if the form is valid and if the new password is valid

        :return: True if the form is valid and the new password is valid, False otherwise.
        :rtype: bool
        """
        if not super().is_valid():
            return False

        valid = True
        actual_password = self.cleaned_data.get("actual_password")
        new_password = self.cleaned_data.get("new_password")
        repeat_password = self.cleaned_data.get("repeat_password")

        # Checks against the DCS if the actual password is OK
        headers = {'Authorization': 'Token {}'.format(settings.DCS_TOKEN)}
        response = requests.post(
            settings.DCS_USER_LOGIN_API_URL,
            data={"email": self.email, "password": actual_password},
            headers=headers
        )
        invalid_password = ValidationError(_("A senha atual não é válida"))

        if response.status_code == 200:
            body = response.json()
            # If the password does not match with the user, will return OK with DENIED, but
            # to be more relaxed we check if one of the following params are different
            if not body.get("result") == "OK"\
                or not body.get("reason") == "SUCCESS"\
                or not body.get("token"):
                valid = False
                self.add_error("actual_password", invalid_password)
        else:
            self.add_error("actual_password", invalid_password)

        if new_password != repeat_password:
            valid = False
            self.add_error("new_password", ValidationError(_("As senhas digitadas não coincidem")))

        # This will validates if the password meets the minimum security requirements
        try:
            validate_password(new_password)
        except ValidationError as error:
            valid = False
            # The exception return a list of errors in messages attr
            [self.add_error("new_password", ValidationError(message)) for message in error.messages]

        return valid

    def save(self):
        """Creates or updates a new user and adds the 'user_migrated' attribute on keycloak"""
        new_password = self.cleaned_data.get("new_password")
        custom_attributes = {"user_migrated": True}

        if not keycloak_user_exists(self.email):
            create_user(
                self.email,
                password=new_password,
                temporary_password=False,
                custom_attributes=custom_attributes,
            )
        else:
            update_password(self.email, password=new_password, temporary=False)
            update_user(self.email, custom_attributes=custom_attributes)
