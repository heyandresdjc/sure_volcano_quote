from array import array
import uuid
from django.db import models
from django.shortcuts import reverse
from validators import zip_code_validator
from django.utils.translation import gettext as _


class BaseModel(models.Model):

    id = models.UUIDField(_("id"), primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = "-updated_at"

    def __str__(self):
        return (
            f"id: {self.id} created: {self.created_at} last changed: {self.updated_at}"
        )

    def get_absolute_url(self):
        return reverse(f"{self.__class__.__name__}_detail", kwargs={"pk": self.pk})


class Address(BaseModel):

    address = models.CharField(_("Address"), max_length=150)
    state = models.CharField(_("state"), max_length=50)
    zip_code = models.CharField(
        _("Zip Code"), max_length=10, validators=[zip_code_validator]
    )

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Address_detail", kwargs={"pk": self.pk})


class Policy(models.Model):

    policy_number = models.CharField(_("Policy Number"), max_length=50)
    is_active = models.BooleanField(_("Active"), default=True)
    is_cancel = models.BooleanField(_("Cancel"), default=False)
    address = models.CharField(_("Address"), max_length=150)

    class Meta:
        verbose_name = _("Policy")
        verbose_name_plural = _("Policys")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Policy_detail", kwargs={"pk": self.pk})


class Quote(BaseModel):
    """
    Description:
    ● Quote number
        ○ A 10 digit mix of random letters and numbers used to uniquely identify
        the quote. This is generated on the API side, not through API request data.
    ● Effective date
        ○ The date coverage will begin if a policy is purchased.
    ● Previous policy canceled
        ○ Indicates if the customer has ever had a volcano insurance policy that has been canceled.
    ● Owns property to be insured
        ○ Indicates if the customer owns the property to be insured.
    ● Property address
        ○ zipcode of the property to be insured.
        ○ A valid US state

    Returns:
        _type_: Query Model Object
    """

    quoute_number = models.CharField(_("Quote Number"), max_length=10, unique=True)
    effective_date = models.DateTimeField(
        _("Effective Date"), auto_now=False, auto_now_add=False
    )
    previously_cancel_policy = models.ForeignKey(
        "Policy",
        verbose_name=_("Previously Cancel Policy"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    total_term_premium = models.DecimalField(
        _("Total Term Premium"), max_digits=6, decimal_places=2
    )
    total_monthly_premium = models.DecimalField(
        _("Monthly Term Premium"), max_digits=6, decimal_places=2
    )

    total_additionl_fee = models.DecimalField(
        _("Total Additonal Fee"), max_digits=6, decimal_places=2
    )
    total_monthly_fee = models.DecimalField(
        _("Total Additonal Fee"), max_digits=6, decimal_places=2
    )

    total_discount = models.DecimalField(
        _("Total Discount"), max_digits=6, decimal_places=2
    )
    total_monthly_discount = models.DecimalField(
        _("Total Discount Monthly Fee"), max_digits=6, decimal_places=2
    )

    class Meta:
        verbose_name = _("Quote")
        verbose_name_plural = _("Quotes")
        indexes = [
            models.Index(fields=["quoute_number"]),
            models.Index(
                fields=[
                    "quoute_number",
                    "effective_date",
                ]
            ),
            models.Index(
                fields=[
                    "quoute_number",
                    "is_active",
                ]
            ),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Quote_detail", kwargs={"pk": self.pk})
