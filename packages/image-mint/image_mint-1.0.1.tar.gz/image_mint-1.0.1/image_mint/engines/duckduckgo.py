"""
Template for extracting image links on duckduckgo
"""
from image_mint import SearchEngine
from urllib.parse import quote


class DuckDuckGo(SearchEngine):
    def __init__(self, *args):
        super().__init__(*args)
        self.img_class_ref = 'tile--img__img'
        self.has_next_result_btn = False

    def _get_search_url(self, search):
        search = quote(search.encode('utf-8'))
        return f"https://duckduckgo.com/?q={search}&t=ha&va=j&iax=images&ia=images"
