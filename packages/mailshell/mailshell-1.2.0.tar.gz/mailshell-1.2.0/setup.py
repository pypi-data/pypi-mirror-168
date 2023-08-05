import pip
from pathlib import Path
from setuptools import setup
from setuptools import find_packages
from pip._internal import main


def pip_install(package):
    try:
        main(['install', package])
    except AttributeError:
        from pip import __main__ as pmain
        pmain._main(['install', package])


# install requirements
pip_install('requests')
pip_install('html2text')

# read text from README file 
current_folder = Path(__file__).parent
README = (current_folder / "README.md").read_text()

setup(
    name="mailshell",
    version="1.2.0",
    author="Malki Abderrahman",
    author_email="abdo.malkiep@gmail.com",
    description="Create and send emails faster from the terminal",
    long_description=README,
    long_description_content_type='text/markdown',
    url="https://github.com/malkiAbdoo/mailshell",
    project_urls={
        'Source': 'https://github.com/malkiAbdoo/mailshell',
        'Tracker': 'https://github.com/joelibaceta/mailshell/issues'
    },
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.10",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="terminal, app, email, gmail, shell",
    entry_points={
        "console_scripts": ['msl=mailshell.app:main']
    }
)
