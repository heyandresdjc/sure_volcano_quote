from django.utils import timezone
from core.models import Quote, Policy


def checkout(quote_number: str) -> Policy | None:
    quote = Quote.objects.get(quote_number=quote_number)
    return Policy.objects.create(
        policy_number=quote_number,
        address=quote.address,
        total_monthly_premium=quote.total_monthly_premium,
        effective_date=timezone.now(),
        quote=quote,
    )
