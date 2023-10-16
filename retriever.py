from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import re
import sys
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s.%(msecs)03d] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)


class Retriever:

    def __init__(self, url=None):
        self.url = url

    def set_url(self, url):
        """
        Set the URL where the price data should be retrieved from. Start a query at https://www.flychina.com/, and
        copy the URL after hitting search.

        :param url: str.
        """
        self.url = url

    def retrieve_prices(self):
        """
        Get the prices of the recommended and cheapest tickets.

        :return: dict.
        """
        price_dict = {'recommended': 0, 'cheapest': 0}
        chrome_options = Options()
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--headless")

        logging.info('Fetching from webpage...')
        try:
            driver = webdriver.Chrome(executable_path=os.path.join(os.path.dirname(__file__), 'bin', 'chromedriver.exe'),
                                      options=chrome_options)
        except:
            driver = webdriver.Chrome(executable_path=os.path.join(os.path.dirname(__file__), 'bin', 'chromedriver'),
                                      options=chrome_options)

        driver.implicitly_wait(20)
        driver.get(self.url)

        g = driver.find_elements_by_class_name("priceC2")
        for i, tag in zip(range(max(len(g), 2)), ['recommended', 'cheapest']):
            price_dict[tag] = self.price_text_to_float(g[i].text)
        if price_dict['cheapest'] == 0:
            price_dict['cheapest'] = price_dict['recommended']

        logging.info('Recommended price: {}'.format(price_dict['recommended']))
        logging.info('Cheapest price: {}'.format(price_dict['cheapest']))
        return price_dict

    def price_text_to_float(self, price):
        return float(''.join(re.findall('\d+', price)))

