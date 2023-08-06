import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent
VERSION = '1.4.0'
PACKAGE_NAME = 'selenium_pro'
AUTHOR = 'DataKund'
AUTHOR_EMAIL = 'datakund@gmail.com'
URL = 'https://github.com/you/your_package'
LICENSE = 'Apache License 2.0'
DESCRIPTION = 'Automation Library'
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"
KEYWORDS="selenium no-html web-scraping bots test-automation no-code low-code cloud proxy datakund"
INSTALL_REQUIRES = [
      'requests','beautifulsoup4','webdriver-manager'
]

setup(name=PACKAGE_NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      long_description_content_type=LONG_DESC_TYPE,
      author=AUTHOR,
      license=LICENSE,
      author_email=AUTHOR_EMAIL,
      install_requires=INSTALL_REQUIRES,
      packages=find_packages(),
      package_data={'selenium_pro.webdriver.remote': ['*'],'selenium_pro.webdriver.firefox.amd64':['*'],'selenium_pro.webdriver.firefox.x86':['*'],'selenium_pro.webdriver.firefox':['*']},
      package_dir={'selenium_pro': 'selenium_pro'},
      keywords = KEYWORDS
      )