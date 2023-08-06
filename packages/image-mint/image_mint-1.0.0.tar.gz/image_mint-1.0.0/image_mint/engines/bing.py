"""
Template for extracting image links on bing
"""
from image_mint import SearchEngine
from selenium.webdriver.common.by import By
from urllib.parse import quote


class Bing(SearchEngine):

    def __init__(self, *args):
        super().__init__(*args)
        self.img_class_ref = 'mimg'
        self.has_next_result_btn = True
        self.must_type_search = False

    def _get_search_url(self, search):
        search = quote(search.encode('utf-8'))
        return f"https://www.bing.com/images/search?q={search}&form=IRBPRS&first=1&tsc=ImageHoverTitle"

    def _get_next_btn(self):
        return self.driver.find_element(By.CLASS_NAME, "btn_seemore")


