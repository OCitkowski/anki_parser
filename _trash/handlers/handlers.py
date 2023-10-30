from selenium.webdriver.common.by import By
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from _trash.config.settings import CHROME_OPTIONS, NAME_COOKIES_FILE, TIME_SLEEP
from _trash.utils.cookies_utils import set_cookies_to_browser
import logging

# Створення об'єкта логування
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# Створення обробника, який буде записувати логи в файл
handler = logging.FileHandler('verbformen_handlers.log')
handler.setLevel(logging.INFO)
# Створення форматувальника логів
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
# Додавання обробника до логера
logger.addHandler(handler)


def find_element_s_by_xpath(driver, xpatch_selector: str) -> list:
    try:
        elements = driver.find_elements(By.XPATH, xpatch_selector)  #
        found_elements = [element.text for element in elements]

        logger.info(f'Ok - {xpatch_selector} {found_elements}')
    except Exception as ex:
        found_elements = ['Failed']
        logger.error(f'Failed - {xpatch_selector} / {ex}')
    finally:
        time.sleep(TIME_SLEEP)

    return found_elements


def find_element_by_xpath(driver, xpatch_selector: str) -> list:
    try:
        found_elements = driver.find_element(By.XPATH, xpatch_selector)

        logger.info(f'Ok - {xpatch_selector}')
    except Exception as ex:
        logger.error(f'Failed - {xpatch_selector} / {ex}')
    finally:
        time.sleep(TIME_SLEEP)

    return found_elements


def parse_word(elements) -> list:
    result = []
    return result


if __name__ == '__main__':
    domen = 'https://www.verbformen.de/deklination/substantive/?w='
    # domen = 'https://www.verbformen.de/konjugation/beispiele/arbeiten.html'

    urls_test = [
        f"{domen}gehen",
        f"{domen}arbeiten",
    ]

    chrome_options = Options()
    for row in CHROME_OPTIONS:
        chrome_options.add_argument(row)

    capabilities = webdriver.DesiredCapabilities.CHROME.copy()
    print(f'Run localhost -----------')

    driver = webdriver.Chrome(desired_capabilities=capabilities,
                              service=Service(ChromeDriverManager().install()),
                              options=chrome_options)
    for url in urls_test:
        try:
            print(url)
            driver.get(url)
            set_cookies_to_browser(driver, NAME_COOKIES_FILE)

            selector_I = "//*[@id='vVdBxBox']/p[(contains(@class,'rInf'))]"
            elements_I = find_element_s_by_xpath(driver, selector_I)
            driver.refresh()
            selector_II = "//*[@lang='uk']/span"
            elements_II = find_element_s_by_xpath(driver, selector_II)
            driver.refresh()
            driver.refresh()
            selector_IV = "//*[@id='stammformen']"
            elements_IV = find_element_s_by_xpath(driver, selector_IV)
            print(elements_I, elements_II, elements_IV)

            # save_cookies_to_file(driver=driver, cookies_file_name=NAME_COOKIES_FILE)

        except Exception as ex:
            print(ex)
            # save_cookies_to_file(driver=driver, cookies_file_name=NAME_COOKIES_FILE)
