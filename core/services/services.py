from select import select
from core.models import Quote, Policy, Address
from core.constants import active_volcanos_states


term = 6
monthly_base_volcano_policy_price = 59.94


def is_in_danger_zone(state: str) -> bool:
    try:
        active_volcanos_states[state]
        return True
    except KeyError:
        return False


def additional_fees(had_previous_volcano_policy: bool, state: str) -> list:
    additional_fees = []
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
    if had_previous_volcano_policy:
        additional_fees.append(0.15)

    if is_in_danger_zone(state):
        additional_fees.append(0.25)

    return additional_fees


def additional_discounts(never_cancel_volcano_policy: bool, new_property: bool) -> list:
    additional_discounts = []
    """
    Additional Discounts
    ● If the policy holder has never had a previous Volcano Insurance policy canceled,
    a discount is applied in the amount of 10% of the base price.
    ● If the policy holder owns the property to be insured, a discount is applied in the
    amount of 20% of the base price.
    """
    if never_cancel_volcano_policy:
        additional_discounts.append(-0.10)
    if new_property:
        additional_discounts.append(-0.20)

    return additional_discounts


def create_quote(
    address: str = "1600 Pennsylvania Avenue NW, Washington, DC 20500",
    state: str = "DC",
) -> Quote | None:

    fees = additional_fees(False, state)
    discounts = additional_discounts(True, True)

    total = 0

    for fee in fees:
        total += monthly_base_volcano_policy_price * term * fee

    for discount in discounts:
        total += monthly_base_volcano_policy_price * term * discount
