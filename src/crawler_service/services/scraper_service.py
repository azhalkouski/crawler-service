import time

from crawler_service.services.logger_factory import LoggerFactory
from crawler_service.utils.index import (
    extract_numeric_word,
    get_current_time,
    open_service_config,
)
from fake_headers import Headers
from selenium import webdriver
from selenium.webdriver.common.by import By


class ScraperService:
    """
    Respnsibility: obtain data and hand it over
    Should not: load cities from db, save data to db
    Should: be invoked with city, type_of_deal, type_of_unit passed via arguments
    """

    def __init__(self):
        self.serviceConfig = open_service_config()

        loggerFactory = LoggerFactory(__name__)

        self.info_logger = loggerFactory.info_logger
        self.error_logger = loggerFactory.error_logger
        self.critical_logger = loggerFactory.critical_logger

    def scrape(self, city_name, type_of_unit, type_of_deal):
        print(f"ScraperService::{city_name}-{type_of_unit}-{type_of_deal}")
        count = 0

        headers = Headers(browser="firefox", os="linux", headers=True).generate()

        firefoxOptions = webdriver.FirefoxOptions()
        firefoxOptions.add_argument("-headless")
        service = webdriver.FirefoxService(
            executable_path=self.serviceConfig["geckodriver_path"]
        )

        for key, value in headers.items():
            firefoxOptions.add_argument(f"--header={key}: {value}")
            firefoxOptions.add_argument(
                "--header=Accept: ext/html,application/xhtml+xml,"
                "application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
            )
            firefoxOptions.add_argument("--header=Accept-Language: en-US,en;q=0.5")
            firefoxOptions.add_argument("--header=Host: www.otodom.pl")

        driver = webdriver.Firefox(options=firefoxOptions, service=service)
        url = self.serviceConfig["targetServiceUrl"]
        try:
            driver.get(url)

            driver.implicitly_wait(5)
            acceptBtn = driver.find_element(
                By.ID, self.serviceConfig["acceptCookiesBtnId"]
            )
            acceptBtn.click()

            if type_of_unit != "apartment":
                """apartment option is selected by default"""

                type_of_unit_dropdown_selector = self.serviceConfig["type_of_unit"][
                    "dropdown"
                ]
                dropdown_input_element = driver.find_element(
                    By.CSS_SELECTOR, type_of_unit_dropdown_selector
                )
                dropdown_input_element.click()
                unit_type_option_selector = self.serviceConfig["type_of_unit"][
                    f"{type_of_unit}"
                ]
                rooms_option_element = driver.find_element(
                    By.ID, unit_type_option_selector
                )
                rooms_option_element.click()

            if type_of_deal == "rent":
                """sell option is selected by default"""

                types_of_deal_selectors = self.serviceConfig["type_of_deal"]
                transactionsDropDown = driver.find_element(
                    By.CSS_SELECTOR,
                    types_of_deal_selectors["rent"],
                )
                transactionsDropDown.click()

                optionZero = driver.find_element(
                    By.ID, self.serviceConfig["transactionTypeOprionZeroId"]
                )
                optionZero.click()

            locationBtn = driver.find_element(
                By.ID, self.serviceConfig["locationBtnId"]
            )
            locationBtn.click()
            driver.implicitly_wait(2)

            locationPicker = driver.find_element(
                By.ID, self.serviceConfig["locationPickerId"]
            )
            locationPicker.click()
            locationPicker.send_keys(city_name)
            driver.implicitly_wait(5)

            searchedLocationInput = driver.find_element(
                By.ID,
                self.serviceConfig["dynamicallyMountedCityCheckboxIds"][city_name],
            )
            driver.implicitly_wait(5)
            lishka = searchedLocationInput.find_element(By.XPATH, "./..")
            label = lishka.find_element(
                By.XPATH,
                f"//label[@for='{self.serviceConfig['dynamicallyMountedCityCheckboxIds'][city_name]}']",
            )
            label.click()

            # Wait for 5 seconds because searchedLocationLiElement.click() initiates
            # a network request which then updates the search button text,
            # which in turn embeds the prior network request's response data
            # TODO: get rid of this wait. 5 sec is way too long
            time.sleep(3)

            searchBtn = driver.find_element(
                By.ID, self.serviceConfig["searchFormSubmitBtnId"]
            )

            count = (
                extract_numeric_word(searchBtn.text)
                if extract_numeric_word(searchBtn.text) is not None
                else 0
            )

        except Exception as e:
            driver.save_screenshot(f"screenshot-of-scraping-{get_current_time()}.png")
            self.error_logger.error(
                f"Failed to scrape for {city_name} with an error: {e}"
            )
            # buble up the exception to the caller
            raise e
        else:
            driver.quit()

        return count
