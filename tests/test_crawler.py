"""Tests for Aesop spider"""
import unittest  # pylint: disable=missing-module-docstring

from pymongo import MongoClient
import requests

from crawler.aesop import get_aesop_links, AesopSpider


class TestAesopSpider(unittest.TestCase):
    """Test cases for Aesop spider"""
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
        """Check if get_aesop_links return links"""
        self.assertTrue(len(self.links) == 2)

    def test_parse(self):
        """Check if parse method is parsing properly"""
        test_story = self.links[0]
        response = requests.get(test_story)
        self.assertTrue(isinstance(self.test_spider._parse(response.content),
                        dict))  # pylint: disable=protected-access

    def test_crawl(self):
        """Check if crawl is able to insert documents into mongo server"""
        self.test_spider.crawl(self.coll)
        self.assertEqual(self.coll.count_documents({}), 2)

    @classmethod
    def tearDownClass(cls):
        cls.client.drop_database(cls.test_db)


if __name__ == '__main__':
    unittest.main()
