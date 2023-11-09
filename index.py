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

locationBtn = driver.find_element(By.ID, sys.argv[4])
locationBtn.click()
driver.implicitly_wait(2)
locationPicker = driver.find_element(By.ID, sys.argv[5])
locationPicker.click()
locationPicker.send_keys(sys.argv[6])
driver.implicitly_wait(5)
searchedLocationInput = driver.find_element(By.ID, sys.argv[7])
searchedLocationLiElement = searchedLocationInput.find_element(By.XPATH, "./..")
searchedLocationLiElement.click()

# wait 5 sec because searchedLocationLiElement.click() initiales a network req
# which then updates the search button text, which in turn embeds the prior
# network req's response data
time.sleep(5)
searchBtn = driver.find_element(By.ID, sys.argv[8])

print('searchBtn.text', searchBtn.text)

time.sleep(5)
driver.quit()