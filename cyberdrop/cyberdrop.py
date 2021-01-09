import os
import sys
import json
import concurrent.futures
import re
import argparse
import threading
import time

import requests
from bs4 import BeautifulSoup

from cyberdrop.constants import HEADERS, CHARACTERS


class CyberDrop:
    def __init__(self, args, path=os.getcwd(), length=None, album_dir=None):
        self.url = args.url
        self.path = path
        self.length = length
        self.album_dir = album_dir

    def scrape_album(self):
        with requests.Session() as s:
            r = s.get(self.url, headers=HEADERS)
        soup = BeautifulSoup(r.content, 'lxml')
        containers = soup.findAll('a', {'class': 'image'})
        file_urls = [container['href'] for container in containers]
        if not file_urls:
            print('Found 0 files')
            return None
        filenames = [container['title'] for container in containers]
        timestamps = [int(container['data-timestamp'])
                      for container in containers]
        tuples = zip(file_urls, filenames, timestamps)
        album_name = self.clean_text(soup.find('h1', {'id': 'title'})['title'])
        self.album_dir = os.path.join(self.path, album_name)
        self.length = len(file_urls)
        os.makedirs(self.album_dir, exist_ok=True)
        return tuples

    def prepare_download(self, tuples):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(self.download, tupl): tupl for tupl in tuples
            }
            for future in concurrent.futures.as_completed(futures):
                future.result

    def download(self, tupl):
        url, filename, timestamp = tupl[0], tupl[1], tupl[2]
        with requests.Session() as s:
            r = s.get(url, headers=HEADERS)
        path = os.path.join(self.album_dir, filename)
        with open(path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                f.write(chunk)
        os.utime(path, (timestamp, timestamp))

    @staticmethod
    def clean_text(string):
        pattern = re.compile(r'[.:/\\]')
        new_string = pattern.sub('_', string)
        return new_string

    @staticmethod
    def spinner(event):
        while True:
            for character in CHARACTERS:
                if event.is_set():
                    return None
                print(f' {character}', end='\r', flush=True)
                time.sleep(0.5)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='a URL to scrape', type=str)
    args = parser.parse_args()
    e1 = threading.Event()
    t1 = threading.Thread(target=CyberDrop.spinner, args=(e1,))
    t1.start()
    cyberdrop = CyberDrop(args)
    tuples = cyberdrop.scrape_album()
    cyberdrop.prepare_download(tuples)
    e1.set()


if __name__ == '__main__':
    main()
