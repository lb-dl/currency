from django.db import models


# Create a model Rate here
class Rate(models.Model):
    CURRENCY_CHOICES = (
        (1, 'USD'),
        (2, 'EUR')
    )
    SOURCE_CHOICES = (
        (1, 'PrivatBank'),
        (2, 'Monobank'),
        (3, 'Minora'),
        (4, 'PUMB'),
        (5, 'KredoBank'),
    )
    source = models.PositiveSmallIntegerField(choices=SOURCE_CHOICES)
    currency = models.PositiveSmallIntegerField(choices=CURRENCY_CHOICES)
    buy = models.DecimalField(max_digits=6, decimal_places=2)
    sale = models.DecimalField(max_digits=6, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
