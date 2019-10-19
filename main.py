import requests, os, re, calendar
from bs4 import BeautifulSoup


MONTHS = dict((month.lower(), num) for num, month in enumerate(calendar.month_name))
DATA_DIR = 'downloads'
DATA_PATH = os.path.join(os.getcwd(), DATA_DIR)
if not os.path.exists(DATA_PATH):
    os.mkdir(DATA_PATH)


def download_content(page: bytes, screen_resolution: str):
    """
    Download all wallpapers on the given page with given screen resolution.
    :param page: HTML-content in bytes.
    :param screen_resolution: Users screen resolution.
    """
    download_path = os.path.join(DATA_PATH, 'september')
    if not os.path.exists(download_path):
        os.mkdir(download_path)
    content_soup = BeautifulSoup(page, 'html.parser')
    wallpapers = content_soup.find_all('h3', id=True)
    downloads_count = 0

    for wallpaper in wallpapers:
        print(wallpaper.get_text())
        links = wallpaper.find_next_sibling('ul').find_all('a', text=screen_resolution)

        for link in links:
            download_link = link.get('href')
            filename = re.search(r'/([^\/]+\.\w{3}$)', download_link)[1]
            file_path = os.path.join(download_path, filename)
            print(download_link)
            download_request = requests.get(download_link)
            if download_request.status_code == 200:
                with open(file_path, 'wb') as f:
                    f.write(download_request.content)
                    print(f'{filename} downloaded.')
                    downloads_count += 1
        print()
    print(f'Total wallpapers downloaded: {downloads_count}.')


def get_page(year: int, month: str) -> bytes:
    main_url = 'https://www.smashingmagazine.com/'
    prev_year, prev_month = calendar.prevmonth(year, MONTHS[month])
    url = f'{main_url}{prev_year}/{str(prev_month).zfill(2)}/desktop-wallpaper-calendars-{month}-{year}/'
    page = requests.get(url)

    if page.status_code == 200:
        print(page.status_code)
        return page.content


def main():
    resolution = '1680x1050'
    content = get_page(2019, 'may')
    if content:
        download_content(content, resolution)
    else:
        print('No content found. Try another time range.')


if __name__ == '__main__':
    main()
