import re
import logging
from datetime import datetime
from core.models import Quote, Policy, Address
from core.constants import active_volcanos_states
from django.utils.crypto import get_random_string


logger = logging.getLogger(__name__)

term = 6
monthly_base_volcano_policy_price = 59.94


def is_in_danger_zone(state: str) -> bool:
    try:
        return bool(active_volcanos_states[state])
    except KeyError:
        return False


def address_parser(raw_address: str) -> Address:
    regexp = "[0-9]{1,3} .+, .+, [A-Z]{2} [0-9]{5}"
    address = re.findall(regexp, raw_address)
    # address = ['44 West 22nd Street, New York, NY 12345']
    addr, _ = Address.objects.get_or_create(
        address=address[0],
        state=address[1],
        zip_code=address[2].split(" ")[1],
    )
    return addr


def additional_fees(had_previously_cancel_volcano_policy: bool, state: str) -> list:
    additional_fees_array = []
    """
    Additional Fees
        ● If the policy holder has ever had a previous Volcano Insurance policy canceled,
        an additional fee is applied in the amount of 15% of the base price.
        
        ● If the policy holder's property is in a state with a volcano,
        an additional fee is applied in the amount of 25% of the base price,
        regardless of the distance the property is from an active volcano.
            ○ This fee is in addition to the fees mentioned above.
            ○ US States with active volcanoes are:
                ■ Alaska
                ■ Arizona
                ■ California
                ■ Colorado
                ■ Hawaii
                ■ Idaho
                ■ Nevada
                ■ New Mexico
                ■ Oregon
                ■ Utah
                ■ Washington
                ■ Wyoming
    """
    if had_previously_cancel_volcano_policy:
        additional_fees_array.append(0.15)

    if is_in_danger_zone(state):
        additional_fees_array.append(0.25)

    return additional_fees_array


def additional_discounts(never_cancel_volcano_policy: bool, new_property: bool) -> list:
    additional_discounts_array = []
    """
    Additional Discounts
    ● If the policy holder has never had a previous Volcano Insurance policy canceled,
    a discount is applied in the amount of 10% of the base price.
    ● If the policy holder owns the property to be insured, a discount is applied in the
    amount of 20% of the base price.
    """
    if never_cancel_volcano_policy:
        additional_discounts_array.append(-0.10)
    if new_property:
        additional_discounts_array.append(-0.20)

    return additional_discounts_array


def create_quote(
        effective_date: datetime,
        had_previously_cancel_volcano_policy: bool,
        never_cancel_volcano_policy: bool,
        new_property: bool,
        previously_cancel_policy: Policy = None,
        address: str = "1600 Pennsylvania Avenue NW, Washington, DC 20500",
        state: str = "DC",
) -> Quote | None:

    random_string_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

    quote_number = get_random_string(length=10, allowed_chars=random_string_chars)
    fees = additional_fees(had_previously_cancel_volcano_policy, state)
    discounts = additional_discounts(never_cancel_volcano_policy, new_property)

    total_term_premium = monthly_base_volcano_policy_price * term
    total_monthly_premium = monthly_base_volcano_policy_price

    total_additional_fee = sum([x * total_term_premium for x in fees])
    total_monthly_fee = sum([x * total_monthly_premium for x in fees])

    total_discount = sum([x * total_term_premium for x in discounts])
    total_monthly_discount = sum([x * total_monthly_premium for x in discounts])

    try:
        address = address_parser(address)
        return Quote.objects.create(
            quote_number=quote_number,
            effective_date=effective_date,
            previously_cancel_policy=previously_cancel_policy,
            address=address,
            total_term_premium=total_term_premium,
            total_monthly_premium=total_monthly_premium,
            total_additional_fee=total_additional_fee,
            total_monthly_fee=total_monthly_fee,
            total_discount=total_discount,
            total_monthly_discount=total_monthly_discount
        )
    except Quote.MultipleObjectsReturned:
        pass
    except Exception as ex:
        logger.error(
            msg="Failed to create policy",
            exc_info=ex
        )

    return None
