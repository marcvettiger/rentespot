from unittest import TestCase
import rentepoint
import pandas


class TestSpots(TestCase):

    AMOUNT_OF_ALL_SPOTS = 3620

    def test_Spots_object_loads_3620_elements_in_dict(self):
        s = rentepoint.Spots()
        self.assertEqual(len(s.dict), self.AMOUNT_OF_ALL_SPOTS)
        self.assertEqual(s.dict[1]['name'], "Newquay - Fistral North")

    def test_get_ids(self):
        s = rentepoint.Spots()
        ids = s.get_ids()
        self.assertIs(type(ids), list)

    def test_get_pandaDF_without_args(self):
        s = rentepoint.Spots()
        df = s.get_pandaDF()
        self.assertIs(type(df), pandas.DataFrame)
        self.assertEqual(len(df.index), self.AMOUNT_OF_ALL_SPOTS)

    def test_get_urls_without_arg(self):
        s = rentepoint.Spots()
        urls = s.get_urls()
        self.assertIs(type(urls), dict)
        self.assertEqual(len(urls), self.AMOUNT_OF_ALL_SPOTS)



class TestDataEngine(TestCase):

    def test_DataEngine_object_init(self):
        e = rentepoint.DataEngine()
        self.assertIs(type(e), rentepoint.DataEngine)
        self.assertIs(type(e.url_dict), dict)
        self.assertIsNotNone(e.url_dict)

    def test_get_update_data(self):
        self.fail("Not yet implemented")

    def test_scrape_jsons(self):
        self.fail("Not yet implemented")

    def test_get_ratings(self):
        self.fail("Not yet implemented")
