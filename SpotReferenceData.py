import logging
import os.path
import json
import unittest
from Spot import Spot


logging.config.fileConfig('cfg/logger.conf')
logger = logging.getLogger()


class SpotReferenceData:
    resources_path = "resources/spots/"
    spots_list = None
    spots_json = None

    spots_dict = {}

    def __init__(self):
        pass

    def load_reference_file(self, filename):
        logger.info("Loading spot reference data from file: %s" % filename)
        #TODO Use try with exception for wrong filename
        spots_file_path = self.resources_path + filename
        spots_file = self.read_file(spots_file_path)
        self.spots_json = self.load_json(spots_file)
        self.spots_dict[filename[:-11]] = self.spots_json

    @staticmethod
    def read_file(spots_file_path):
        """Takes string input as filename. Returns content of file."""
        if os.path.isfile(spots_file_path):
            with open(spots_file_path, 'rb') as f:
                content = f.read()
            return content
        else:
            logger.error("No spots file found with name %s" % spots_file_path)

    @staticmethod
    def load_json(spots_file):
        logger.debug("Loading json object ")
        try:
            return json.loads(spots_file)
        except ValueError:
            logger.error("Failed to load JSON data. Value Error")


    def get_spots(self, country="france"):
        #self.load_reference_file(france)
        return [Spot(spot_json) for spot_json in self.spots_json]

    def get_spots_by_region(self, country=None):
        if country in self.spots_dict.keys():
            return [Spot(spot_json) for spot_json in self.spots_dict[country]]
        else:
            logger.warning("Country not loaded in Spot Reference Data")
            return None

    def get_spot_keys(self):
        return self.spots_dict.keys()










class Test(unittest.TestCase):
    def test_load_reference_file(self):
        print("Testing load file function")
        x = SpotReferenceData()
        x.load_reference_file("japan_spots.json")
        #self.fail()

    def test_load_json(self):
        print("Testing load json function")
        a_json_string = {"_id": 606,
                         "name": "Aha Point",
                         "description": "",
                         "lat": 26.7396, "lon": 128.321,
                         "url": "/Aha-Point-Surf-Report/606/",
                         "hasNetcam": "false",
                         "region": {"_id": 61 },
                         "country": {"iso": "jp"}
                         }
        a_json = json.dumps(a_json_string)
        x = SpotReferenceData.load_json(a_json)
        self.assertEqual(x['_id'], 606)
        self.assertEqual(x['name'], 'Aha Point')

    def test_get_spots_by_region(self):
        x = SpotReferenceData()
        x.spots_dict["myCountry"] = "MOCK_SPOT_OBJECT"
        res = x.get_spots_by_region("that_country")
        self.assertEqual(res, None)

        pass



if __name__ == '__main__':
    unittest.main()