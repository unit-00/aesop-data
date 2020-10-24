from typing import Dict, Generator
import pymongo
from tqdm import tqdm

from .spider import Spider

from bs4 import BeautifulSoup
import requests
import time

class AesopSpider(Spider):
    def __init__(self, base_url):
        super().__init__()
        self.base_url = base_url

    def _get_all_stories_link() -> Generator[str, None, None]:
        """
        Returns a generator for links to all stories
        """
        response = requests.get(self.base_url + '001.html')

        soup = BeautifulSoup(response.content, 'html.parser')
        stories_link = soup.select('ul.toc>li>a')

        for a in stories_link:
            yield base_url + a['href']

    def crawl(collection: pymongo.collection) -> int:
        """
        Crawl logic for spider
        """
        stories_link = _get_all_stories_link()

        for idx, link in enumerate(tqdm(stories_link)):
            response = requests.get(link)
            
            story = _parse(response)
            
            collection.insert_one(story)
                
            print('\nSleep 3 seconds')
            time.sleep(3)

            if idx % 10 == 9:
                print('\nSleep 10 seconds')
                time.sleep(10)

        return 0

    def _parse(self, response: requests.models.Response) -> Dict:
        """
        Parse logic for crawled text
        """
        soup = BeautifulSoup(response.content, 'html.parser')
        story_text = [p.text for p in soup.select('p')]
        quote_text = [quote.text for quote in soup.select('blockquote')]

        story = {
            'link': link,
            'html': response.content,
            'story': story_text,
            'quote': quote_text
        }

        return story