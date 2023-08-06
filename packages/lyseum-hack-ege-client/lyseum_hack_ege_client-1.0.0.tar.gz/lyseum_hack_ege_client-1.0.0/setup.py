from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.rst").read_text()

setup(
    name='lyseum_hack_ege_client',
    version='1.0.0',
    license='MIT',
    author="grin-de-vald1",
    author_email='grin-de-vald1@ya.ru',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://pypi.org/project/lyseum_hack_ege_client/',
    keywords='hack lyseum client yandex-proxy',
    install_requires=['yadisk>=1.2.10'],
    long_description=long_description,
    long_description_content_type="text/x-rst",
)
