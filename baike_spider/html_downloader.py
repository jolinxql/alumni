from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from urllib import request
import time
url='贵州省 习近平'
dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = (
    "'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36")
driver = webdriver.PhantomJS(executable_path='c:\\Users\\xql\\Desktop\\alumni\\19大\\scripts\\phantomjs.exe',
                             desired_capabilities=dcap)
driver.set_page_load_timeout(10000)
driver.maximize_window()

class HtmlDownloader(object):
    def download(self, url):

        if 'http' in url:
            try:
                response = request.urlopen(url)
            except Exception:
                try:
                    response = request.urlopen(url)
                except Exception:
                    try:
                        response = request.urlopen(url)
                    except Exception:
                        try:
                            response = request.urlopen(url)
                        except Exception:
                            time.sleep(10)
                            try:
                                response = request.urlopen(url)
                            except Exception:
                                print('failed')
                                return None
            if response.getcode() != 200:
                return None
            return response.read().decode('utf-8')

        driver.get('https://www.baidu.com')
        driver.find_element_by_id('kw').send_keys(url)
        driver.find_element_by_id('su').submit()
        try:
            dr = WebDriverWait(driver, 20)
            dr.until(lambda the_driver: the_driver.find_element_by_id('1').is_displayed())
        except:
            print('failed')
            driver.get('https://www.baidu.com')
            driver.find_element_by_id('kw').send_keys(url)
            driver.find_element_by_id('su').submit()
            try:
                dr = WebDriverWait(driver, 20)
                dr.until(lambda the_driver: the_driver.find_element_by_id('1').is_displayed())
            except:
                print('failed2')
        data=driver.page_source
        return data

