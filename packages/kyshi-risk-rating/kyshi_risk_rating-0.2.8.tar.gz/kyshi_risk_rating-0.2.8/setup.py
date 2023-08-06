import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = '0.2.8'
PACKAGE_NAME = 'kyshi_risk_rating'
AUTHOR = 'raphaelolams'
AUTHOR_EMAIL = 'raphealolams@gmail.com'
URL = 'https://github.com/KyshiTransfer/risk-rating.git'

LICENSE = 'MIT License'
DESCRIPTION = 'Module that handles Kyshi Risk Rating calculation'
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [

]

setup(name=PACKAGE_NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      long_description_content_type=LONG_DESC_TYPE,
      author=AUTHOR,
      license=LICENSE,
      author_email=AUTHOR_EMAIL,
      url=URL,
      project_urls={
          "Bug Tracker": URL,
      },
      install_requires=INSTALL_REQUIRES,
      setup_requires=['wheel'],
      packages=find_packages()
      )
