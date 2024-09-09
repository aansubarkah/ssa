import time

from RecaptchaSolver import RecaptchaSolver

from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

#driver.get("https://www.google.com/recaptcha/api2/demo")
driver.get('https://elhkpn.kpk.go.id/portal/user/login#announ')

recaptchaSolver = RecaptchaSolver(driver)

try:
    # Perform CAPTCHA solving
    recaptchaSolver.solveCaptcha()

except Exception as e:
    print(f"An error occurred: {e}")
    driver.quit()

time.sleep(10)

driver.quit()