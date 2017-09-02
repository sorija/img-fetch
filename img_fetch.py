import os
import sys
import requests
import pathlib
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

def normalize_src(url, relative_srcs):
  """Normalizes relative imgs' urls."""
  normalized_srcs = []
  url_scheme = urlparse(url).scheme
  for src in relative_srcs:
    parsed = urlparse(src, url_scheme)
    if not parsed.netloc:
      normalized_srcs.append(urljoin(url, src))
    else:
      normalized_srcs.append(parsed.geturl())
  return normalized_srcs

def scrape_img(url):
  """List of img's links found at the url."""
  html_str = requests.get(url).text
  # find all the img and then value of associated src tag
  soup = BeautifulSoup(html_str, 'html.parser')
  img_tags = soup.find_all('img')
  img_srcs = []
  for tag in img_tags:
    img_srcs.append(tag['src'])
  return img_srcs

def save_links(img_srcs, file_path):
  """"Writes images' adresses in path."""
  with open(file_path, "w") as new_file:
    new_file.write('\n'.join(img_srcs))

def save_img(srcs, dir_path):
  """Downloads images into dir_path."""
  count = 0
  for src in srcs:
    r = requests.get(src)
    img = Image.open(BytesIO(r.content))
    name = "img" + str(count) + pathlib.Path(src).suffix
    img.save(os.path.join(dir_path, name))
    img.close()
    count += 1
