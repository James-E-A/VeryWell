from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import get_current_timezone_name

from uuid import uuid4
try:
    from uuid import uuid6
except ImportError:
    from uuid6 import uuid6


class Policy(models.Model):
    id = models.CharField(db_index=True, max_length=50, verbose_name="ID")
    _rowid = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)

    published_at = models.DateTimeField(null=True, blank=True)
    retires_at = models.DateTimeField(null=True, blank=True)

    short_name = models.CharField(max_length=200)
    legal_html = models.TextField()

    class Meta:
        verbose_name_plural="policies"


class Contract(models.Model):
    id = models.UUIDField(db_index=True, default=uuid4, editable=False, verbose_name="ID")
    _rowid = models.BigAutoField(primary_key=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.RESTRICT)
    created_at = models.DateTimeField(auto_now_add=True)

    policy_set = models.ManyToManyField(Policy)

    effective_from = models.DateTimeField()
    effective_to = models.DateTimeField()

    client_acceptance = models.ForeignKey("Signature", on_delete=models.PROTECT, null=True, blank=True, editable=False, related_name="+")
    issuer_acceptance = models.ForeignKey("Signature", on_delete=models.PROTECT, null=True, blank=True, editable=False, related_name="+")

    is_endorsement_on = models.ForeignKey("self", on_delete=models.RESTRICT, null=True, blank=True, related_name="endorsement_set", limit_choices_to={'is_endorsement_on': None})


class Signature(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid6, verbose_name="ID")
    created_at = models.DateTimeField(auto_now_add=True)
    created_in_timezone = models.CharField(max_length=50, default=get_current_timezone_name)

    subject = models.CharField(max_length=150) # cached copy of meta.User.legal_name
    data_sha256 = models.BinaryField(max_length=32)
