from __future__ import division
from numpy import mean
import logging.config
import bs4
import requests
import json

logging.config.fileConfig('cfg/logger.conf')
logger = logging.getLogger()


class SpotDataEngine:
    # TODO: Check if return None or Null possible for no initialized object
    initialized = False

    base_url = "http://magicseaweed.com"
    data_json = None

    def __init__(self, url):
        self.url = self.base_url + url
        self.scrape_data()

    def scrape_data(self):
        logger.info("Scraping spot data for %s" % self.url)
        try:
            html_text = requests.get(self.url).text
            soup = bs4.BeautifulSoup(html_text, "html5lib")
            logger.debug("Parsing data as json")
            data_chart = soup.find('div', {"class": "msw-fcc"})["data-chartdata"]
            self.data_json = json.loads(data_chart)
            self.initialized = True
        except requests.exceptions.RequestException as e:
            logger.error("Request exception %s" % e)

    def get_ratings_all(self):
        if self.initialized is True:
            logger.debug("Getting all ratings from data JSON")
            ratings_all = []
            for i in self.data_json['run']:
                ratings_all.append(i['solidRating'])
            return ratings_all

    def get_ratings(self):
        if self.initialized is True:
            logger.debug("Getting average rating for each day for given ratings list")
            ratings_all = self.get_ratings_all()
            ratings_mean = []
            for i in range(0, len(ratings_all), 3):
                v = mean(ratings_all[i:i + 3])
                v = round(v, 1)
                ratings_mean.append(v)
            return ratings_mean

    def get_dates(self):
        if self.initialized is True:
            logger.debug("Getting all dates")
            dates_with_duplicates = [i["anchor"] for i in self.data_json['data'][0]]
            return dates_with_duplicates[::3]

