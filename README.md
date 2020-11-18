# CyberDrop Scraper
Download images and videos from CyberDrop albums

Scraped files will retain their *original* filenames and exclude the name extension that CyberDrop slaps on the end of each file.


![preview](images/preview.png)


# Installation

While in the project folder, go to your command line and run:

`pip install -r requirements.txt`

or, if you're on macOS/Linux:

`pip3 install -r requirements.txt`

# Usage

While in the project folder, start the scraper by running the following in the command line:

`python cyberdrop.py`

or

`python3 cyberdrop.py`

The script will then ask you for a CyberDrop album link. Enter one after the `>>>` and then hit 'ENTER'.

# Options

The following options are accessible in the `config.json` file:

`User-Agent`

You can change the default user agent if you wish.

`destination`

You can specify a destination folder for downloaded content. If you don't specify one, CyberDrop albums will be saved in the current working directory.

`organize_files`

Set to `true` by default. If you set this to `false`, downloaded content won't be organized into subdirectories (e.g., "Images", "Videos", etc.)
