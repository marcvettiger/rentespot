import logging
import requests
import time
import numpy
from rentepoint import Spots

MSW_URL = 'http://magicseaweed.com'


# response headers elements
SERVER_NAME = "X-MSW-SERVER"
LENGTH = "Content-Length"
EXPIRES = "expires"


def load_engine():
    """Testing network and load for download function"""

    urls = Spots().get_urls()

    with requests.Session() as s:
        elapsed_time = []

        for id , url in urls.iteritems():
            url = MSW_URL + url
            logger.info("Loadtester get url: %s", url)
            try:
                res = s.get(url, timeout=5)
                if res is None:
                    logger.error("Empty Response received for url: %s ", url)
                    continue
            except requests.exceptions.RequestException as e:  # Handles all requests exceptions
                logger.error("Requests Exception for url: %s ", url)
                logger.error("Error message: %s", e)
                logger.error("Timeout 5 seconds")
                time.sleep(5)
                continue

            logger.info("Response metrics:")
            logger.info("Elapsed time: %s " % res.elapsed.total_seconds())
            elapsed_time.append(res.elapsed.total_seconds())
            logger.info("Average response time: %s" % numpy.mean(elapsed_time))
            logger.info("Max response time: %s " % numpy.max(elapsed_time))
            logger.info("Min response time: %s " % numpy.min(elapsed_time))

            logger.info("Length of response text: %s " % res.headers[LENGTH])
            logger.info("Server name: %s " % res.headers[SERVER_NAME])
            logger.info("Cookies: %s " % res.cookies)

        logger.info("Loadtesting of chunk done")


            #soup = bs4.BeautifulSoup(res, "html5lib")
            #data_chart = soup.find('div', {"class": "msw-fcc"})["data-chartdata"]
            #data_json = json.loads(data_chart)
            #x[id] = data_json

def run():
    logger.info("Starting load engine to measure")
    while True:
        load_engine()








if __name__ == '__main__':
    logging.config.fileConfig('cfg/logger.conf')
    logger = logging.getLogger()

    run()