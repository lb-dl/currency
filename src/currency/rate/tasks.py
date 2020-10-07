from decimal import Decimal

from bs4 import BeautifulSoup

from celery import shared_task

import requests

# from django.contrib.auth.models import User
# from django.utils.crypto import get_random_string


@shared_task
def parse_privatbank():
    from rate.models import Rate
    url = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5'
    response = requests.get(url)
    # rase an error if status is not 200
    response.raise_for_status()
    data = response.json()
    source = 1
    currency_map = {
        'USD': 1,
        'EUR': 2,
    }
    TWOPLACES = Decimal(10) ** -2
    for row in data:
        if row['ccy'] in currency_map:
            buy = Decimal(row['buy']).quantize(TWOPLACES)
            sale = Decimal(row['sale']).quantize(TWOPLACES)
            currency = currency_map[row['ccy']]
            last_rate = Rate.objects.filter(source=source, currency=currency).last()
            if last_rate is None or buy != last_rate.buy or sale != last_rate.sale:
                Rate.objects.create(
                    currency=currency,
                    source=source,
                    sale=sale,
                    buy=buy
                )


@shared_task
def parse_monobank():
    from rate.models import Rate
    url = 'https://api.monobank.ua/bank/currency'
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()[0:2]
    source = 2
    currency_map = {
        840: 1,
        978: 2,
    }
    TWOPLACES = Decimal(10) ** -2
    for row in data:
        if row['currencyCodeA'] in currency_map:
            buy = Decimal(row['rateBuy']).quantize(TWOPLACES)
            sale = Decimal(row['rateSell']).quantize(TWOPLACES)
            currency = currency_map[row['currencyCodeA']]
            last_rate = Rate.objects.filter(source=source, currency=currency).last()
            if last_rate is None or buy != last_rate.buy or sale != last_rate.sale:
                Rate.objects.create(
                    currency=currency,
                    source=source,
                    sale=sale,
                    buy=buy
                )


@shared_task
def parse_minora():
    from rate.models import Rate
    url = 'http://vkurse.dp.ua/course.json'
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    source = 3
    TWOPLACES = Decimal(10) ** -2
    for key in data:
        if key == 'Dollar':
            currency = 1
            buy = Decimal(data['Dollar']['buy']).quantize(TWOPLACES)
            sale = Decimal(data['Dollar']['sale']).quantize(TWOPLACES)
            last_rate = Rate.objects.filter(source=source, currency=currency).last()
            if last_rate is None or buy != last_rate.buy or sale != last_rate.sale:
                Rate.objects.create(
                    currency=currency,
                    source=source,
                    buy=buy,
                    sale=sale)
        if key == 'Euro':
            currency = 2
            buy = Decimal(data['Euro']['buy']).quantize(TWOPLACES)
            sale = Decimal(data['Euro']['sale']).quantize(TWOPLACES)
            last_rate = Rate.objects.filter(source=source, currency=currency).last()
            if last_rate is None or buy != last_rate.buy or sale != last_rate.sale:
                Rate.objects.create(
                    currency=currency,
                    source=source,
                    buy=buy,
                    sale=sale)


@shared_task
def parse_pumb():
    from rate.models import Rate
    url = 'https://retail.pumb.ua/'
    response = requests.get(url)
    response.raise_for_status()
    source = 4
    soup = BeautifulSoup(response.content, 'lxml')
    table = soup.find('table')
    buy_usd = table.find_all('tr')[1].find_all('td')[1].text
    sale_usd = table.find_all('tr')[1].find_all('td')[2].text
    buy_euro = table.find_all('tr')[2].find_all('td')[1].text
    sale_euro = table.find_all('tr')[2].find_all('td')[2].text
    usd = dict(ccy='USD', buy=buy_usd, sale=sale_usd)
    euro = dict(ccy='EUR', buy=buy_euro, sale=sale_euro)
    data = [usd, euro]
    currency_map = {
        'USD': 1,
        'EUR': 2,
    }
    TWOPLACES = Decimal(10) ** -2
    for row in data:
        if row['ccy'] in currency_map:
            buy = Decimal(row['buy']).quantize(TWOPLACES)
            sale = Decimal(row['sale']).quantize(TWOPLACES)
            currency = currency_map[row['ccy']]
            last_rate = Rate.objects.filter(source=source, currency=currency).last()
            if last_rate is None or buy != last_rate.buy or sale != last_rate.sale:
                Rate.objects.create(
                    currency=currency,
                    source=source,
                    sale=sale,
                    buy=buy
                )


@shared_task
def parse_kredobank():
    from rate.models import Rate
    url = 'https://kredobank.com.ua/info/kursy-valyut/commercial'
    response = requests.get(url)
    response.raise_for_status()
    source = 5
    soup = BeautifulSoup(response.content, 'lxml')
    table = soup.find('table')
    buy_usd = int(table.find_all('tr')[1].find_all('td')[3].text)/100
    sale_usd = int(table.find_all('tr')[1].find_all('td')[2].text)/100
    buy_euro = int(table.find_all('tr')[2].find_all('td')[3].text)/100
    sale_euro = int(table.find_all('tr')[2].find_all('td')[2].text)/100
    usd = dict(ccy='USD', buy=buy_usd, sale=sale_usd)
    euro = dict(ccy='EUR', buy=buy_euro, sale=sale_euro)
    data = [usd, euro]
    currency_map = {
        'USD': 1,
        'EUR': 2,
    }
    TWOPLACES = Decimal(10) ** -2
    for row in data:
        if row['ccy'] in currency_map:
            buy = Decimal(row['buy']).quantize(TWOPLACES)
            sale = Decimal(row['sale']).quantize(TWOPLACES)
            currency = currency_map[row['ccy']]
            last_rate = Rate.objects.filter(source=source, currency=currency).last()
            if last_rate is None or buy != last_rate.buy or sale != last_rate.sale:
                Rate.objects.create(
                    currency=currency,
                    source=source,
                    sale=sale,
                    buy=buy
                )
