import argparse
import json
from pymongo import MongoClient
from typing import List, Dict

from crawler.aesop import get_aesop_links, AesopSpider

def main(spider: str, database_config: Dict[str, str]) -> int:
    """Crawl for data"""

    host = database_config['host']
    port = database_config['port']
    database = database_config['database']
    collection = database_config['collection']

    with MongoClient(host, port, serverSelectionTimeoutMS=10000) as client:
        coll = client[database][collection]

        if spider == 'aesop':
            base_url = 'http://read.gov/aesop/'
            links = get_aesop_links(base_url)
            aesop_spider = AesopSpider(links)
            aesop_spider.crawl(coll)

    return 0

def _parse_args():
    """Parse commandline arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--spider", type=str, default="aesop", help="Spiders to use")
    parser.add_argument("--db_config", type=str, help="""
    Mongo Database info JSON:
    '{
        "host": "localhost", 
        "port": 27017, 
        "database": "story", 
        "collection": "test_coll"
    }'
    """, required=True
    )

    args = parser.parse_args()

    return args

if __name__ == '__main__':
    args = _parse_args()
    database_config = json.loads(args.db_config)
    main(args.spider, database_config)