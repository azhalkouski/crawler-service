from selenium import webdriver
from selenium.webdriver.common.by import By
import time, json

with open('searchConfig.json') as search_config_file:
  search_config = json.load(search_config_file)


driver = webdriver.Chrome()
url = search_config["targetServiceUrl"]

driver.get(url)

acceptBtn = driver.find_element(By.ID, search_config["acceptCookiesBtnId"])
acceptBtn.click()

transactionsDropDown = driver.find_element(By.CSS_SELECTOR, search_config["transactionTypeDropDownCssSelector"])
transactionsDropDown.click()

optionZero = driver.find_element(By.ID, search_config["transactionTypeOprionZeroId"])
optionZero.click()

locationBtn = driver.find_element(By.ID, search_config["locationBtnId"])
locationBtn.click()
driver.implicitly_wait(2)
locationPicker = driver.find_element(By.ID, search_config["locationPickerId"])
locationPicker.click()
locationPicker.send_keys(search_config["cityName"])
driver.implicitly_wait(5)
searchedLocationInput = driver.find_element(By.ID, search_config["dynamicallyMountedCityCheckboxId"])
searchedLocationLiElement = searchedLocationInput.find_element(By.XPATH, "./..")
searchedLocationLiElement.click()

# wait 5 sec because searchedLocationLiElement.click() initiales a network req
# which then updates the search button text, which in turn embeds the prior
# network req's response data
time.sleep(5)
searchBtn = driver.find_element(By.ID, search_config["searchFormSubmitBtnId"])

print('searchBtn.text', searchBtn.text)

time.sleep(5)
driver.quit()