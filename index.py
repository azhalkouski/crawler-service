from selenium import webdriver
from selenium.webdriver.common.by import By
import sys, time

driver = webdriver.Chrome()
url = "https://selenium.dev"

if len(sys.argv) > 1:
  url = sys.argv[1]

driver.get(url)

acceptBtn = driver.find_element(By.ID, "onetrust-accept-btn-handler")
acceptBtn.click()

transactionsDropDown = driver.find_element(By.CSS_SELECTOR, sys.argv[2])
transactionsDropDown.click()

optionZero = driver.find_element(By.ID, sys.argv[3])
optionZero.click()

time.sleep(5)
driver.quit()