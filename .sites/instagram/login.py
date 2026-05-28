import sys
import time
import pickle
import os
import traceback

from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


LOG_FILE = "debug_log.txt"


def log(message):

    print(message)

    with open(LOG_FILE, "a", encoding="utf-8") as f:

        f.write(
            f"{time.strftime('%Y-%m-%d %H:%M:%S')} -> "
            f"{message}\n"
        )


def login_instagram(username, password):

    driver = None

    try:

        log("SCRIPT STARTED")

        options = Options()

        log("OPTIONS CREATED")

        # --------------------------------
        # GOOGLE CHROME PATH
        # --------------------------------

        options.binary_location = "/usr/bin/google-chrome"

        # --------------------------------
        # UBUNTU / WSL FIXES
        # --------------------------------

        options.add_argument("--headless=new")

        options.add_argument("--no-sandbox")

        options.add_argument("--disable-dev-shm-usage")

        options.add_argument("--disable-gpu")

        options.add_argument("--remote-debugging-port=9222")

        options.add_argument("--window-size=1920,1080")

        # --------------------------------
        # ANTI DETECT
        # --------------------------------

        options.add_argument(
            "--disable-blink-features=AutomationControlled"
        )

        options.add_experimental_option(
            "excludeSwitches",
            ["enable-automation"]
        )

        options.add_experimental_option(
            "useAutomationExtension",
            False
        )

        log("OPTIONS ADDED")

        # --------------------------------
        # PROFILE
        # --------------------------------

        profile_path = os.path.join(
            os.getcwd(),
            "instagram_profile"
        )

        if not os.path.exists(profile_path):

            os.makedirs(profile_path)

            log("PROFILE CREATED")

        options.add_argument(
            f"--user-data-dir={profile_path}"
        )

        # --------------------------------
        # CHROMEDRIVER PATH
        # --------------------------------

        chromedriver_path = (
            "/home/user/chromedriver-linux64/chromedriver"
        )

        log(
            f"CHROMEDRIVER PATH: "
            f"{chromedriver_path}"
        )

        service = Service(
            executable_path=chromedriver_path,
            log_path="chromedriver.log"
        )

        log("CREATING DRIVER")

        driver = webdriver.Chrome(
            service=service,
            options=options
        )

        log("DRIVER CREATED")

        # --------------------------------
        # PATCH WEBDRIVER
        # --------------------------------

        driver.execute_script("""
            Object.defineProperty(
                navigator,
                'webdriver',
                {
                    get: () => undefined
                }
            )
        """)

        log("WEBDRIVER PATCHED")

        wait = WebDriverWait(driver, 15)

        cookies_file = "instagram_cookies.pkl"

        # --------------------------------
        # LOGIN WITH COOKIES
        # --------------------------------

        if os.path.exists(cookies_file):

            log("COOKIES FILE EXISTS")

            driver.get(
                "https://www.instagram.com/"
            )

            log("INSTAGRAM OPENED")

            time.sleep(2)

            with open(cookies_file, "rb") as f:

                cookies = pickle.load(f)

                for cookie in cookies:

                    try:

                        driver.add_cookie(cookie)

                    except Exception as cookie_error:

                        log(
                            f"COOKIE ERROR: "
                            f"{str(cookie_error)}"
                        )

            log("COOKIES LOADED")

            driver.refresh()

            time.sleep(3)

            log(
                f"CURRENT URL AFTER COOKIE: "
                f"{driver.current_url}"
            )

            if (
                "accounts/login"
                not in driver.current_url
            ):

                log("LOGIN SUCCESS USING COOKIES")

                print("true")

                driver.quit()

                return True

        # --------------------------------
        # OPEN LOGIN PAGE
        # --------------------------------

        log("OPENING LOGIN PAGE")

        driver.get(
            "https://www.instagram.com/accounts/login/"
        )

        log(
            f"LOGIN PAGE URL: "
            f"{driver.current_url}"
        )

        # --------------------------------
        # USERNAME INPUT
        # --------------------------------

        username_input = wait.until(
            EC.presence_of_element_located(
                (By.NAME, "username")
            )
        )

        log("USERNAME INPUT FOUND")

        username_input.clear()

        username_input.send_keys(username)

        log("USERNAME ENTERED")

        # --------------------------------
        # PASSWORD INPUT
        # --------------------------------

        password_input = wait.until(
            EC.presence_of_element_located(
                (By.NAME, "password")
            )
        )

        log("PASSWORD INPUT FOUND")

        password_input.clear()

        password_input.send_keys(password)

        log("PASSWORD ENTERED")

        # --------------------------------
        # LOGIN SUBMIT
        # --------------------------------

        password_input.send_keys(Keys.RETURN)

        log("LOGIN SUBMITTED")

        time.sleep(7)

        current_url = driver.current_url

        log(
            f"FINAL URL: "
            f"{current_url}"
        )

        # --------------------------------
        # LOGIN SUCCESS
        # --------------------------------

        if (
            "accounts/login"
            not in current_url
        ):

            log("LOGIN SUCCESS")

            with open(cookies_file, "wb") as f:

                pickle.dump(
                    driver.get_cookies(),
                    f
                )

            log("COOKIES SAVED")

            print("true")

            driver.quit()

            return True

        # --------------------------------
        # LOGIN FAILED
        # --------------------------------

        else:

            log("LOGIN FAILED")

            try:

                with open(
                    "instagram_error_page.html",
                    "w",
                    encoding="utf-8"
                ) as f:

                    f.write(driver.page_source)

                log("ERROR PAGE SAVED")

            except Exception as html_error:

                log(
                    f"HTML SAVE ERROR: "
                    f"{str(html_error)}"
                )

            print("false")

            driver.quit()

            return False

    except Exception as e:

        log("EXCEPTION HAPPENED")

        log(str(e))

        log(traceback.format_exc())

        print("false")

        if driver:

            try:

                driver.quit()

            except:

                pass

        return False


if __name__ == "__main__":

    if len(sys.argv) >= 3:

        username = sys.argv[1]

        password = sys.argv[2]

        login_instagram(
            username,
            password
        )

    else:

        print("false")
