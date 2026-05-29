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


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LOG_FILE = os.path.join(BASE_DIR, "debug_log.txt")


def log(message):

    print(message, flush=True)

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

        options.binary_location = "/usr/bin/google-chrome"

        # -------------------------
        # UBUNTU / WSL
        # -------------------------

        options.add_argument("--no-sandbox")

        options.add_argument("--disable-dev-shm-usage")

        options.add_argument("--disable-gpu")

        options.add_argument("--window-size=1920,1080")

        options.add_argument("--start-maximized")

        options.add_argument("--remote-debugging-port=9222")

        # -------------------------
        # SPEED
        # -------------------------

        options.add_argument("--disable-extensions")

        options.add_argument("--disable-notifications")

        # -------------------------
        # ANTI BOT
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

        log("OPTIONS READY")

        # -------------------------
        # PROFILE
        # -------------------------

        profile_path = os.path.join(
            BASE_DIR,
            "instagram_profile"
        )

        if not os.path.exists(profile_path):

            os.makedirs(profile_path)

        options.add_argument(
            f"--user-data-dir={profile_path}"
        )

        # -------------------------
        # CHROMEDRIVER
        # -------------------------

        chromedriver_path = (
            "/home/user/chromedriver-linux64/chromedriver"
        )

        log(f"CHROMEDRIVER: {chromedriver_path}")

        service = Service(chromedriver_path)

        log("CREATING DRIVER")

        driver = webdriver.Chrome(
            service=service,
            options=options
        )

        log("DRIVER CREATED")

        wait = WebDriverWait(driver, 60)

        # -------------------------
        # OPEN LOGIN PAGE
        # -------------------------

        login_url = (
            "https://www.instagram.com/accounts/login/"
        )

        log("OPEN LOGIN PAGE")

        driver.get(login_url)

        time.sleep(10)

        log(f"CURRENT URL: {driver.current_url}")

        # -------------------------
        # USERNAME INPUT
        # -------------------------

        username_input = wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//input[@name='username']"
                )
            )
        )

        log("USERNAME INPUT FOUND")

        username_input.click()

        username_input.clear()

        username_input.send_keys(username)

        log("USERNAME ENTERED")

        # -------------------------
        # PASSWORD INPUT
        # -------------------------

        password_input = wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//input[@name='password']"
                )
            )
        )

        log("PASSWORD INPUT FOUND")

        password_input.click()

        password_input.clear()

        password_input.send_keys(password)

        log("PASSWORD ENTERED")

        # -------------------------
        # LOGIN BUTTON
        # -------------------------

        password_input.send_keys(Keys.RETURN)

        log("LOGIN SUBMITTED")

        time.sleep(8)

        log(f"FINAL URL: {driver.current_url}")

        if "accounts/login" not in driver.current_url:

            log("LOGIN SUCCESS")

            cookies_path = os.path.join(
                BASE_DIR,
                "instagram_cookies.pkl"
            )

            with open(cookies_path, "wb") as f:

                pickle.dump(
                    driver.get_cookies(),
                    f
                )

            print("true")

        else:

            log("LOGIN FAILED")

            print("false")

        driver.quit()

    except Exception as e:

        log("EXCEPTION")

        log(str(e))

        log(traceback.format_exc())

        try:

            if driver:
                driver.quit()
        except:
            pass

        print("false")


if __name__ == "__main__":

    if len(sys.argv) >= 3:

        username = sys.argv[1]

        password = sys.argv[2]

        login_instagram(username, password)

    else:

        print("false")
