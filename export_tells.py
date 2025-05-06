from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import undetected_chromedriver as uc
from selenium_stealth import stealth
import random
import pickle
import json
import time

USERNAME = "boymoderology"
PASSWORD = '******************************************'

def gen_driver():
    try:
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.140 Safari/537.36"
        chrome_options = uc.ChromeOptions()
        # chrome_options.add_argument('--headless=new')
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("user-agent={}".format(user_agent))
        driver = uc.Chrome(options=chrome_options)
        stealth(driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True
        )
        return driver
    except Exception as e:
        print("Error in Driver: ",e)

def type_in_input(input_elem, word):
    for letter in word:
        input_elem.send_keys(letter)
        time.sleep(random.randint(50, 100) / 1000)

if __name__ == "__main__":
    driver = gen_driver()
    username_password = [USERNAME, PASSWORD]
    qnas = []

    driver.get("https://tellonym.me/%s" % USERNAME)
    time.sleep(2.02)
    driver.find_element(By.CLASS_NAME, "icon-login").click()
    time.sleep(2.02)
    for i, input_elem in enumerate(driver.find_elements(By.CLASS_NAME, "input-underline"), 0):
        type_in_input(input_elem, username_password[i])
        time.sleep(1.01)
    driver.find_elements(By.CLASS_NAME, "input-underline")[-1].send_keys(Keys.RETURN)

    time.sleep(5.05)
    driver.find_element(By.XPATH, "/html/body/div[1]/div/div").click()
    with open("cookies.json", "w") as f:
        json.dump(driver.get_cookies(), f)

    while True:
        try:
            for e in driver.find_elements(By.CLASS_NAME, "rmq-3ca56ea3"):
                try:
                    qna = [s.text for s in e.find_elements(By.TAG_NAME, "span")]
                except StaleElementReferenceException:
                    print("Skipped stale element...")
                    continue
                
                when = e.find_element(By.CSS_SELECTOR, "div[style='color: rgb(175, 175, 179); font-size: 12px; overflow-wrap: break-word; white-space: pre-wrap; word-break: break-word;']").text
                
                if qna[0] not in [q[0] for q in qnas]:
                    qnas.append(qna + [when])
                    print(len(qnas), qna, when)
            

            time.sleep(0.05)

            html = driver.find_element(By.TAG_NAME, 'html')
            html.send_keys(Keys.ARROW_DOWN)
            time.sleep(0.0001)
            html.send_keys(Keys.ARROW_DOWN)
        except KeyboardInterrupt:
            break

    driver.quit()

    with open("tells.json", "w") as f:
        json.dump(qnas, f, indent = 4)
