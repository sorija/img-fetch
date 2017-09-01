#    Finds and fetches all images on a webpage and stores the images on disk
#    Writes a file on disk, which lists the URL’s of the images fetched
import requests
from bs4 import BeautifulSoup

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
