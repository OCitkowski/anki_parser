from selenium.webdriver.common.by import By
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from verbformen_parser.settings import CHROME_OPTIONS, CSS_SELECTOR, NAME_COOKIES_FILE, TIME_SLEEP
from verbformen_parser.utilites import set_cookies_to_browser, save_cookies_to_file
import logging

# Створення об'єкта логування
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Створення обробника, який буде записувати логи в файл
handler = logging.FileHandler('verbformen_parser.log')
handler.setLevel(logging.INFO)

# Створення форматувальника логів
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Додавання обробника до логера
logger.addHandler(handler)


def find_elements_by_css(driver, css_selector: str) -> dict:
    try:
        found_elements = driver.find_elements(By.CSS_SELECTOR, css_selector)
        logger.info(f'Ok - {css_selector}')
    except Exception as ex:
        logger.error(f'Failed - {css_selector} / {ex}')
    finally:
        time.sleep(TIME_SLEEP)

    return found_elements


def find_element_s_by_xpath(driver, xpatch_selector: str) -> dict:
    try:
        found_elements = driver.find_elements(By.XPATH, xpatch_selector)

        logger.info(f'Ok - {xpatch_selector}')
    except Exception as ex:
        logger.error(f'Failed - {xpatch_selector} / {ex}')
    finally:
        time.sleep(TIME_SLEEP)

    return found_elements


def find_element_by_xpath(driver, xpatch_selector: str) -> dict:
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
    try:
        # Проходимося по кожному елементу та отримуємо потрібні дані
        for element in elements:
            # Отримуємо значення 'невідомого слова 1'
            # word_1 = element.find_element(By.XPATH, "./img").get_attribute("alt")
            word_1 = element.text.split()[0]
            # Отримуємо значення 'невідомого слова 2'
            word_2 = element.find_element(By.XPATH, "./b").text
            # Отримуємо значення посилання
            link = element.find_element(By.XPATH, "./a").get_attribute("href")
            # Виводимо отримані дані у вказаному форматі
            # print(f"'{word_1}' '{word_2}' {link}")

        result = [word_1, word_2, link]
    except Exception as ex:
        logger.error(f'Failed / {ex}')

    return result


def parse_level(elements) -> list:
    result = []
    try:
        # Проходимося по кожному елементу та отримуємо потрібні дані
        for element in elements:
            word_1 = element.find_element(By.XPATH, "./b/span").text
            word_2 = element.text.split("·")[1].strip()
            result = f"'{word_1}' '{word_2}'"

        result = [word_1, word_2]
    except Exception as ex:
        logger.error(f'Failed / {ex}')

    return result


def find_elements_by_css_to_list(driver, css_selector_s: list) -> list:
    found_elements = []

    for i in css_selector_s:
        try:
            full_row = ''
            elements = driver.find_elements(By.CSS_SELECTOR, i)
            for row in elements:
                full_row += f'{row.text}; '

            found_elements.append(full_row)
        except:

            found_elements.append(' ')
        finally:
            time.sleep(5)

    return found_elements


if __name__ == '__main__':
    urls = ['https://www.verbformen.de/deklination/substantive/?w=Katze',
            'https://www.verbformen.de/deklination/substantive/?w=Gabel',
            'https://www.verbformen.de/deklination/substantive/?w=tanzen',
            ]

    chrome_options = Options()
    for row in CHROME_OPTIONS:
        chrome_options.add_argument(row)

    capabilities = webdriver.DesiredCapabilities.CHROME.copy()
    print(f'Run localhost -----------')

    driver = webdriver.Chrome(desired_capabilities=capabilities,
                              service=Service(ChromeDriverManager().install()),
                              options=chrome_options)
    for url in urls:
        driver.get(url)
        set_cookies_to_browser(driver, NAME_COOKIES_FILE)
        selector_I = "//p[contains(@class,'vGrnd rCntr')]"
        elements_I = find_element_s_by_xpath(driver, selector_I)

        selector_II = "//p[contains(@class,'rInf')]"
        elements_II = find_element_s_by_xpath(driver, selector_II)

        save_cookies_to_file(driver=driver, cookies_file_name=NAME_COOKIES_FILE)
        print(parse_word(elements_I), parse_level(elements_II),)
