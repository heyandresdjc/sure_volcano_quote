import json
import pgeocode
from pandas.core.series import Series
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def zip_code_validator(zip_code: str) -> None:
    country: str = "us"
    nomi = pgeocode.Nominatim(country)
    if json.loads(nomi.query_postal_code(zip_code).to_json())["country_code"] is None:
        raise ValidationError(
            _("%(value)s is not an even number"),
            params={"value": zip_code},
        )
