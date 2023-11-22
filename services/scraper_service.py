from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from utils.index import openServiceConfig, extract_numeric_word


class ScraperService:
    def __init__(self):
        self.serviceConfig = openServiceConfig()


    def scrape_appartments_count_for_city(self, city_name):
        count = 0

        driver = webdriver.Chrome()
        url = self.serviceConfig["targetServiceUrl"]
        driver.get(url)

        driver.implicitly_wait(5)
        acceptBtn = driver.find_element(By.ID, self.serviceConfig["acceptCookiesBtnId"])
        acceptBtn.click()

        transactionsDropDown = driver.find_element(
            By.CSS_SELECTOR, self.serviceConfig["transactionTypeDropDownCssSelector"])
        transactionsDropDown.click()

        optionZero = driver.find_element(
            By.ID, self.serviceConfig["transactionTypeOprionZeroId"])
        optionZero.click()

        locationBtn = driver.find_element(By.ID, self.serviceConfig["locationBtnId"])
        locationBtn.click()
        driver.implicitly_wait(2)

        locationPicker = driver.find_element(
            By.ID, self.serviceConfig["locationPickerId"])
        locationPicker.click()
        locationPicker.send_keys(city_name)
        driver.implicitly_wait(5)


        searchedLocationInput = driver.find_element(
            By.ID, self.serviceConfig["dynamicallyMountedCityCheckboxIds"][city_name])
        driver.implicitly_wait(5)
        lishka = searchedLocationInput.find_element(By.XPATH, "./..")
        label = lishka.find_element(By.XPATH, f"//label[@for='{self.serviceConfig['dynamicallyMountedCityCheckboxIds'][city_name]}']")
        label.click()


        # Wait for 5 seconds because searchedLocationLiElement.click() initiates
        # a network request which then updates the search button text,
        # which in turn embeds the prior network request's response data
        # TODO: get rid of this wait. 5 sec is way too long
        time.sleep(3)

        searchBtn = driver.find_element(
            By.ID, self.serviceConfig["searchFormSubmitBtnId"])

        count = extract_numeric_word(searchBtn.text) \
          if extract_numeric_word(searchBtn.text) is not None else 0

        driver.quit()

        return count
