import json


# cookies?
def set_cookies_to_browser(driver, cookies_file_name) -> bool:
    result = False
    try:
        driver.delete_all_cookies()
        open_cook_file = open(f"{cookies_file_name}.pkl", "r")
        cookies = json.load(open_cook_file)
        for cookie in cookies:
            try:
                driver.add_cookie(cookie)
                result = True
            except Exception as ex:
                print(ex)
    except:
        driver.refresh()
        result = False

    finally:
        try:
            open_cook_file.close()
            # print(f'set cookies is {result}')
        except Exception as ex:
            print(ex)

    return result


def save_cookies_to_file(driver, cookies_file_name) -> bool:
    result = False
    try:
        # print(cookies_file_name)

        with open(f"{cookies_file_name}.pkl", 'w') as write_file:
            json.dump(driver.get_cookies(), write_file, ensure_ascii=False)
            result = True
        # print(f'{cookies_file_name}.pkl save to root')
    except Exception as ex:
        print(f'{cookies_file_name}.pkl don`t save to root : {ex}')
    finally:
        write_file.close()

    return result
