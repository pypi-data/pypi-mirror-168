#!/usr/bin/env python
import requests


def download_file(url):
   local_filename = url.split('/')[-1]
   with requests.get(url, stream=True) as r:
       r.raise_for_status()
       with open(local_filename, 'wb') as f:
           for chunk in r.iter_content(chunk_size=8192):
               f.write(chunk)
   return local_filename


if __name__ == '__main__':
    url = "https://exiftool.org/exiftool-12.42.zip"
    zip_file = download_file(url)
    print("FUNKADE FINT!")


