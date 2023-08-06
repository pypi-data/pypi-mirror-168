from parsel import Selector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import os
import requests
import enum
from slugify import slugify


class ERRORS(enum.IntEnum):
    """
    Contains constant errors for Gplaycli
    """
    SUCCESS = 0
    ERROR_FETCHING_DOWNLOAD = 15
    NO_DOWNLOAD_LINK_FOUND = 6
    KEYRING_NOT_INSTALLED = 10
    CANNOT_LOGIN_GPLAY = 15


class Apkcombo():
    """docstring for ."""

    def __init__(self, args=None):
        self.driver_path = "G:\chromedriver\chromedriver.exe"
        self.download_folder = "G:\scraping"
        if args.dpath is not None:
            self.dpath = args.dpath
        if args.folder is not None:
            self.download_folder = args.folder[0]
        capa = DesiredCapabilities.CHROME
        capa["pageLoadStrategy"] = "none"
        proxy = "203.13.32.211:80"
        # configure chrome browser to not load images and javascript
        options = webdriver.ChromeOptions()
        # set window size to native GUI size
        options.add_argument("--window-size=1920,1080")
        options.add_argument("start-maximized")  # ensure window is full-screen
        options.add_argument('disable-infobars')
        # options.add_argument('--disable-gpu')
        options.add_argument('--headless')
        # options.add_argument('--proxy-server=%s' % proxy)
        options.add_experimental_option(
            # this will disable image loading
            "prefs", {"useAutomationExtension": False,
                      "intl.accept_languages": "en,en_US"}
        )
        options.add_experimental_option(
            "excludeSwitches", ["enable-logging", "enable-automation"])
        s = Service(self.driver_path)
        self.driver = webdriver.Chrome(
            service=s, options=options, desired_capabilities=capa)
        self.version = None
        self.filename = None

    def getDownloadLink(self, appID=None):
        self.driver.get("https://apkcombo.com/downloader/")
        # wait for page to load
        element = WebDriverWait(driver=self.driver, timeout=30).until(
            EC.presence_of_element_located((By.ID, 'package'))
        )
        # print("Search input showing")
        input = self.driver.find_element(By.NAME, "package")
        input.send_keys(appID)
        sumbitBtn = self.driver.find_element(By.ID, 'apksumbit')

        # Sumbit button
        sumbitBtn.click()
        # wait for URL to change with 15 seconds timeout

        linksTab = WebDriverWait(driver=self.driver, timeout=30).until(
            EC.presence_of_element_located((By.ID, 'apkcombo-tab'))
        )
        # print(element);
        elements = self.driver.find_elements(
            By.CSS_SELECTOR, '.file-list li a')
        links = [elem.get_attribute('href') for elem in elements]
        # print("Link has been fetched {link}".format(link = links[0]))
        # Download file
        # time.sleep(15)
        filterApks = []
        for link in links:
            if (".apk" in link and "&ip=" in link):
                filterApks.append(link)

        data = {}
        dlink = None
        try:
            dlink = filterApks[0]
        except IndexError:
            raise ERRORS.NO_DOWNLOAD_LINK_FOUND
        self.version = self.driver.find_element(
            By.CSS_SELECTOR, '.app_header .version').text
        self.version = slugify(self.version, max_length=20,
                               word_boundary=True, separator=".")
        self.filename = '{filename}.{version}{extension}'.format(
            filename=appID, version=self.version, extension='.apk')
        self.filename = slugify(
            self.filename, max_length=200, word_boundary=True, separator=".")
        self.driver.close()
        data['version'] = self.version
        data['filename'] = self.filename
        data['link'] = dlink
        return data

    def download(self, appID):
        data = {"ok": False, "code": 200, "filename": None, "message": None}
        try:
            link = self.getDownloadLink(appID)["link"]
            r = requests.get(link, allow_redirects=True)
            # Check if download folder exists or create it
            if not os.path.isdir(self.download_folder):
                os.makedirs(self.download_folder, exist_ok=True)
            filepath = os.path.join(self.download_folder, self.filename)
            if os.path.isfile(filepath):
                data["message"] = "File {filename} already exists, skipping.".format(
                    filename=self.filename)
            else:
                open(filepath, 'wb').write(r.content)
                data["message"] = "File has been downloaded successfully {filename}".format(
                    filename=self.filename)
            data["ok"] = True
            data["filename"] = self.filename
        except Exception as e:
            data["message"] = "Failed to download file {filename}".format(
                filename=self.filename)
            data["code"] = 500
        return data
