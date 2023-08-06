from setuptools import setup, find_packages
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.rst").read_text()

setup(
    name='global_storage_json_dict',
    version='1.0.1',
    license='MIT',
    author="grin-de-vald1",
    author_email='grin-de-vald1@ya.ru',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://pypi.org/project/aiofiles/global_storage_json_dict',
    keywords='json storage flask synchron',
    install_requires=[],
    long_description=long_description,
    long_description_content_type="text/x-rst",
)