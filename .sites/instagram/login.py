import sys
import os
import time
import pickle
import traceback
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "debug_log.txt")


def log(message):
    print(message, flush=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} -> {message}\n")


def login_instagram(username, password):
    driver = None
    try:
        log("SCRIPT STARTED")
        options = uc.ChromeOptions()
        options.binary_location = "/usr/bin/google-chrome"
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-notifications")

        profile_path = os.path.join(BASE_DIR, "instagram_profile")
        if not os.path.exists(profile_path):
            os.makedirs(profile_path)
        options.add_argument(f"--user-data-dir={profile_path}")

        log("CREATING DRIVER")
        driver = uc.Chrome(
            options=options,
            browser_executable_path="/usr/bin/google-chrome",
            version_main=148,
            use_subprocess=True
        )

        log("DRIVER CREATED")
        wait = WebDriverWait(driver, 60)

        login_url = "https://www.instagram.com/accounts/login/"
        log("OPEN LOGIN PAGE")
        driver.get(login_url)
        time.sleep(5)
        log(f"CURRENT URL: {driver.current_url}")

        username_input = wait.until(EC.presence_of_element_located((By.NAME, "email")))
        log("USERNAME INPUT FOUND")
        username_input.click()
        username_input.clear()
        username_input.send_keys(username)
        log("USERNAME ENTERED")

        password_input = wait.until(EC.presence_of_element_located((By.NAME, "pass")))
        log("PASSWORD INPUT FOUND")
        password_input.click()
        password_input.clear()
        password_input.send_keys(password)
        log("PASSWORD ENTERED")

        password_input.send_keys(Keys.RETURN)
        log("LOGIN SUBMITTED")

        time.sleep(8)
        log(f"FINAL URL: {driver.current_url}")

        if "accounts/login" not in driver.current_url:
            log("LOGIN SUCCESSFUL")
            cookies_path = os.path.join(BASE_DIR, "instagram_cookies.pkl")
            with open(cookies_path, "wb") as f:
                pickle.dump(driver.get_cookies(), f)
            print("true")
            return True
        else:
            log("LOGIN FAILED")
            print("false")
            return False

    except Exception as e:
        log("EXCEPTION")
        log(str(e))
        log(traceback.format_exc())
        print("false")
        return False

    finally:
        try:
            if driver:
                driver.quit()
        except:
            pass


if __name__ == "__main__":
    if len(sys.argv) >= 3:
        username = sys.argv[1]
        password = sys.argv[2]
        login_instagram(username, password)
    else:
        print("false")