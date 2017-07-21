import logging
import csv
import json
from Spot import Spot


## Write a Loader/Init/ Prepare SpotCollection class here
#################################################################################
def read_file(filename):
    """Takes string input as filename.
    Returns content of file."""
    with open(filename, 'rb') as f:
        content = f.read()
    return content


def load_json(filename):
    try:
        data = read_file(filename)
        jsondata = json.loads(data)
        return jsondata
    except:
        logging.error("Failed to load JSON data")


def load_spots(filename):
    #TODO: check if file exists

    logging.info("Loading Spots: %s" % filename)

    spots_file = "resources/"+filename
    logging.info("Load all spots from resource file")
    spots_json = load_json(spots_file)

    logging.info("Initializing all Spot objects in a List")
    loaded_spots = []
    for spot_json in spots_json:
        loaded_spots.append(Spot(spot_json))

    logging.info("Finished initializing France Spots -  returning List")
    return loaded_spots


def write_csv(csv_filename, spots):
    #TODO: Unicode Issue!
    with open("csv_results/"+csv_filename, 'w') as f:
        writer = csv.writer(f, delimiter=',')
        for spot in spots:
            writer.writerow(spot.get_all_pretty())

############################







def main():

    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', filename='log/main.log',filemode='w')

    logging.info("# Starting main ")

    # spots = load_spots("japan_spots.json")
    spots = load_spots("europe/azores_spots.json")

    for spot in spots[0:3]:
        spot.init_engine()
        spot.initialize()
        spot.set_ratings()
        for day in spot.get_pretty_all_long():
            print day
            # write this to csv

    # write_csv("20170720_japan_spots.csv", spots)

    logging.info("# Finished main.py")

if __name__ == '__main__':
    main()