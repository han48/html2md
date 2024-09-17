from markdownify import markdownify as md
from bs4 import BeautifulSoup
import configparser
import glob
import os

config_file_name = 'config.ini'
config = configparser.ConfigParser()


def save_config():
    with open(config_file_name, 'w') as config_file:
        config.write(config_file)


def load_config():
    config.read(config_file_name)
    if (not config.has_option('source', 'path')):
        config['source'] = {
            'path': '../source'
        }
        save_config()
    if (not config.has_option('destination', 'path')):
        config['destination'] = {
            'path': '../destination'
        }
        save_config()


load_config()

source_directory = config['source']['path']
source_path = os.path.join(source_directory, "*.html")
if not os.path.exists(source_directory):
    os.makedirs(source_directory)

destination_directory = config['destination']['path']
if not os.path.exists(destination_directory):
    os.makedirs(destination_directory)

html_files = sorted(glob.glob(source_path), reverse=True)
html_count = len(html_files)
for chapter in range(1, html_count + 1):
    file_name = html_files[chapter - 1]
    with open(file_name, 'r') as source:
        html_content = source.read()
        html = BeautifulSoup(html_content, 'html.parser')
        body_text = html.body.get_text(separator='\n', strip=True)
        with open(f'{destination_directory}/Chapter_{str(chapter).zfill(5)}.md', 'w') as destination:
            destination.write(body_text)
