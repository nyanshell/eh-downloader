'''
run geckodriver first
'''
import os
import time
import json
from glob import glob

from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located


GECKO_PATH = '/home/scarlet/geckodriver'
FIRST_PAGE_URL = 'https://exhentai.org/s/b75240e130/1301695-1'
MAIN_URL = 'https://exhentai.org'
FORUM_URL = 'https://forums.e-hentai.org'

def download_url(driver, url):
    wait = WebDriverWait(driver, 15)
    driver.get(url)
    print('current url:', driver.current_url)
    wait.until(presence_of_element_located((By.XPATH, '//*[@id="i7"]')))
    driver.find_element(By.XPATH, '/html/body/div[1]/div[6]/a').click()  # download link


def download_page():
    """
    with open('cookies.json') as fin:
        cookies = json.load(fin)
    """
    with open('cookies-forum.json') as fin:
        forum_cookies = json.load(fin)
    options = Options()
    options.headless = True
    s = Service(executable_path=GECKO_PATH)
    # profile = webdriver.FirefoxProfile()
    options.set_preference('browser.download.folderList', 2) # custom location
    options.set_preference('browser.download.manager.showWhenStarting', False)
    # TODO save path
    SAVE_PATH = '/home/scarlet/eh_download/downloaded/b75240e130/'
    options.set_preference('browser.download.dir', SAVE_PATH)
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "image/jpeg, image/png")

    # set socks proxy
    options.set_preference("network.proxy.type", 1)
    options.set_preference("network.proxy.socks", "192.168.0.5")
    options.set_preference("network.proxy.socks_port", 2046)
    options.set_preference("network.proxy.socks_version", 5)

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
        print('forum loaded')

        # open main page
        d.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + 't')
        d.get(MAIN_URL)
        img = d.get_full_page_screenshot_as_png()
        with open('site.png', 'wb') as fout:
            fout.write(img)
        wait = WebDriverWait(d, 15)
        print('start loading page')
        d.get(FIRST_PAGE_URL)
        wait.until(presence_of_element_located((By.XPATH, '//*[@id="i7"]')))

        download_url(d, 'https://exhentai.org/s/5eefc9dbf7/1301695-3')
        d.quit()
        return
        print('start downloading first page.')
        d.find_element(By.XPATH, '//*[@id="i7"]').click()
        max_page = int(d.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div/span[2]').text.strip())
        print('max page ' + str(max_page))
        for i in range(2, max_page + 1):
            print(f'downloading page {i}')
            # url = FIRST_PAGE_URL.rsplit('-', 1)[0] + '-' + str(i)
            # print(url)
            d.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[2]/a[3]/img').click()
            wait = WebDriverWait(d, 15)
            print('current url:', d.current_url)
            wait.until(presence_of_element_located((By.XPATH, '//*[@id="i7"]')))
            d.find_element(By.XPATH, '/html/body/div[1]/div[6]/a').click()  # download link
            # /html/body/div[1]/div[6]/a

            img = d.get_full_page_screenshot_as_png()
            with open(f'page-{i}.png', 'wb') as fout:
                fout.write(img)

            time.sleep(3)
            while len(glob(os.path.join(SAVE_PATH, '*'))) < i:
                print('waiting for download complete')
                time.sleep(3)
        print('download complete, exit.')
        d.quit()


if __name__ == '__main__':
    download_page()