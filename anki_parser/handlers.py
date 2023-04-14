from selenium.webdriver.common.by import By
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from anki_parser.settings import CHROME_OPTIONS, CSS_SELECTOR, NAME_COOKIES_FILE
from anki_parser.utilites import set_cookies_to_browser


def find_elements_by_css(self, element_css_names: list) -> dict:
    # finded_elements = {}
    #
    # for i in element_css_names:
    #     try:
    #         full_row = ''
    #         elements = self.__browser.find_elements(By.CSS_SELECTOR, i)
    #         for row in elements:
    #             full_row += f'{row.text}; '
    #
    #         finded_elements[i] = full_row
    #     except:
    #
    #         finded_elements[i] = None
    #     finally:
    #         self.sleep()
    #
    # return finded_elements
    pass


def find_elements_by_css_to_list(driver, element_css_names: list) -> list:
    finded_elements = []

    for i in element_css_names:
        try:
            full_row = ''
            elements = driver.find_elements(By.CSS_SELECTOR, i)
            for row in elements:
                full_row += f'{row.text}; '

            finded_elements.append(full_row)
        except:

            finded_elements.append(' ')
        finally:
            time.sleep(5)

    return finded_elements


if __name__ == '__main__':
    url = 'https://dict.com/ukrainisch-deutsch/sein'

    chrome_options = Options()
    for row in CHROME_OPTIONS:
        chrome_options.add_argument(row)

    capabilities = webdriver.DesiredCapabilities.CHROME.copy()
    print(f'Run localhost -----------')

    driver = webdriver.Chrome(desired_capabilities=capabilities,
                              service=Service(ChromeDriverManager().install()),
                              options=chrome_options)

    driver.get(url)
    set_cookies_to_browser(driver, NAME_COOKIES_FILE)

    found_elements = find_elements_by_css_to_list(driver=driver, element_css_names=CSS_SELECTOR)
    print(found_elements)
