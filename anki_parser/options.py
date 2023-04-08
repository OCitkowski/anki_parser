MAX_CONCURRENT_TASKS = 5
TOTAL_TASKS = 100
REQUEST_TIMEOUT = 2


CHROME_OPTIONS = [
    # '--headless', #: безголовний режим роботи браузера
    '--disable-logging', #: вимкнути логування
    '--start-maximized', #: максимізувати вікно браузера після запуску
    '--no-sandbox', #: запускати браузер без піщаного ящика(sandbox)
    '--disable-gpu', #: вимкнути підтримку GPU в браузері
    '--user-data-dir=/tmp/user-data', #: вказати шлях до каталогу з користувацькими даними
    '--hide-scrollbars', #: приховати полосу прокрутки в браузері
    '--enable-logging', #: включити логування
    '--log-level=0', #: встановити рівень логування на 0(найнижчий рівень)
    '--v=99', #: встановити рівень подробиць логування на 99
    '--data-path=/tmp/data-path', #: вказати шлях до  каталогу з даними
    '--ignore-certificate-errors', #: ігнорувати помилки сертифікатів HTTPS
    '--homedir=/tmp', #: вказати домашній каталог для браузера
    '--disk-cache-dir=/tmp/cache-dir', #: вказати шлях до каталогу з кешем
    '--disable-blink-features=AutomationControlled', #: вимкнути певні функції браузера, які використовуються для автоматизації.
    '--disable-extensions',  #: вимкнути всі розширення браузера
    '--disable-popup-blocking',  #: вимкнути блокування виринаючих вікон
    '--disable-infobars',  #: вимкнути інформаційну панель браузера
    '--disable-notifications',  #: вимкнути сповіщення браузера
    '--disable-translate',  #: вимкнути автоматичний переклад сторінок
    '--disable-web-security',  #: вимкнути політику безпеки мережі Same-Origin
    '--window-position=0,0',  #: встановити позицію вікна браузера в лівий верхній кут екрану
    '--disable-remote-fonts',  #: вимкнути завантаження шрифтів з віддалених серверів
    '--disable-background-networking',  #: вимкнути фонову мережеву діяльність браузера
    '--disable-default-apps',  #: вимкнути встановлені за замовчуванням додатки браузера
    '--disable-client-side-phishing-detection',  #: вимкнути захист від фішингу на клієнтському боці
    '--disable-sync',  #: вимкнути синхронізацію даних між браузером та Google-аккаунтом
    '--disable-accelerated-video',  #: вимкнути прискорення відео
    '--disable-accelerated-2d-canvas',  #: вимкнути прискорення 2D-холсту
    '--disable-dev-shm-usage',  #: вимкнути використання /dev/shm для тимчасових файлів
    '--disable-setuid-sandbox',  #: вимкнути піщаний ящик на рівні системи
    '--disable-background-timer-throttling',  #: вимкнути затримки таймерів у фонових вкладка

    '--ignore-ssl-errors=yes',
    '--ignore-certificate-errors',

    'user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    '--disable-blink-features=AutomationControlled'
    # 'user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36', #: встановити користувацький рядок агента
    ]
