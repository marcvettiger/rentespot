import logging
import time
from SpotReferenceData import SpotReferenceData
from GSpreadEngine import GSpreadEngine

def rente_point():

    logging.info("Starting application")

    my_spot_list = ["france_spots.json",
                    "norway_spots.json",
                    "japan_spots.json",
                    ]

    my_collection = SpotReferenceData()

    # Fill all json files in spot reference data
    for ref_file in my_spot_list:
        my_collection.load_reference_file(ref_file)

    print("Loaded files: %s " % my_collection.get_spot_keys())

    my_spots = my_collection.get_spots_by_region('france')

    gsheet_data = []
    for spot in my_spots:
        try:
            spot.initialize()
            logging.info(spot.get_pretty_all())
            gsheet_data.append(spot.get_pretty_all())
        except Exception as e :
            logging.error("Exception in initializing spot: %s" % spot.get_pretty_all)
            logging.error("sleeping for 5 sec")
            time.sleep(5)


    # Write to Google spread sheet
    sheet_name = 'Rente Point DataBase'
    gspread_engine = GSpreadEngine()
    gspread_engine.write_range(sheet_name, gsheet_data)
    logging.info("Finished application")



if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(module)s - %(funcName)s(): %(message)s',
                        filename='log/main.log',
                        filemode='w')
    rente_point()
