#! /usr/bin/env python3

import os
import sys
import json
import enum
import argparse
from pkg_resources import get_distribution, DistributionNotFound
import logging
from scrapis.apkcombo import Apkcombo
from google_play_scraper import app

try:
	__version__ = '%s [Python%s] ' % (get_distribution('scrapis').version, sys.version.split()[0])
except DistributionNotFound:
	__version__ = 'unknown: scrapis not installed'

logging.basicConfig(level = logging.INFO)
logger  = logging.getLogger(__name__)  # default level is WARNING
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
logger.addHandler(handler)
logger.propagate = False


class ERRORS(enum.IntEnum):
	"""
	Contains constant errors for Gplaycli
	"""
	SUCCESS = 0
	ERROR_FETCHING_DOWNLOAD = 15
	TOKEN_DISPENSER_SERVER_ERROR = 6
	KEYRING_NOT_INSTALLED = 10
	CANNOT_LOGIN_GPLAY = 15

class Scrapper():
	def __init__(self, args=None):
		self.args = args
		self.locale = "en"
		self.country = "us"
		self.folder = None
		self.website = "apkcombo"
		self.driver = None
		if args.locale is not None:
			self.locale = args.locale

		if args.country is not None:
			self.country = args.country

		if args.progress is not None:
			self.progress_bar = args.progress

		if args.website is not None:
			self.website = args.website

		if args.folder is not None:
			self.folder = args.folder[0]

		if args.log is not None:
			self.logging_enable = args.log
		if self.website == "apkcombo":
			self.driver = Apkcombo(args = self.args)
	def dlink(self, appID):
		"""
		Get download link of an app
		"""
		link = {}
		try:
			link = self.driver.getDownloadLink(appID)
		except:
			link = None
		if not link:
			logger.info("No link found")
			return
		print(json.dumps(link))
	def details(self, appID):
		"""
		Get download link of an app
		"""
		details = {}
		try:
			details = app(
			    appID,
			    lang=self.locale, # defaults to 'en'
			    country=self.country, # defaults to 'us'
			)
		except:
			details = {}
		link = {}
		try:
			link = self.driver.getDownloadLink(appID)
		except:
			logger.info("No link found")
		details["download"] = link
		print(json.dumps(details))
def main():
	"""
	Main function.
	Parse command line arguments
	"""
	parser = argparse.ArgumentParser(description="A Google Play Store Apk downloader and manager for command line")
	parser.add_argument('-v',  '--version',				help="Print version number and exit", action='store_true')
	parser.add_argument('-s',  '--search',				help="Search the given string in Google Play Store", metavar="SEARCH")
	parser.add_argument('-d',  '--download',			help="Download the Apps that map given AppIDs", metavar="AppID", nargs="+")
	parser.add_argument('-av', '--append-version',		help="Append versionstring to APKs when downloading", action='store_true')
	parser.add_argument('-a',  '--additional-files',	help="Enable the download of additional files", action='store_true', default=False)
	parser.add_argument('-f',  '--folder',				help="Where to put the downloaded Apks, only for -d command", metavar="FOLDER", nargs=1, default=['.'])
	parser.add_argument('-p',  '--progress',			help="Prompt a progress bar while downloading packages", action='store_true')
	parser.add_argument('-dl',  '--dlink',				help="Get the download link ID", metavar="DLINK")
	parser.add_argument('-dt',  '--details',			help="Get app details", metavar="DETAILS")
	parser.add_argument('-locale',  '--locale',			help="Language to use gplay with", metavar="LOCALE")
	parser.add_argument('-c',  '--country',				help="Country to use gplay with", metavar="COUNTRY")
	parser.add_argument('-w',  '--website',				help="Website to scrapp from", metavar="WEBSITE")
	parser.add_argument('-dpath',  '--dpath',			help="Folder driver path", metavar="WEBSITE")
	parser.add_argument('-r',  '--retry',				help="Number of retries", metavar="RETRIES", default= 0)
	parser.add_argument('-t',  '--timeout',				help="Timout in seconds", metavar="TIMEOUT", default= 0)
	parser.add_argument('-L',  '--log',					help="Enable logging of apps status in separate logging files", action='store_true', default=False)

	if len(sys.argv) < 2:
		sys.argv.append("-h")

	args = parser.parse_args()

	if args.version:
		print(__version__)
		return

	scrapper = Scrapper(args)

	if args.dlink:
		scrapper.dlink(args.dlink)

	if args.details:
		scrapper.details(args.details)

	if args.search:
		scrapper.search(args.search)

	if args.download is not None:
		print(json.dumps(scrapper.driver.download(args.download)))


if __name__ == '__main__':
	main()
