import requests
import os
import re
import calendar
from bs4 import BeautifulSoup


MONTHS = dict((month.lower(), num) for num, month in enumerate(calendar.month_name))
DATA_DIR = 'downloads'
DATA_PATH = os.path.join(os.getcwd(), DATA_DIR)
if not os.path.exists(DATA_PATH):
    os.mkdir(DATA_PATH)


class Downloader(object):

    def __init__(self, resolution: str = None, year: int = None, month: str = None):
        if not resolution:
            print('Enter your screen resolution: ')
            self.resolution = f"{input(f'Enter width: ')}x{input(f'Enter height: ')}"
        else:
            self.resolution = resolution

        if not year:
            self.year = int(input('Enter year: '))
        else:
            self.year = year

        if not month:
            self.month = input('Enter month: ').lower()
        else:
            self.month = month

    def get_page(self):
        """
        Get HTML-content from web-page and pass it further for downloading.
        """
        main_url = 'https://www.smashingmagazine.com/'
        prev_year, prev_month = calendar.prevmonth(self.year, MONTHS[self.month])
        url = f'{main_url}{prev_year}/{str(prev_month).zfill(2)}/desktop-wallpaper-calendars-{self.month}-{self.year}/'
        page = requests.get(url)

        if page.status_code == 200:
            print(page.status_code)
            self.download_content(page.content)
        else:
            print('No content found. Try another month and/or year.')

    def download_content(self, page: bytes, resolution=None):
        """
        Download all wallpapers from given page with given resolution.
        :param page: Receives HTML-document, either downloaded via requests or loaded from disc.
        :param resolution: User screen resolution. Uses instance resolution by default but can be overridden.
        """
        if not resolution:
            resolution = self.resolution
        download_path_year = os.path.join(DATA_PATH, str(self.year))
        if not os.path.exists(download_path_year):
            os.mkdir(download_path_year)
        full_download_path = os.path.join(download_path_year, self.month)
        if not os.path.exists(full_download_path):
            os.mkdir(full_download_path)

        content_soup = BeautifulSoup(page, 'html.parser')
        wallpapers = content_soup.find_all('h3', id=True)
        downloads_count = 0

        for wallpaper in wallpapers:
            print(wallpaper.get_text())
            links = wallpaper.find_next_sibling('ul').find_all('a', text=resolution)

            for link in links:
                download_link = link.get('href')
                filename = re.search(r'/([^\/]+\.\w{3}$)', download_link)[1]
                file_path = os.path.join(full_download_path, filename)
                print(download_link)
                download_request = requests.get(download_link)
                if download_request.status_code == 200:
                    with open(file_path, 'wb') as f:
                        f.write(download_request.content)
                        print(f'{filename} downloaded.')
                        downloads_count += 1
            print()
        print(f'Total wallpapers downloaded: {downloads_count}.')


def main():
    downloader = Downloader()
    downloader.get_page()


if __name__ == '__main__':
    main()
