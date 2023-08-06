"""
Package for searching for images and downloading them
"""
import os
import base64
import requests
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from urllib.parse import quote
import time
import logging
logging.basicConfig(level='INFO')
logger = logging.getLogger(__name__).setLevel(logging.WARNING)


def __is_img_size_good(image_path, min_width, min_height):
    """
    :param image_path: string, path must exist
    :param min_width: int or None
    :param min_height: int or None
    :return: boolean, True if there are no minimum size requirements of if size requirements are satisfied
    """
    if min_width is None and min_height is None:
        return True

    try:
        with Image.open(image_path) as img:
            width, height = img.size
    except Exception as ex:
        print(f"PIL failed to open {image_path}")
        return False

    if min_width is not None:
        if width < min_width:
            return False

    if min_height is not None:
        if height < min_height:
            return False

    return True


def download_file(directory, filename, url, min_width, min_height):
    """
    :param directory: string, a valid folder that exists
    :param filename: string
    :param url: string
    :param min_width, min_height: int, if not None, then it will check the size restriction and if the file is too small
        it will delete the file and return False
    :return: False of download fails or the file is too small
        it downloads the url file into the folder with the given filename
    """
    img_data = None
    if url.startswith('data:image/'):
        try:
            img_data = base64.urlsafe_b64decode(url[url.find(',') + 1:])
        except Exception as ex:
            print(ex)
            return False

        open(os.path.join(directory, filename), "wb").write(img_data)

    else:
        try:
            response = requests.get(url)
            img_data = response.content
        except Exception as ex:
            print(ex)
            return False

    img_path = os.path.join(directory, filename)
    with open(img_path, "wb") as img_file:
        img_file.write(img_data)
        img_file.close()

    is_img_size_good = __is_img_size_good(img_path, min_width, min_height)
    if not is_img_size_good:
        os.remove(img_path)
    return is_img_size_good


class SearchEngine(object):
    """
    Base class for search engines
    """
    END_SIGNAL = '{END}'
    SCROLL_DELAY = 1.2

    def __init__(self, chrome_driver_path):
        self.chrome_driver = chrome_driver_path
        service_obj = Service(self.chrome_driver)
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--log-level=3")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=options, service=service_obj)
        self.driver.set_window_size(1505, 1000)
        self.next_page_btn = None
        self.img_class_ref = None
        self.has_next_result_btn = False
        self.must_type_search = False

    def _get_search_url(self):
        """
        Interface for fetching the base url
        """
        raise NotImplementedError()

    def _get_next_btn(self):
        raise NotImplementedError()

    def _found_next_btn(self):
        self.next_page_btn = None
        try:
            next_page_btn = self._get_next_btn()
            if next_page_btn is None:
                return False
            self.next_page_btn = next_page_btn
            return next_page_btn.is_displayed()
        except NoSuchElementException:
            return False

    def __exit__(self, exc_type, exc_value, traceback):
        self.driver.quit()

    def _found_next_btn(self):
        self.next_page_btn = None
        try:
            next_page_btn = self.driver.find_element(By.CLASS_NAME, "pagination__num--next")
            self.next_page_btn = next_page_btn
            return next_page_btn.is_displayed()
        except NoSuchElementException:
            return False

    def _go_to_next_page(self):
        if self.next_page_btn is None:
            raise Exception("The next page button is not found")
        self.next_page_btn.click()
        self.next_page_btn = None
        time.sleep(1)

    def _get_search_field(self):
        raise NotImplementedError()

    def _get_image(self, search):
        """
        :param search: string keywords to search
        :return: either an image url or base64 encrypted image data
        This is a generator function
        """
        logger.info('Scraping page links...')
        search_url = self._get_search_url(search)
        self.driver.get(search_url)

        if self.must_type_search:
            search_field = self._get_search_field()
            search = quote(search.encode('utf-8'))
            search_field.send_keys(f"{search}\n")

        images = set()
        for page_num in range(10):
            body = self.driver.find_element(By.TAG_NAME, 'body')
            reached_page_end = False
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            while not reached_page_end:
                body.send_keys(Keys.END)
                time.sleep(self.SCROLL_DELAY)
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if last_height == new_height:
                    reached_page_end = True
                else:
                    last_height = new_height

            for img in self.driver.find_elements(By.TAG_NAME, 'img'):
                src = img.get_attribute("src")
                class_name = img.get_attribute("class")
                class_check = True
                if self.img_class_ref is not None:
                    class_check = class_name.contains(self.img_class_ref)

                if src is not None and not src.endswith('.svg') and not src.startswith('data:image/svg')\
                        and class_check:
                    if src not in images:
                        images.add(src)
                        yield src

            if not self.has_next_result_btn:
                yield self.END_SIGNAL

            if self._found_next_btn():
                last_height = self.driver.execute_script("return document.body.scrollHeight")
                self._go_to_next_page()
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    yield self.END_SIGNAL


class Scraper(object):
    """
    Use this class to search the internet for images and download them
    """
    def __init__(self, search_engine: SearchEngine):
        self.search_engine = search_engine

    def download(self, keywords, directory, limit=10, min_width=None, min_height=None,  prefix='', postfix=''):
        """
        :param keywords: string
        :param directory: string, valid path
        :param limit: int
        :param min_width: int
        :param min_height: int
        :param prefix: string
        :param postfix: string
        :return: Nothing. It downloads files in the specified directory
        """
        gen = self.search_engine._get_image(keywords)
        img_count = 0
        img_filename_ind = 1
        for url in gen:
            if url == SearchEngine.END_SIGNAL:  # no more search results
                return

            file_type = url[url.rfind('.') + 1:]
            file_type = (file_type[:4]) if len(file_type) > 4 else file_type
            if file_type.lower() not in ["jpeg", "jfif", "exif", "tiff", "gif", "bmp", "png", "webp", "jpg"]:
                file_type = "jpg"

            filename = f'{prefix}{img_filename_ind}{postfix}.{file_type}'
            while os.path.exists(os.path.join(directory, filename)):
                img_filename_ind += 1
                filename = f'{prefix}{img_filename_ind}{postfix}.{file_type}'

            if download_file(directory, filename, url, min_width, min_height):
                url_log = ''
                if url.startswith('http'):
                    url_log = f'from {url}'
                logger.info(f"Downloaded file: {filename}{url_log}")
                img_count += 1

            if img_count >= limit:
                return

