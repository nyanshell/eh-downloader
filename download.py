'''
eh downloader
'''
import os
import time
import json
from glob import glob

import click
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.common.exceptions import NoSuchElementException


MAIN_URL = 'https://exhentai.org'
FORUM_URL = 'https://forums.e-hentai.org'


def download_url(driver, url):
    wait = WebDriverWait(driver, 15)
    driver.get(url)
    img = driver.get_full_page_screenshot_as_png()
    with open('pg.png', 'wb') as fout:
        fout.write(img)
    click.echo(f'downloading {driver.current_url}')
    wait.until(presence_of_element_located((By.XPATH, '//*[@id="i7"]')))
    driver.find_element(By.XPATH, '/html/body/div[1]/div[6]/a').click()  # download link


def download_page(url, save_path, gecko_path, socks_proxy, cookies_file):
    with open(cookies_file) as fin:
        forum_cookies = json.load(fin)
    options = Options()
    options.headless = True
    s = Service(executable_path=gecko_path)

    # custom save location
    options.set_preference('browser.download.folderList', 2)
    options.set_preference('browser.download.manager.showWhenStarting', False)

    save_dir = os.path.join(save_path, url.rstrip('/').rsplit('/', 1)[-1])
    try:
        os.removedirs(save_dir)
    except OSError:
        pass
    os.mkdir(save_dir)
    save_dir = os.path.abspath(save_dir)
    click.echo(f'saving into {save_dir}')
    options.set_preference('browser.download.dir',  save_dir)

    # suppress download popup
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "image/jpeg, image/png")

    # set socks proxy
    if socks_proxy:
        proxy, port = socks_proxy.rsplit(':', 1)
        options.set_preference("network.proxy.type", 1)
        options.set_preference("network.proxy.socks", proxy)
        options.set_preference("network.proxy.socks_port", int(port))
        options.set_preference("network.proxy.socks_version", 5)

    # quit without popup
    options.set_preference("dom.disable_beforeunload", True)

    with Firefox(options=options, service=s) as d:
        d.get(FORUM_URL)
        for c in forum_cookies:
            d.add_cookie({
                'domain': c['Host raw'],
                'name': c['Name raw'],
                'value': c['Content raw'],
                'path': c['Path raw'],
                'expiry': int(c['Expires raw']),
                'httpOnly': True if c['HTTP only raw'] == 'true' else False
            })
        d.refresh()
        click.echo('forum loaded')

        # open main page
        d.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + 't')
        d.get(MAIN_URL)

        # doujinshi front page
        d.get(url)
        img = d.get_full_page_screenshot_as_png()
        with open('site.png', 'wb') as fout:
            fout.write(img)

        title = d.find_element(By.XPATH, '//*[@id="gj"]').text.strip()
        click.echo(f'doujinshi name: {title}')
        # get all urls
        links_dom = d.find_elements(By.XPATH, '/html/body//*[@class="gdtm"]')
        links = [l.find_element(By.TAG_NAME, 'a').get_attribute('href') for l in links_dom]
        # ignore first page
        max_tab = int(d.find_elements(By.XPATH, '/html/body/div[7]/table/tbody/tr/td/a')[-2].text)
        click.echo(f'total {max_tab} tabs in this doujinshi')
        for i in range(2, max_tab + 1):
            click.echo(f'loading tab {i}')
            d.get(url + f'?p={i-1}')
            links_dom = d.find_elements(By.XPATH, '/html/body//*[@class="gdtm"]')
            links.extend([l.find_element(By.TAG_NAME, 'a').get_attribute('href') for l in links_dom])

        total_pages = len(links)
        click.echo(f'total {total_pages} images')
        d.get(url)
        for i, l in enumerate(links):
            try:
                download_url(d, l)
                time.sleep(3.0)
            except NoSuchElementException:
                click.echo(f"can't download {l}")
                total_pages -= 1

        while len(glob(os.path.join(save_dir, '*'))) < total_pages:
            click.echo('waiting for download complete')
            time.sleep(3)

        os.rename(save_dir, os.join(save_path, title))
        click.echo(f'download complete, total {total_pages} images, exit.')
        d.quit()


@click.command()
@click.argument("url", type=str)
@click.option("--save-path", type=str, default='./')
@click.option("--gecko-path", type=str, default='./geckodriver')
@click.option("--socks-proxy", type=str)
@click.option("--cookies-file", type=str, default='cookies-forum.json')
def cli(url, save_path, gecko_path, socks_proxy, cookies_file):
    download_page(url, save_path, gecko_path, socks_proxy, cookies_file)


if __name__ == '__main__':
    cli()
