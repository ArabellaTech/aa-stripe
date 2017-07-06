"""Test charging users through the StripeCharge model"""
import sys

import mock
import stripe
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.utils.six import StringIO
from stripe.error import StripeError

from aa_stripe.models import StripeCharge, StripeCustomer

UserModel = get_user_model()


class TestCharges(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create(email="foo@bar.bar", username="foo", password="dump-password")

    @mock.patch("aa_stripe.management.commands.charge_stripe.stripe.Charge.create")
    def test_charges(self, charge_create_mocked):
        data = {
            "customer_id": "cus_AlSWz1ZQw7qG2z",
            "currency": "usd",
            "amount": 100,
            "description": "ABC"
        }

        charge_create_mocked.return_value = stripe.Charge(id="AA1")
        StripeCustomer.objects.create(
            user=self.user, stripe_customer_id="bum", stripe_js_response="aa")

        StripeCustomer.objects.create(
            user=self.user, stripe_customer_id=data["customer_id"], stripe_js_response="foo")
        customer = StripeCustomer.objects.create(
            user=self.user, stripe_customer_id=data["customer_id"], stripe_js_response="foo")
        self.assertTrue(customer, StripeCustomer.get_latest_active_customer_for_user(self.user))

        charge = StripeCharge.objects.create(user=self.user, amount=data["amount"], customer=customer,
                                             description=data["description"])
        self.assertFalse(charge.is_charged)

        # test in case of an API error
        charge_create_mocked.side_effect = StripeError()
        with self.assertRaises(SystemExit):
            out = StringIO()
            sys.stdout = out
            call_command('charge_stripe')
            charge.refresh_from_db()
            self.assertFalse(charge.is_charged)
            self.assertIn('Exception happened', out.getvalue())

        charge_create_mocked.reset_mock()
        charge_create_mocked.side_effect = None

        # test regular case
        call_command("charge_stripe")
        charge.refresh_from_db()
        self.assertTrue(charge.is_charged)
        self.assertEqual(charge.stripe_response["id"], "AA1")
        charge_create_mocked.assert_called_with(amount=charge.amount, currency=data["currency"],
                                                customer=data["customer_id"], description=data["description"])
