import logging.config
import os.path
import json
import numpy
import requests
import bs4
import time
import pandas
import unittest




##
#
# Static Variables
#
##

PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCE_PATH = os.path.join(PACKAGE_DIR, 'src/')
LOGGER_CFG = os.path.join(PACKAGE_DIR, '../cfg/logger.conf')


logging.config.fileConfig(LOGGER_CFG)
logger = logging.getLogger()




SPOT_FILES = ['alaska_spots.json', 'antarctic_peninsula_spots.json', 'argentina_spots.json',
              'atlantic_states_spots.json', 'azores_spots.json', 'bali_lombok_spots.json', 'baltic_sea_spots.json',
              'bangladesh_spots.json', 'bermuda_spots.json', 'brazil_east_spots.json',
              'brazil_northeast_spots.json', 'brazil_south_spots.json', 'bulgaria_romania_spots.json',
              'california_central_spots.json','california_north_spots.json', 'california_south_spots.json',
              'canada_west_spots.json', 'canary_islands_spots.json', 'central_africa_spots.json',
              'central_america_north_spots.json', 'central_america_south_spots.json', 'central_caribbean_spots.json',
              'chile_north_spots.json', 'chile_south_spots.json', 'china_spots.json', 'colombia_spots.json',
              'cook_islands_spots.json', 'ecuador_spots.json', 'equatorial_guinea_spots.json',
              'fiji_samoa_tonga_spots.json', 'florida_spots.json', 'france_spots.json', 'french_polynesia_spots.json',
              'germany_denmark_spots.json', 'ghana_the_ivory_coast_spots.json', 'great_lakes_spots.json',
              'greece_spots.json', 'gulf_coast_spots.json', 'hawaii_spots.json', 'iran_spots.json', 'israel_spots.json',
              'italy_spots.json', 'japan_spots.json', 'java_spots.json', 'korea_spots.json', 'lebanon_spots.json',
              'leeward_islands_spots.json', 'maldives_spots.json', 'maluku_islands_spots.json',
              'mauritius_reunion_spots.json', 'mexico_baja_spots.json', 'mexico_pacific_spots.json',
              'micronesia_carolines_spots.json', 'morocco_spots.json', 'mozambique_madagascar_spots.json',
              'netherlands_belgium_spots.json', 'new_england_spots.json', 'new_guinea_spots.json',
              'new_jersey_new_york_spots.json', 'new_south_wales_spots.json', 'new_zealand_spots.json',
              'north_carolina_spots.json', 'north_west_australia_spots.json', 'norway_spots.json',
              'nova_scotia_spots.json', 'oman_spots.json', 'oregon_spots.json', 'persian_gulf_spots.json',
              'peru_north_spots.json', 'peru_south_spots.json', 'philippines_spots.json', 'queensland_spots.json',
              'russia_spots.json', 'seychelles_spots.json', 'south_africa_spots.json', 'south_australia_spots.json',
              'south_carolina_georgia_spots.json', 'south_east_asia_spots.json', 'south_west_australia_spots.json',
              'spain_portugal_spots.json', 'sri_lanka_spots.json', 'sumatra_mentawais_spots.json', 'sweden_spots.json',
              'taiwan_spots.json', 'tasmania_spots.json', 'turkey_spots.json', 'uk_ireland_spots.json',
              'uruguay_spots.json', 'venezuela_trindad_tobago_spots.json', 'victoria_spots.json',
              'washington_spots.json', 'west_africa_spots.json', 'western_sahara_spots.json',
              'windward_islands_spots.json',
              ]

MSW_URL = 'http://magicseaweed.com'

##
#
# Static functions used within the module
#
##


def read_file(file_path):
    """Takes string input as filename. Returns content of file."""
    logger.debug("Reading file %s", file_path)
    if os.path.isfile(file_path):
        with open(file_path, 'rb') as f:
            content = f.read()
        return content
    else:
        logger.error("Unable to read file %s" % file_path)


def load_json(spots_file):
    logger.debug("Loading json object ")
    try:
        return json.loads(spots_file)
    except ValueError:
        logger.error("Failed to load JSON data. Value Error")

##
#
# Classes to work with
#
##


