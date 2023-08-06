import unittest
from image_mint import Scraper, SearchEngine


class MockSearch(SearchEngine):
    def __init__(self, path):
        pass

    def _get_image(self, keywords):
        yield SearchEngine.END_SIGNAL


class TestFeatures(unittest.TestCase):
    def test_download(self):
        scraper = Scraper(MockSearch('path'))
        scraper.download("test", "dir")


if __name__ == '__main__':
    unittest.main()
