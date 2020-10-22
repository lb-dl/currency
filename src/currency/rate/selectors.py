from django.core.cache import cache

from rate import choices
from rate.models import Rate


def get_latest_rates():

    rates = []
    for source_int, source_str in choices.SOURCE_CHOICES:
        for currency_int, _ in choices.CURRENCY_CHOICES:
            key = Rate.cache_key(currency_int, source_int)
            if key in cache:
                rate = cache.get(key)
            else:
                # slow part
                rate = Rate.objects \
                    .filter(source=source_int, currency=currency_int) \
                    .order_by('created') \
                    .last()
                if rate:
                    cache.set(key, rate, 20)
            # if rate is not None
            if rate:
                rates.append(rate)
    return rates
