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


def save_debug(driver):

    try:

        screenshot_path = os.path.join(
            BASE_DIR,
            "debug_screen.png"
        )

        html_path = os.path.join(
            BASE_DIR,
            "debug_page.html"
        )

        driver.save_screenshot(screenshot_path)

        with open(
            html_path,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(driver.page_source)

        log("SCREENSHOT SAVED")

        log("HTML SAVED")

    except Exception as e:

        log(f"DEBUG SAVE ERROR: {str(e)}")


def login_instagram(username, password):

    driver = None

    try:

        log("SCRIPT STARTED")

        options = Options()

        options.binary_location = "/usr/bin/google-chrome"

        # -------------------------
        # IMPORTANT
        # -------------------------

        # headless خاموش
        # چون Instagram روی WSL مشکل میده

        # options.add_argument("--headless=new")

        # -------------------------
        # UBUNTU FIXES
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

        options.add_argument("--disable-infobars")

        options.add_argument("--disable-notifications")

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

            log("PROFILE CREATED")

        options.add_argument(
            f"--user-data-dir={profile_path}"
        )

        # -------------------------
        # CHROMEDRIVER
        # -------------------------

        chromedriver_path = (
            "/home/user/chromedriver-linux64/chromedriver"
        )

        log(
            f"CHROMEDRIVER: "
            f"{chromedriver_path}"
        )

        service = Service(chromedriver_path)

        log("CREATING DRIVER")

        driver = webdriver.Chrome(
            service=service,
            options=options
        )

        log("DRIVER CREATED")

        driver.execute_script("""
            Object.defineProperty(
                navigator,
                'webdriver',
                {
                    get: () => undefined
                }
            )
        """)

        log("PATCHED")

        wait = WebDriverWait(driver, 30)

        # -------------------------
        # OPEN LOGIN PAGE
        # -------------------------

        login_url = (
            "https://www.instagram.com/accounts/login/"
        )

        log("OPENING LOGIN PAGE")

        driver.get(login_url)

        time.sleep(5)

        log(
            f"CURRENT URL: "
            f"{driver.current_url}"
        )

        save_debug(driver)

        # -------------------------
        # USERNAME
        # -------------------------

        username_input = wait.until(
            EC.visibility_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "input[name='username']"
                )
            )
        )

        log("USERNAME INPUT FOUND")

        username_input.clear()

        username_input.send_keys(username)

        log("USERNAME ENTERED")

        # -------------------------
        # PASSWORD
        # -------------------------

        password_input = wait.until(
            EC.visibility_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "input[name='password']"
                )
            )
        )

        log("PASSWORD INPUT FOUND")

        password_input.clear()

        password_input.send_keys(password)

        log("PASSWORD ENTERED")

        # -------------------------
        # SUBMIT
        # -------------------------

        password_input.send_keys(Keys.RETURN)

        log("LOGIN SUBMITTED")

        time.sleep(8)

        log(
            f"FINAL URL: "
            f"{driver.current_url}"
        )

        save_debug(driver)

        # -------------------------
        # SUCCESS
        # -------------------------

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

                save_debug(driver)

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