class DataEngine(object):

    url_dict = {}

    def __init__(self):
        self.url_dict = Spots().get_urls()
        pass

    @staticmethod
    def get_pandaDF(data_set):
        """
        Requires a data_set list as stored in DB (Google Spreadsheet for now) and processes it to a pandas DataFrame
        :param data_set: Format [spot_id, day_date, rating]
        :return: pandas_df:
        """
        logger.info("Packing data in pandas DF")
        df = pandas.DataFrame(data_set, columns=['_id', 'date', 'rating'])
        df = df.pivot_table(values='rating', index='_id', columns='date', aggfunc='first')
        return df



    def get_update_data(self, id_list):
        """
        Main function to get data for updating spot forecasts. Will scrape json files from MSW and load ratings from it.
        The Function retrieves and process the data to format [ spot_id , day_date, rating ]
        :param id_list: A selection of spot ids to get update list from
        :return: data_set: as list containing all ratings in long format to pass on for storing/ etc..
        """
        urls = {i: self.url_dict[i] for i in id_list}
        jsons = self.scrape_jsons(urls)
        ratings = self.get_ratings(jsons)
        data_set = []
        for spot_id in ratings:
            for day, rating in ratings[spot_id].iteritems():
                data_set.append([spot_id, day, rating])
        return data_set

    @staticmethod
    def scrape_jsons(urls):
        """
        Function to scrape ratings. Expects a dict with {spot_id : spot_url}
        Returns a dict with {spot_id : json }
        """
        x = {}
        with requests.Session() as s:
            for id in urls:
                url = MSW_URL + urls[id]
                logger.info("Requesting for url: %s", url)
                try:
                    res = s.get(url, timeout=5).text
                    if res is None:
                        logger.error("Empty Response received for url: %s ", url)
                        continue

                except requests.exceptions.RequestException as e:  # Handles all requests exceptions
                    logger.error("Requests Exception for url: %s ", url)
                    logger.error("Error message: %s", e)
                    logger.error("Timeout 5 seconds")
                    time.sleep(5)
                    continue

                logger.debug("Parsing data as json")
                soup = bs4.BeautifulSoup(res, "html5lib")
                data_chart = soup.find('div', {"class": "msw-fcc"})["data-chartdata"]
                data_json = json.loads(data_chart)
                x[id] = data_json
        return x

    @staticmethod
    def get_ratings(jsons):
        """
        Function to get ratings from scraped JSON dict
        :param jsons: Expected dict with { id : json }
        :return: Dict with {id : { day : rating }
        """
        x = {}
        for id in jsons:
            # Read dates from json file
            dates = [date['anchor'] for date in jsons[id]['data'][0][::3]]
            logger.debug(dates)

            # Read ratings from json file
            ratings30 = [i['solidRating'] for i in jsons[id]['run']]
            ratings = [round(numpy.mean(ratings30[i:i+3]), 1) for i in range(0, len(ratings30), 3)]
            logger.debug(ratings)

            ratings_dict = dict(zip(dates, ratings))
            x[id] = ratings_dict

        return x










class Spots(object):
    """
    Class to handle all Spots. It loads all reference data on __init__ .
    All spots data is stored in a dict which is accessable
    Example:
        s = Spots()
        print s.dict[1]
    """
    dict = {}

    def __init__(self):
        self.__load()
        pass

    def __load(self):
        logger.info("Loading Spot object")
        for f in SPOT_FILES:
            j = read_file(RESOURCE_PATH+f)
            spot_group = load_json(j)
            for spot in spot_group:
                self.dict[spot['_id']] = spot

    def get_ids(self):
        """
        :return: A list of all unique spot ids
        """
        return [_id for _id in self.dict ]

    def get_pandaDF(self, ids=None, source=None):
        """
        Function to get panda data frame of Spots().
        :param ids: Pass ids for which to produce a panda DF. If not set, all will be returned.
        :param source: Select source from where to retrieve Forecast Data options as [ gspread_DB, msw, None ]
        :return: Panda data frame
        """
        df = pandas.DataFrame.from_dict(self.dict.values(), orient='columns')
        df = df.drop('description', 1)
        df = df.drop('hasNetcam', 1)
        df = df.drop('region', 1)

        return df

    def get_urls(self):
        """Returns a dictionary for all spots with { id : url }"""
        return {spot_id: spot['url'] for spot_id, spot in self.dict.iteritems()}


    # def get_ids_longitude_sorted(self):
    #     """
    #     Return a list of all spot ids sorted by longitude
    #     """
    #     x = {spot_id: spot['lon'] for spot_id, spot in self.dict.iteritems()}
    #     return sorted(x, key=x.get)






if __name__ == "__main__":
    pass





