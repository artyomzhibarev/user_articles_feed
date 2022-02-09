from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.contrib.auth.password_validation import NumericPasswordValidator


class LiteralNumericPasswordValidator(NumericPasswordValidator):
    """
    Validate whether the password is alphanumeric.
    """
    def validate(self, password, user=None):
        super().validate(password)
        if password.isalpha():
            raise ValidationError(
                _("This password is entirely alphabetic."),
                code='password_entirely_alphabetic',
            )

    def get_help_text(self):
        return _('Your password can’t be entirely numeric or alphabetic.')
