"""
Template for extracting image links on yahoo
"""
from image_mint import SearchEngine
from selenium.webdriver.common.by import By
from urllib.parse import quote


class Yahoo(SearchEngine):
    def __init__(self, *args):
        super().__init__(*args)
        self.img_class_ref = 'tile--rg_i'
        self.has_next_result_btn = True
        self.must_type_search = False

    def _get_search_url(self, search):
        search = quote(search.encode('utf-8'))
        return f"https://ca.images.search.yahoo.com/search/images?p={search}"

    def _get_next_btn(self):
        return self.driver.find_element(By.XPATH, "//button[@value='more-res']")


