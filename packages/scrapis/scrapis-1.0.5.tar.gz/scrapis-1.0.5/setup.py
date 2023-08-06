from setuptools import setup
import os
import sys

with open("README.md", "r") as fh:
	long_description = fh.read()

setup(name='scrapis',
		version='1.0.5',
		description='Google play downloader command line interface',
		long_description=long_description,
		long_description_content_type="text/markdown",
		author="Redzoua",
		author_email="mthaqafiah@gmail.com",
		url="https://github.com/redzoua/scrapis",
		license="AGPLv3",
		entry_points={
			'console_scripts': [
				'scrapis = scrapis.scrapis:main',
			],
		},
		packages=[
			'scrapis',
		],
		package_dir={
			'scrapis': 'scrapis',
		},
		setup_requires=[
			"wheel"
		],
		install_requires=[
            "setuptools>=61.0",
            "parsel>=1.6.0",
            "selenium>=4.4.0",
            "python-slugify>=6.1.2",
            "requests>=2.28.1",
			"google-play-scraper>=1.2.2",
		],
)
