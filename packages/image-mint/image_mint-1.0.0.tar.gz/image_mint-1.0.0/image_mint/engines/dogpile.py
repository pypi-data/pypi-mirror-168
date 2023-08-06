"""
Template for extracting image links on dogpile
"""
from image_mint import SearchEngine
from selenium.webdriver.common.by import By


class DogPile(SearchEngine):

    def __init__(self, *args):
        super().__init__(*args)
        self.img_class_ref = None
        self.has_next_result_btn = True
        self.must_type_search = True

    def _get_search_url(self, search):
        return "https://www.dogpile.com/?qc=images"

    def _get_next_btn(self):
        return self.driver.find_element(By.CLASS_NAME, "pagination__num--next")

    def _get_search_field(self):
        return self.driver.find_element(By.NAME, 'q')
