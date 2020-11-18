import os
import sys
import json
import concurrent.futures
import re
import glob
import shutil

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def scrape_url(url):
    with requests.Session() as s:
        r = s.get(url, headers=headers)
    soup = BeautifulSoup(r.content, "lxml")
    containers = soup.findAll("a", {"class": "image"})
    file_urls = [container["href"] for container in containers]
    if not file_urls:
        return None
    file_names = [container["title"] for container in containers]
    timestamps = [int(container["data-timestamp"]) for container in containers]
    combination = zip(file_urls, file_names, timestamps)
    length = len(file_urls)
    album_name = soup.find("h1", {"id": "title"})["title"]
    album_name = text_replacement(album_name)
    album_dir = directory + "/" + album_name
    if os.path.isdir(album_dir):
        pass
    else:
        os.mkdir(album_dir)
    print(f"Scraping '{album_name}' with {length} files")
    return combination, album_dir, length


def text_replacement(string):
    pattern = re.compile(r'[.:/\\]')
    new_string = pattern.sub("_", string)
    return new_string


def download_manager(tuples, length):
    with tqdm(total=length, desc="Downloading...") as bar:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {executor.submit(download, tup): tup for tup in tuples}
            for future in concurrent.futures.as_completed(futures):
                future.result
                bar.update(1)


def download(tup):
    with requests.Session() as s:
        r = s.get(tup[0], headers=headers)
    path = os.path.join(album_dir, tup[1])
    with open(path, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024):
            f.write(chunk)
    time = (tup[2], tup[2])
    os.utime(path, time)


def separator():
    files_list = glob.glob(album_dir + "/*")
    video_pattern = re.compile(fr'.+\.({video_extensions})', re.I)
    video_matches = [re.finditer(video_pattern, file) for file in files_list]
    video_files = [file.group() for match in video_matches for file in match]
    if video_files:
        videos_dir = os.path.join(album_dir, "Videos")
        if not os.path.isdir(videos_dir):
            os.mkdir(videos_dir)
        for file in video_files:
            shutil.move(file, videos_dir)
    image_pattern = re.compile(fr'.+\.({image_extensions})', re.I)
    image_matches = [re.finditer(image_pattern, file) for file in files_list]
    image_files = [file.group() for match in image_matches for file in match]
    if image_files:
        images_dir = os.path.join(album_dir, "Images")
        if not os.path.isdir(images_dir):
            os.mkdir(images_dir)
        for file in image_files:
            shutil.move(file, images_dir)
    gif_pattern = re.compile(fr'.+\.({gif_extensions})', re.I)
    gif_matches = [re.finditer(gif_pattern, file) for file in files_list]
    gif_files = [file.group() for match in gif_matches for file in match]
    if gif_files:
        gifs_dir = os.path.join(album_dir, "GIFs")
        if not os.path.isdir(gifs_dir):
            os.mkdir(gifs_dir)
        for file in gif_files:
            shutil.move(file, gifs_dir)


if __name__ == "__main__":
    config_file = sys.path[0] + "/config.json"
    with open(config_file, "r") as f:
        config = json.load(f)["config"]
        headers = config["headers"]
        settings = config["settings"]
    if not (directory := settings["destination"]):
        directory = os.getcwd()
    if organize_files := settings["organize_files"]:
        video_extensions = settings["video_extensions"]
        image_extensions = settings["image_extensions"]
        gif_extensions = settings["gif_extensions"]
    url = input("Enter a CyberDrop album link below\n>>> ")
    combination, album_dir, length = scrape_url(url)
    if not combination:
        print("There are no files in that album")
    else:
        download_manager(combination, length)
        if organize_files:
            separator()
        print("Program successfully quit")
