#    Finds and fetches all images on a webpage and stores the images on disk
#    Writes a file on disk, which lists the URL’s of the images fetched
import requests

def scrape_img(url):
  """List of img's links found at the url."""
  contents = requests.get(url).text
  return []
