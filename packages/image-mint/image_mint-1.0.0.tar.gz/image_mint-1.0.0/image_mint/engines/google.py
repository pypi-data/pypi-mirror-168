"""
Template for extracting image links on google
"""
from image_mint import SearchEngine
from selenium.webdriver.common.by import By
from urllib.parse import quote


class Google(SearchEngine):
    def __init__(self, *args):
        super().__init__(*args)
        self.img_class_ref = 'rg_i'
        self.has_next_result_btn = True
        self.must_type_search = False

    def _get_search_url(self, search):
        search = quote(search.encode('utf-8'))
        return f"https://www.google.com/search?q={search}&espv=2&biw=1366&bih=667&site=webhp&source=lnms&tbm=isch&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg"

    def _get_next_btn(self):
        return self.driver.find_element(By.XPATH, "//input[@value='Show more results']")

