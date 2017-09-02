import os
import sys
import requests
import pathlib
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

def main():
  usage = "Usage: img_fetch.py url path"
  if not len(sys.argv) == 3:
    print(usage)
    sys.exit(1)
  url = sys.argv[1]
  path = sys.argv[2]
  parsed = urlparse(url, "http")
  if not parsed.netloc:
    print("Please preface the address with 'http://'")
    sys.exit(1)
  print("Working on it...")
  scraped_srcs = scrape_img(url)
  normalized_urls = normalize_src(url, scraped_srcs)
  save_links(normalized_urls, os.path.join(path, "img-links.txt"))
  save_img(normalized_urls, path)
  print("Finished!")

def scrape_img(url):
  """List of img's links found at the url."""
  html_str = requests.get(url).text
  soup = BeautifulSoup(html_str, "html.parser")
  img_tags = soup.find_all("img")
  img_srcs = []
  for tag in img_tags:
    img_srcs.append(tag["src"])
  print("Saving " + str(len(img_srcs)) + " images...")
  return img_srcs

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

def save_links(img_srcs, file_path):
  """"Writes images' adresses in path."""
  with open(file_path, "w") as new_file:
    new_file.write('\n'.join(img_srcs))

def save_img(srcs, dir_path):
  """Downloads images into dir_path."""
  count = 0
  for src in srcs:
    r = requests.get(src)
    try:
      img = Image.open(BytesIO(r.content))
      name = "img" + str(count) + pathlib.Path(src).suffix
      img.save(os.path.join(dir_path, name))
      img.close()
    except:
      print("Invalid image format (" + src + ")")
      continue
    count += 1

if __name__ == "__main__":
  main()
