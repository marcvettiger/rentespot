import logging
import logging.config
import loggly.handlers
import time
from SpotReferenceData import SpotReferenceData
from GSpreadEngine import GSpreadEngine


def rente_point():

    logger.info('Starting application')

    my_spot_list = ["azores_spots.json",
                    "baltic_sea_spots.json",
                    "bulgaria_romania_spots.json",
                    "france_spots.json",
                    "germany_denmark_spots.json",
                    "greece_spots.json",
                    "italy_spots.json",
                    "netherlands_belgium_spots.json",
                    "norway_spots.json",
                    "russia_spots.json",
                    "spain_portugal_spots.json",
                    "sweden_spots.json",
                    "turkey_spots.json",
                    "uk_ireland_spots.json",

                    "japan_spots.json",
                    ]

    my_collection = SpotReferenceData()

    # Fill all json files in spot reference data
    for ref_file in my_spot_list:
        my_collection.load_reference_file(ref_file)

    europe_list = my_collection.get_spot_keys()
    europe_list.sort()
    logger.info("Loaded countries: %s " % europe_list)





    for country in europe_list[0:1]:
        logger.info("Downloading ratings for country: %s " % country)

        my_spots = my_collection.get_spots_by_region(country)

        gsheet_data = []
        for spot in my_spots:
            try:
                spot.initialize()
                logger.info(spot.get_pretty_all())
                gsheet_data.append(spot.get_pretty_all())
            except Exception as e :
                logger.error("Exception in initializing spot: %s" % spot.get_pretty_all)
                logger.error("sleeping for 5 sec")
                time.sleep(5)


        # Write to Google spread sheet
        # sheet_name = 'Rentepoint Spread'
        # gspread_engine = GSpreadEngine(sheet_name)
        # gspread_engine.create_sheet(country)
        # gspread_engine.write_range(sheet_name, country , gsheet_data)


    logger.info("Finished application")


if __name__ == '__main__':
    logging.config.fileConfig('cfg/logger.conf')
    logger = logging.getLogger()

    rente_point()


