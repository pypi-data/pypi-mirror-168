import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

# get the version of the library
from eureka_requests import __version__ as _version

setup(
    name='eureka-requests',
    url="https://dev.azure.com/OsramDS/Tools/_git/eureka-requests",
    version=os.getenv('PYLIB_VERSION', '0.0.0'),    
    packages=find_packages(),
    license="MIT",
    keywords="Use eureka to make a request at different locations",
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    install_requires=[
        'requests',
        'py-eureka-client'
    ]
)