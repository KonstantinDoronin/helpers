import csv
# import random
import re
import time
from datetime import datetime

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions


def get_description(info):
    description = info.find('div',
                            attrs={'class': ['item-description-html', 'item-description-text']})
    return description.getText().strip() if description else None


def get_params(info):
    params = info.find('div', attrs={'class': 'item-params'})
    return params.getText().strip().replace('\xa0', '').replace('\n', '') if params else None


def get_office_area_param(string):
    try:
        area = re.search(r"(\d.*?)м²", string).group(1)
        area = float(area)
    except (TypeError, AttributeError):
        area = None
    return area


def get_views(info):
    views = info.find('div', attrs={'class': 'title-info-metadata-item title-info-metadata-views'}).getText()
    if "(" in views:
        views_total = re.compile("(.*?)\s*\(").match(views).group(1)
        views_total = float(views_total.replace(' ', ''))

        views_dynamics = re.compile(".*?\((.*?)\)").match(views).group(1)
        views_dynamics = float(views_dynamics.replace('+', ''))
    else:
        views_total = views
        views_total = float(views_total.replace(' ', ''))
        views_dynamics = None
    return views_total, views_dynamics


def get_class(string):
    try:
        class_ = re.search(r"(\w+)", string).group(1)
    except (AttributeError, TypeError):
        class_ = None
    return class_


def replace_list(text):
    for ch in []:
        text = text.replace(ch, '')
    return text


def get_office_area_title(title):
    rule = ''

    try:
        area = re.search(rule, title).group()
    except AttributeError:
        area = '0'
    area = replace_list(area)

    if re.findall('[а-яА-Я-/,]', area):
        area = 0
    else:
        area = float(area)
    return area


def unpack_param_office(parameters, title):
    area = get_office_area_param(parameters)
    class_ = get_class(parameters)

    area_title = get_office_area_title(title)

    return area, area_title, class_


#to be continued