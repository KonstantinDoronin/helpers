import re
import time
from datetime import datetime
from random import randint
from re import compile as recompile
from urllib.parse import quote

import pandas as pd
import requests
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
import csv

today = datetime.today().date()

# Launch Nominatim geo locator
geolocator = Nominatim(user_agent='')

# Define headers for requests.get
headers = {"'}


class TooManyRequests(Exception):
    """raises in fetch_page function if request redirected to https://www.avito.ru/blocked"""
    pass


def get_all_ads(query, sort_by='date', by_title=False, with_images=False, owner=None):
    """Yields dicts with ad info.

    Keyword arguments:
    query -- search query, like 'audi tt'
    sort_by -- method of sorting, 'date', 'price', 'price_desc' (price descending)
               default None (yields ads sorted by Avito algorithm)
    by_title -- if True yields only ads with query in title
                default False
    with_images -- if True yields only ads with query in title
                   default False
    owner -- if 'private' yields only private ads, if 'company' only company
             default None (yields all ads)
    """
    search_url = generate_search_url(query, sort_by, by_title, with_images, owner)
    for page, page_number in get_pages(search_url):
        for ad in get_ads_from_page(page):
            yield agregate_ad_info(ad, page_number)


def generate_search_url(query, sort_by, by_title, with_images, owner):
    """Generates url by search parameters
    raises ValueError if sort_by or owner argument is not correct
    """
    sort_values = {'date': '104', 'price': '1', 'price_desc': '2', None: '101'}
    owners = {'private': '1', 'company': '2', None: '0'}
    if sort_by not in sort_values:
        raise ValueError('Sorting by {} is not supported'.format(sort_by))
    if owner not in owners:
        raise ValueError('Owner can be only private or company')
    urlencoded_query = quote(query)
    base_url = 'https://www.avito.ru/kazan/kommercheskaya_nedvizhimost/sdam-ASgBAgICAUSwCNRW?s={}&bt={}&q={}&i={}&user={}'
    return base_url.format(sort_values[sort_by],
                            int(by_title),
                            urlencoded_query,
                            int(with_images),
                            owners[owner]) + '&p={}'


def agregate_ad_info(ad, page_number):
    title = get_title(ad)
    link = get_link(ad)
    price, price_per_sqm = get_price(ad)

    closest_metro = get_metro(ad)
    metro_distance = get_metro_distance(ad)
    metro_distance_km = clean_metro_distance(metro_distance)

    date = get_current_date()
    publication_date = get_date(ad)

    try:
        publication_date = convert_date(publication_date)
    except IndexError as e:
        print(e)

    address = get_address(ad)
    address = clean_address(address)
    latitude, longitude = geocoding(address)
    district = get_district(latitude, longitude)

    return title, date, link, price, publication_date, \
           address, closest_metro, metro_distance_km, page_number, \
           latitude, longitude, district, price_per_sqm
    # return title, date, link, price, publication_date, \
    #        closest_metro, metro_distance_km, page_number, \
    #        price_per_sqm

def get_pages(search_url):
    """Yields page html as string until it reaches page with nothing found"""
    page_number = 1
    page = fetch_page(search_url.format(page_number))
    while (page_exists(page)) & (page_number <= 100):
        print (page_number, end=', ')
        yield page, page_number
        page_number += 1
        page = fetch_page(search_url.format(page_number))


def get_ads_from_page(page):
    return get_beautiful_soup(page).find_all('div', attrs={'class': 'item_table-wrapper'})


def fetch_page(page_url):
    """Returns page html as string
    raises TooManyRequest if avito blocks IP
    """
    response = requests.get(page_url, headers=headers)  # define proxies if necessary

    if response.status_code == 429:
        raise TooManyRequests('IP temporarily blocked')
    time.sleep(randint(10, 18))
    return response.text

#to be continue