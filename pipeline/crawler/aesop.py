from typing import List, Dict, Generator
import pymongo
from tqdm import tqdm

from .spider import Spider

from bs4 import BeautifulSoup
import requests
import time

class AesopSpider(Spider):
    def __init__(self, links: List[str]):
        super().__init__()
        self.links = links

    def crawl(self, collection: pymongo.collection) -> int:
        """
        Crawl logic for spider
        """
        for idx, link in enumerate(tqdm(self.links)):
            response = requests.get(link)
            
            story = self._parse(response.content)

            story['link'] = link
            
            collection.insert_one(story)
                
            print('\nSleep 3 seconds')
            time.sleep(3)

            if idx % 10 == 9:
                print('\nSleep 10 seconds')
                time.sleep(10)

        return 0

    def _parse(self, content: bytes) -> Dict:
        """
        Parse logic for crawled text
        """
        soup = BeautifulSoup(content, 'html.parser')
        story_text = [p.text for p in soup.select('p')]
        quote_text = [quote.text for quote in soup.select('blockquote')]

        story = {
            'html': content,
            'story': story_text,
            'quote': quote_text
        }

        return story

def get_aesop_links(base_url: str) -> List[str]:
    """
    Returns a generator for links to all stories
    """
    response = requests.get(base_url + '001.html')

    soup = BeautifulSoup(response.content, 'html.parser')
    stories_link = soup.select('ul.toc>li>a')

    return [base_url + a['href'] for a in stories_link]