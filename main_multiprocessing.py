import random
import time, json
from multiprocessing import Pool
from selenium import webdriver

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from anki_parser.settings import CHROME_OPTIONS, MAX_CONCURRENT_TASKS, TOTAL_TASKS, REQUEST_TIMEOUT
from anki_parser.utilites import save_cookies_to_file, set_cookies_to_browser, find_elements_by_css_to_list

# urls = ['https://www.verbformen.ru/sklonenie/sushhestvitelnye/Heft.htm',
#         'https://www.verbformen.ru/sklonenie/sushhestvitelnye/?w=hallen',
#         'https://www.verbformen.ru/sklonenie/sushhestvitelnye/Heft.htm',
#         'https://www.verbformen.ru/sklonenie/sushhestvitelnye/?w=hallen',
        # 'https://www.verbformen.ru/sklonenie/sushhestvitelnye/?w=hallen',
        # 'https://www.verbformen.ru/sklonenie/sushhestvitelnye/Heft.htm',
        # 'https://www.verbformen.ru/sklonenie/sushhestvitelnye/Heft.htm',
        # 'https://www.verbformen.ru/sklonenie/sushhestvitelnye/?w=hallen',
        # 'https://www.verbformen.ru/sklonenie/sushhestvitelnye/Heft.htm',
        # # 'https://www.verbformen.ru/sklonenie/sushhestvitelnye/?w=hallen',
        # ]

urls = ['https://dict.com/ukrainisch-deutsch/noch',
        'https://dict.com/ukrainisch-deutsch/hallo',
        'https://dict.com/ukrainisch-deutsch/morgen',
        ]

element_class_names = (
    "span.lex_ful_tran",
    "span.lex_ful_entr.l1",
    "span.lex_ful_pron",
    "span.lex_ful_morf",
    "span.lex_ful_form"
)
cookies_file_name = 'cookies'


def open_page(url):
    service_log_path = "/home/fox/PycharmProjects/anki_parser/chromedriver.log"

    chrome_options = Options()
    for row in CHROME_OPTIONS:
        chrome_options.add_argument(row)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                              options=chrome_options,
                              service_log_path=service_log_path)

    driver.get(url)
    set_cookies_to_browser(driver, cookies_file_name)

    finded_elements = find_elements_by_css_to_list(driver=driver, element_css_names=element_class_names)
    print(finded_elements)

    random_number = random.randint(3, 5)
    time.sleep(random_number)  # чекаємо random_number секунд, щоб сторінка повністю завантажилась

    save_cookies_to_file(driver, cookies_file_name)
    driver.quit()


if __name__ == '__main__':
    pool = Pool(processes=5)  # запускаємо не більше n процесів одночасно
    pool.map(open_page, urls)
    pool.close()
    pool.join()
