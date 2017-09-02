import os
import requests
import unittest
from unittest import mock
from pathlib import Path
import img_fetch

def mocked_requests(*args, **kwargs):
  class MockResponse:
    def __init__(self, path, status_code):
      mock_data = open(path, "r")
      read_text = mock_data.read()
      mock_data.close()
      self.text = read_text
      self.status_code = status_code

  return MockResponse(args[0], 200)

class MyTestCase(unittest.TestCase):

  def test_normalize_src(self):
    srcs = ["http://images.net/kitty.jpg", "//i.images.net/kitty.jpg", "kitty.jpg"]
    expected = ["http://images.net/kitty.jpg", "http://i.images.net/kitty.jpg", "http://images.net/kitty.jpg"]
    actual = img_fetch.normalize_src("http://images.net", srcs)
    self.assertEqual(expected, actual)

  @mock.patch("requests.get", side_effect=mocked_requests)
  def test_scrape_img(self, mock_get):
    expected = ["foo", "bar", "spam"]
    actual = img_fetch.scrape_img("test-data/mock-page.html")
    self.assertEqual(expected, actual)

  def test_save_links(self):
    text = ["Lorem Ipsum", "cupcake ipsum", "kitty ipsum"]
    file_path = "test-data/my_file.txt"
    expected_file = Path(file_path)
    img_fetch.save_links(text, file_path)
    self.assertTrue(expected_file.exists())
    if expected_file.exists():
      with open(file_path, "r") as f:
        self.assertEqual(f.read(), '\n'.join(text))
      os.remove(file_path)

if __name__ == "__main__":
  unittest.main()
