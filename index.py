from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from utils.index import openServiceConfig


serviceConfig = openServiceConfig()

def scrape_appartments_count_for_city(city_id=0, city_name=serviceConfig["cityName"]):
    count = 0

    driver = webdriver.Chrome()
    url = serviceConfig["targetServiceUrl"]
    driver.get(url)

    acceptBtn = driver.find_element(By.ID, serviceConfig["acceptCookiesBtnId"])
    acceptBtn.click()

    transactionsDropDown = driver.find_element(
        By.CSS_SELECTOR, serviceConfig["transactionTypeDropDownCssSelector"])
    transactionsDropDown.click()

    optionZero = driver.find_element(
        By.ID, serviceConfig["transactionTypeOprionZeroId"])
    optionZero.click()

    locationBtn = driver.find_element(By.ID, serviceConfig["locationBtnId"])
    locationBtn.click()
    driver.implicitly_wait(2)

    locationPicker = driver.find_element(
        By.ID, serviceConfig["locationPickerId"])
    locationPicker.click()
    locationPicker.send_keys(city_name)
    driver.implicitly_wait(5)

    searchedLocationInput = driver.find_element(
        By.ID, serviceConfig["dynamicallyMountedCityCheckboxId"])
    searchedLocationLiElement = searchedLocationInput.find_element(
        By.XPATH, "./..")
    searchedLocationLiElement.click()

    # Wait for 5 seconds because searchedLocationLiElement.click() initiates
    # a network request which then updates the search button text,
    # which in turn embeds the prior network request's response data
    time.sleep(5)

    searchBtn = driver.find_element(
        By.ID, serviceConfig["searchFormSubmitBtnId"])
    print('searchBtn.text', searchBtn.text)

    # TODO: extract_numeric_word(string_with_numeric_word)

    driver.quit()

    return count


if __name__ == '__main__':
    scrape_appartments_count_for_city()
