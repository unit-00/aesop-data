import unittest
import requests
from pymongo import MongoClient
from pipeline.crawler.aesop import get_aesop_links, AesopSpider

class TestAesopSpider(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_url = 'http://read.gov/aesop/'
        cls.links = get_aesop_links(cls.base_url)[:2]
        cls.test_spider = AesopSpider(cls.links)

        cls.test_db = 'test_db'
        cls.test_coll = 'test_coll'

        cls.client = MongoClient('localhost', 27017)
        cls.coll = cls.client[cls.test_db][cls.test_coll]

    def test_get_links(self):
        self.assertTrue(len(self.links) == 2)

    def test_parse(self):
        test_story = self.links[0]
        response = requests.get(test_story)
        self.assertTrue(type(self.test_spider._parse(response.content)) is dict)

    def test_crawl(self):
        self.test_spider.crawl(self.coll)
        self.assertEqual(self.coll.count_documents({}), 2)

    @classmethod
    def tearDownClass(cls):
        cls.client.drop_database(cls.test_db)

if __name__ == '__main__':
    unittest.main()