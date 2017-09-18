import logging.config
import gspread
import schedule
import time
import threading

from rentepoint import Spots, DataEngine, spread


def download_allatones():
    """download function to download new forecast data from MSW."""
    logger.info("Starting download all at ones")

    spread_name = "RentepointDB"
    spread.clean_db(spread_name)

    ids = Spots().get_ids()

    chunk_size = 100
    logger.info("Slicing list in even size chunks of %s" % chunk_size)
    chunks = [ids[i:i + chunk_size] for i in xrange(0, len(ids), chunk_size)]
    logger.debug("Number of chunks: %s" % len(chunks))

    for chunk in chunks:
        res = DataEngine().get_update_data(chunk)

        try:
            spread.append(spread_name, res)
        except gspread.exceptions.RequestError as e:
            logger.error("Request Error in writing to Google Spread sheet:")
            logger.error("Timeout 5s and trying again")
            logger.error(e)
            spread.append(spread_name, res)

    logger.info("Finished application")


def pandas_load_example():
    # get data_set from gspread sheet

    s = Spots()
    spots_df = s.get_pandaDF()

    data_set = spread.get_data("RentepointDB")
    ratings_df = DataEngine.get_pandaDF(data_set)

    # merge them:
    spotsDF = spots_df.merge(ratings_df, on='_id')

    return spotsDF


def print_top20_rated_spots(spots_df):
    dates = spots_df.columns[7:].tolist()
    spots_df.sort_values(dates, ascending=False).head(20)


class DownloadThread(threading.Thread):
    def __init__(self, thread_id, chunk):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.chunk = chunk

    def run(self):
        logger.info("Starting Thread %s" % self.thread_id)
        res = DataEngine().get_update_data(self.chunk)
        logger.info("Exiting Thread %s" % self.thread_id)


def multithreaded_download():
    """Multithread function to download new forecast data from MSW."""
    spread_name = "RentepointDB"
    logger.info("Starting multi threaded download")

    ids = Spots().get_ids()

    chunk_size = 100
    logger.info("Slicing list in even size chunks of %s" % chunk_size)
    chunks = [ids[i:i + chunk_size] for i in xrange(0, len(ids), chunk_size)]
    logger.debug("Number of chunks: %s" % len(chunks))

    threads = []

    for i in range(0, len(chunks[:5])):
        thread = DownloadThread(i, chunks[i])
        thread.start()
        threads.append(thread)

    for t in threads:
        t.join()

    print "Exiting Main Thread"
    logger.info("Finished application")


def scheduled_runner():
    """Scheduled function to run download function for new forecast data from MSW each day at 3pm hours every day."""
    logger.info("Starting scheduled runner")
    moment = "19:15"
    logger.info("Downloading new data every day at %s" % moment)
    schedule.every().day.at(moment).do(download_allatones)
    schedule.every().hour.do(logger.info, "still alive...")

    while True:
        schedule.run_pending()
        time.sleep(60)





if __name__ == '__main__':
    logging.config.fileConfig('cfg/logger.conf')
    logger = logging.getLogger()
    #pandas_load_example()
    #main_download()
    #multithreaded_download()

    scheduled_runner()
