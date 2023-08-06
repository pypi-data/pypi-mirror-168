from setuptools import setup, find_packages  # noqa: H301

NAME = "cropin-plotrisk-insight-client"
VERSION = "0.1.7"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["urllib3 >= 1.15", "six >= 1.10", "certifi", "python-dateutil", "plotrisk_sfplus_internal_client >= 0.0.9"]

setup(
    name=NAME,
    version=VERSION,
    description="Insights Service API",
    author_email="",
    url="",
    keywords=["Insights Service API -test"],
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    long_description="""\
    Cropin Plotrisk-Insight Client has functions to fetch plots, satellite, weather and yield details. It also exposes the plot image download function.

Important Definitions
Plot - A piece of land, represented by geojson structure i.e. Polygon, Multipolygon or a circle.

Satellite Data - For the plot created, satellite insights will be generated.

Yield - Yield mapping refers to the process of collecting georeferenced data on crop yield and characteristics, such as moisture content, while the crop is being harvested with an onboard yield monitor.

Weather - Weather data provides information about the weather and climate of a plot.

GDD - GDD (Cumulative growing degree days) is an index calculated from temperature data and is used to estimate the time needed for a crop or other organisms to reach a certain stage of development.

Prerequisites
1. Supported Python Version - This SDK has been tested with Python versions 3.5+. Earlier Python 3 versions are expected to work as well, as long as the dependencies are fulfilled.

Users who have already onboarded onto sf_plus, enabled plotrisk feature for atleast few plots will be able use this SDK.


    """
)
