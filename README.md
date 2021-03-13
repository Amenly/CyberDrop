# CyberDrop Scraper
A command line tool written in Python for downloading images and videos from CyberDrop albums.

Scraped files will retain their *original* filenames and exclude the name extension that CyberDrop slaps on the end of each file.


# Installation

To install it, run the following in your terminal:

```sh
$ pip install cyberdrop
```

# Usage

To use this, all you have to do is get a URL to an album and type the following in your terminal:

```sh
$ cyberdrop url
```

Example:

```sh
$ cyberdrop https://cyberdrop.me/a/xxxxxxxx
```

All files will be stored in a folder with the same name as the album in the current working directory.
