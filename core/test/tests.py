from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from core.models import Quote, Address, Policy
from core.services.policies.services import checkout
from core.services.quotes.services import (
    additional_fees,
    is_in_danger_zone,
    address_parser,
    additional_discounts,
    calculate_total_discount,
    create_quote,
)

User = get_user_model()


class QuoteCreationTestsCases(APITestCase):
    def setUp(self) -> None:
        self.credentials = {"username": "cunderwood", "password": "welcomeToDC123"}
        self.user = User.objects.create_user(**self.credentials)
        self.token, _ = Token.objects.get_or_create(user=self.user)
        self.client.force_authenticate(user=self.user, token=self.token)
        self.url = "http://0.0.0.0:8000/api/quotes/"

    def test_create_quote_with_api(self):
        """
        Ensure we can create a new account object.
        """

        data = {
            "policy_holder": "Frank Underwood",
            "had_previously_cancel_volcano_policy": True,
            "never_cancel_volcano_policy": True,
            "new_property": True,
            "address": "1600 Pennsylvania Avenue NW, Washington, DC 20500",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED, msg=response.data
        )
        self.assertGreater(Quote.objects.all().count(), 0, msg=response.data)


class QuoteServiceLayerTestCase(APITestCase):
    def test_additional_fees_had_cancel_policy_in_danger_zone(self):
        fees = additional_fees(True, "AK")
        self.assertEqual(len(fees), 2)

    def test_additional_fees_did_not_have_cancel_policy_but_in_danger_zone(self):
        fees = additional_fees(False, "AK")
        self.assertEqual(len(fees), 1)

    def test_additional_fees_did_not_have_cancel_policy_and_not_in_danger_zone(self):
        fees = additional_fees(False, "TX")
        self.assertEqual(len(fees), 0)

    def test_in_danger_zone(self):
        self.assertTrue(is_in_danger_zone("AK"))

    def test_not_in_danger_zone(self):
        self.assertFalse(is_in_danger_zone("WI"))

    def test_address_parser_with_valid_state(self):
        address = address_parser("1600 Pennsylvania Avenue NW, Washington, DC 20500")
        self.assertIsInstance(address, Address)

    def test_address_parser_with_invalid_state(self):
        address = address_parser("1600 Pennsylvania Avenue NW, Washington, ZZ 20500")
        self.assertIsNone(address)

    def test_additional_discounts_with_never_cancel_and_new_property(self):
        self.assertEqual(len(additional_discounts(True, True)), 2)

    def test_additional_discounts_without_never_cancel_and_new_property(self):
        self.assertEqual(len(additional_discounts(False, False)), 0)

    def test_calculate_total_discount(self):
        discounts = additional_discounts(True, True)
        total_monthly_premium = 100

        self.assertEqual(len(discounts), 2)

        total_monthly_discount_from_func = calculate_total_discount(
            discounts=discounts, total_monthly_premium=total_monthly_premium
        )

        total_discount_percent = sum(discounts)
        total_monthly_discount_calc = round(
            total_monthly_premium * total_discount_percent, 2
        )

        self.assertEqual(total_monthly_discount_calc, total_monthly_discount_from_func)

    def test_calculate_total_fees_with_true_and_in_danger(self):
        fees = additional_fees(True, "CA")
        total_monthly_premium = 100

        self.assertEqual(len(fees), 2)

        total_monthly_discount_from_func = calculate_total_discount(
            discounts=fees, total_monthly_premium=total_monthly_premium
        )

        total_fee_percent = sum(fees)
        total_monthly_discount_calc = round(
            total_monthly_premium * total_fee_percent, 2
        )

        self.assertEqual(total_monthly_discount_calc, total_monthly_discount_from_func)

    def test_calculate_total_fees_with_false_and_in_danger(self):
        fees = additional_fees(False, "CA")
        total_monthly_premium = 100

        self.assertEqual(len(fees), 1)

        total_monthly_discount_from_func = calculate_total_discount(
            discounts=fees, total_monthly_premium=total_monthly_premium
        )

        total_fee_percent = sum(fees)
        total_monthly_discount_calc = round(
            total_monthly_premium * total_fee_percent, 2
        )

        self.assertEqual(total_monthly_discount_calc, total_monthly_discount_from_func)

    def test_calculate_total_fees_with_false_and_not_in_danger(self):
        fees = additional_fees(False, "NJ")
        total_monthly_premium = 100

        self.assertEqual(len(fees), 0)

        total_monthly_discount_from_func = calculate_total_discount(
            discounts=fees, total_monthly_premium=total_monthly_premium
        )

        total_fee_percent = sum(fees)
        total_monthly_discount_calc = round(
            total_monthly_premium * total_fee_percent, 2
        )

        self.assertEqual(total_monthly_discount_calc, total_monthly_discount_from_func)


class PolicyCheckoutTestCases(APITestCase):
    def setUp(self) -> None:
        self.credentials = {"username": "takumi", "password": "TruenoAE86"}

        self.user = User.objects.create_user(**self.credentials)
        self.token, _ = Token.objects.get_or_create(user=self.user)
        self.client.force_authenticate(user=self.user, token=self.token)
        self.checkout_url = "http://0.0.0.0:8000/api/checkout/"
        self.quotes_url = "http://0.0.0.0:8000/api/quotes/"

    def test_checkout_functions(self):
        self.quote = create_quote(
            had_previously_cancel_volcano_policy=False,
            never_cancel_volcano_policy=False,
            new_property=False,
        )

        self.assertIsInstance(self.quote, Quote)

        policy = checkout(self.quote.quote_number)

        self.assertIsInstance(policy, Policy)

    def test_checkout_api(self):
        quote_data = {
            "policy_holder": "Frank Underwood",
            "had_previously_cancel_volcano_policy": True,
            "never_cancel_volcano_policy": True,
            "new_property": True,
            "address": "1600 Pennsylvania Avenue NW, Washington, DC 20500",
        }
        quote_response = self.client.post(self.quotes_url, quote_data, format="json")

        self.assertEqual(
            quote_response.status_code, status.HTTP_201_CREATED, msg=quote_response.data
        )

        checkout_response = self.client.post(
            self.checkout_url,
            {"quote_number": quote_response.data["quote_number"]},
            format="json",
        )
        self.assertEqual(
            checkout_response.status_code,
            status.HTTP_201_CREATED,
            msg=checkout_response.data,
        )
