import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle
import os


def login_instagram(username, password):
    driver = None
    try:
        options = Options()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--start-maximized")
        options.add_argument("--disable-extensions")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        profile_path = os.path.join(os.getcwd(), "instagram_profile")
        if not os.path.exists(profile_path):
            os.makedirs(profile_path)
        options.add_argument(f"--user-data-dir={profile_path}")

        driver = webdriver.Chrome(options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        cookies_file = "instagram_cookies.pkl"
        if os.path.exists(cookies_file):
            driver.get("https://www.instagram.com/")
            time.sleep(2)
            with open(cookies_file, "rb") as f:
                cookies = pickle.load(f)
                for cookie in cookies:
                    driver.add_cookie(cookie)
            driver.refresh()
            time.sleep(3)

            if "accounts/login" not in driver.current_url:
                print("true")
                driver.quit()
                return True

        driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(3)

        wait = WebDriverWait(driver, 10)
        username_input = wait.until(EC.presence_of_element_located((By.NAME, "email")))
        username_input.clear()
        username_input.send_keys(username)

        password_input = driver.find_element(By.NAME, "pass")
        password_input.clear()
        password_input.send_keys(password)

        password_input.send_keys(Keys.RETURN)

        time.sleep(8)

        current_url = driver.current_url

        if "accounts/login" not in current_url:
            with open(cookies_file, "wb") as f:
                pickle.dump(driver.get_cookies(), f)
            print("true")
            driver.quit()
            return True
        else:
            print("false")
            driver.quit()
            return False

    except Exception as e:
        print("false")
        if driver:
            driver.quit()
        return False


if __name__ == "__main__":
    if len(sys.argv) >= 3:
        username = sys.argv[1]
        password = sys.argv[2]
        login_instagram(username, password)
    else:
        print("false")