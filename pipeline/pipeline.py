from typing import List, Generator

import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from tqdm import tqdm
import time

import argparse
# import pdb




def get_all_stories_link(base_url: str) -> Generator[str, None, None]:
    """
    Returns an iterator to 
    """
    response = requests.get(base_url + '001.html')

    soup = BeautifulSoup(response.content, 'html.parser')
    stories_link = soup.select('ul.toc>li>a')

    for a in stories_link:
        yield base_url + a['href']


def main():
    base_url = 'http://read.gov/aesop/'

    with MongoClient('localhost', 27017) as client:
        collections = client['story']['aesop']
        stories_link = get_all_stories_link(base_url)

        for idx, link in enumerate(tqdm(stories_link)):
            response = requests.get(link)
            soup = BeautifulSoup(response.content, 'html.parser')
            story_text = [p.text for p in soup.select('p')]
            quote_text = [quote.text for quote in soup.select('blockquote')]

            story = {
                'link': link,
                'html': response.content,
                'story': story_text,
                'quote': quote_text
            }
            
            collections.insert_one(story)

            print('\nSleep 3 seconds')
            time.sleep(3)

            if idx % 10 == 9:
                print('\nSleep 10 seconds')
                time.sleep(10)


if __name__ == '__main__':

    main()