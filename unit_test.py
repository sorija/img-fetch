import requests
import unittest
from unittest import mock
import img_fetch

def mocked_requests(*args, **kwargs):
  class MockResponse:
    def __init__(self, path, status_code):
      mock_data = open(path, 'r')
      read_text = mock_data.read()
      mock_data.close()
      self.text = read_text
      self.status_code = status_code

  return MockResponse(args[0], 200)

class MyTestCase(unittest.TestCase):
  @mock.patch('requests.get', side_effect=mocked_requests)
  def test_scrape_img(self, mock_get):
    expected = ["foo bar", "first img", "second img"]
    actual = img_fetch.scrape_img("test/test-data/mock-page.html")
    self.assertEqual(expected, actual)

if __name__ == '__main__':
  unittest.main()
