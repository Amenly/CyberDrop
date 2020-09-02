import os
import sys
import json
import concurrent.futures

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def download_videos(url, title):
    r = s.get(url)
    if "/" in title:
        title.replace("/", "_")
    with open(os.path.join(album_name + "/Videos", title), "wb") as ww:
        for chunk in r.iter_content(chunk_size=50000000):
            ww.write(chunk)


def download_images(url, title):
    r = s.get(url)
    if "/" in title:
        title.replace("/", "_")
    with open(os.path.join(album_name + "/Images", title), "wb") as ww:
        for chunk in r.iter_content(chunk_size=50000000):
            ww.write(chunk)


def separator(urls, titles):
    comparison = [".mp4", ".mov", "m4a", ".m4v",
                  ".webm", ".flv", ".avi", ".wmv", ".qt"]
    video_urls = []
    video_titles = []
    image_urls = []
    image_titles = []
    for _ in urls:
        if any(x in _ for x in comparison):
            video_urls.append(_)
        else:
            image_urls.append(_)
    for _ in titles:
        if any(x in _ for x in comparison):
            video_titles.append(_)
        else:
            image_titles.append(_)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        if image_urls != []:
            print(f"Downloading {len(image_urls)} images...")
            os.mkdir(album_name + "/Images")
            list(tqdm(executor.map(download_images, image_urls,
                                   image_titles), total=len(image_urls)))
        if video_urls != []:
            print(f"Downloading {len(video_urls)} videos...")
            os.mkdir(album_name + "/Videos")
            list(tqdm(executor.map(download_videos, video_urls,
                                   video_titles), total=len(video_urls)))
        else:
            print("No items detected. Is the album empty?")


def start_session(url, header):
    global s
    with requests.Session() as s:
        r = s.get(url, headers=header)
        soup = BeautifulSoup(r.content, "lxml")
        containers = soup.findAll("a", {"class": "image"})
        content_urls = []
        titles = []
        for container in containers:
            content_urls.append(container["href"])
            titles.append(container["title"])
        global album_name
        album_name = soup.find("h1", {"id": "title"})["title"]
        if "/" in album_name:
            album_name.replace("/", "_")
        os.mkdir(album_name)
        print(f"Scraping '{album_name}'...")
        separator(content_urls, titles)


os.chdir(sys.path[0])

if __name__ == "__main__":
    url_input = input("Enter a CyberDrop album link below\n> ")
    with open("config.json", "r") as config:
        settings = json.load(config)["settings"]
    start_session(url_input, settings)
    print("Done")
