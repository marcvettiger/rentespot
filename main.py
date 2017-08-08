import logging
import logging.config
import loggly.handlers
import time
from SpotReferenceData import SpotReferenceData
import spread
import csv
import spot
import gspread

# Todo: adapt for varaiable columns


def readCSV(csvFilename, colmns = 0):
    with open(csvFilename, 'rU') as f:
        reader = csv.reader(f, delimiter=' ', dialect=csv.excel_tab)
        spot_files = []
        for row in reader:
            spot_files.append(row)
    return spot_files


spot_files = ['alaska_spots.json', 'antarctic_peninsula_spots.json', 'argentina_spots.json',
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



def rente_point():


    logger.info('Starting application')


    my_collection = SpotReferenceData()

    # Fill all json files in spot reference data
    for ref_file in spot_files:
        my_collection.load_reference_file(ref_file)

    world = my_collection.get_spot_keys()
    world.sort()
    logger.info("Loaded countries: %s " % world)
    logger.info("Length: %s " % len(world))


    # Initializing google Spreadsheet:
    from datetime import date
    today = date.today().strftime('%Y%m%d')
    spread_name = today + "_Rentepoint"
    logger.info("Creating new Spreadsheet: %s " % spread_name)


    spread.new(spread_name)


    for country in world:
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

        # Google spread new approach
        spread.append(spread_name, gsheet_data)


    logger.info("Finished application")




def new_main():
    from spot import Spots, DataEngine
    spread_name = "RentepointDB"

    logger.info("Running it the slick way")

    ids = Spots().get_ids()

    logger.info("Slicing list in even size chunks of 100ds")
    chunks = [ids[i:i + 100] for i in xrange(0, len(ids), 100)]

    for chunk in chunks:
        res = DataEngine().get_update_data(chunk)
        #TODO: Better solution for this !!
        try:
            spread.append(spread_name, res)
        except gspread.exceptions.RequestError as e:
            logger.error("Request Error in writing to Google Spread sheet:")
            logger.error("Timeout 5s and trying again")
            logger.error(e)
            spread.append(spread_name, res)

    logger.info("Finished application")



def pandas_load_Example():

    # get data_set from gspread sheet

    s = spot.Spots()
    spots_df = s.get_pandaDF()

    data_set = spread.get_data_set_from_spreadDB("RentepointDB_static")

    ratings_df = spot.DataEngine.get_pandaDF(data_set)








if __name__ == '__main__':
    logging.config.fileConfig('cfg/logger.conf')
    logger = logging.getLogger()

    #rente_point()
    #new_Way()
    #new_main()
    pandas_load_Example()


