import logging.config
import gspread

from rentepoint import Spots, DataEngine, spread


def main_download():
    """Main function to download new forecast data from MSW."""
    spread_name = "RentepointDB"

    logger.info("Running it the slick way")

    ids = Spots().get_ids()

    logger.info("Slicing list in even size chunks of 100ds")
    chunks = [ids[i:i + 100] for i in xrange(0, len(ids), 100)]

    for chunk in chunks[0:1]:
        res = DataEngine().get_update_data(chunk)
        #TODO: Better solution for this !!
        break
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


if __name__ == '__main__':
    logging.config.fileConfig('cfg/logger.conf')
    logger = logging.getLogger()

    #pandas_load_example()
    main_download()


