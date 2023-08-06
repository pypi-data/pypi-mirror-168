from django.db import models

from mojec_core.app.models import BaseModelAbstract


class Bedroom(BaseModelAbstract, models.Model):
    name = models.CharField(max_length=255, blank=False, null=False,
                            unique=True)
    unit_price = models.DecimalField(max_digits=15, decimal_places=2,
                                     default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'Bedrooms'
