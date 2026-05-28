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

        # -------------------------
        # CHROME BINARY
        # -------------------------

        options.binary_location = "/usr/bin/google-chrome"

        # -------------------------
        # UBUNTU / WSL FIX
        # -------------------------

        options.add_argument("--headless=new")

        options.add_argument("--no-sandbox")

        options.add_argument("--disable-dev-shm-usage")

        options.add_argument("--disable-gpu")

        options.add_argument("--remote-debugging-port=9222")

        options.add_argument("--window-size=1920,1080")

        # -------------------------
        # ANTI DETECT
        # -------------------------

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

        # -------------------------
        # PROFILE
        # -------------------------

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

        # -------------------------
        # CHROMEDRIVER
        # -------------------------

        chromedriver_path = "/usr/bin/chromedriver"

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

        # -------------------------
        # PATCH
        # -------------------------

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

        # -------------------------
        # OPEN LOGIN PAGE
        # -------------------------

        log("OPENING LOGIN PAGE")

        driver.get(
            "https://www.instagram.com/accounts/login/"
        )

        log(
            f"CURRENT URL: "
            f"{driver.current_url}"
        )

        # -------------------------
        # USERNAME
        # -------------------------

        username_input = wait.until(
            EC.presence_of_element_located(
                (By.NAME, "username")
            )
        )

        log("USERNAME INPUT FOUND")

        username_input.send_keys(username)

        # -------------------------
        # PASSWORD
        # -------------------------

        password_input = wait.until(
            EC.presence_of_element_located(
                (By.NAME, "password")
            )
        )

        log("PASSWORD INPUT FOUND")

        password_input.send_keys(password)

        # -------------------------
        # SUBMIT
        # -------------------------

        password_input.send_keys(Keys.RETURN)

        log("LOGIN SUBMITTED")

        time.sleep(5)

        current_url = driver.current_url

        log(f"FINAL URL: {current_url}")

        if "accounts/login" not in current_url:

            log("LOGIN SUCCESS")

            print("true")

        else:

            log("LOGIN FAILED")

            print("false")

        driver.quit()

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
