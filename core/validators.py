import json
import pgeocode
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from core.constants import states


def zip_code_validator(zip_code: str) -> None:
    country: str = "us"
    nomi = pgeocode.Nominatim(country)
    if json.loads(nomi.query_postal_code(zip_code).to_json())["country_code"] is None:
        raise ValidationError(
            _("%(value) is not valid zip code"),
            params={"value": zip_code},
        )


def state_validator(state_name: str) -> None:
    if state_name not in [st_name for st_name in states]:
        raise ValidationError(
            _("%(value) is not valid state name"),
            params={"value": state_name},
        )
