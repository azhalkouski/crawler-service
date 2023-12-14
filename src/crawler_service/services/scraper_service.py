import time
from datetime import datetime
from typing import TypeVar

from crawler_service.services.abstract_db_service import AbstractDBService
from crawler_service.services.logger_factory import LoggerFactory
from crawler_service.utils.index import extract_numeric_word, open_service_config
from fake_headers import Headers
from selenium import webdriver
from selenium.webdriver.common.by import By

AbstractDBServiceT = TypeVar("AbstractDBServiceT", bound=AbstractDBService)


def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


"""
Respnsibility: obtain data and hand it over
Should not: load cities from db, save data to db
Should: be invoked with city, type_of_deal, type_of_unit passed via arguments
"""


class ScraperService:
    def __init__(self, db_service: AbstractDBServiceT):
        # Inversion of Control
        if not isinstance(db_service, AbstractDBService):
            raise TypeError(
                f"db_service must be an instance of AbstractDBService, "
                f"not {type(db_service)}"
            )
        self.db_service = db_service

        self.serviceConfig = open_service_config()

        loggerFactory = LoggerFactory(__name__)

        self.info_logger = loggerFactory.info_logger
        self.error_logger = loggerFactory.error_logger
        self.critical_logger = loggerFactory.critical_logger

        self.cities = db_service.load_all_cities()

    def __scrape_apartments_count_for_city(self, city_name):
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

            transactionsDropDown = driver.find_element(
                By.CSS_SELECTOR,
                self.serviceConfig["transactionTypeDropDownCssSelector"],
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

    def process_cities(self):
        print(f"processing at {get_current_time()}")
        if len(self.cities) == 0:
            return None

        self.info_logger.info("Scraping process is running.")
        BREAKPOINT_COUNT = len(self.cities) + 5
        iteration_count = 0

        while len(self.cities) > 0:
            iteration_count += 1
            city = self.cities.pop(0)
            city_id, city_name = city

            try:
                count_of_units = self.__scrape_apartments_count_for_city(city_name)
            except Exception as e:
                self.cities.append(city)

                error_log = f"Failed to scrape for {city_name} with an error: {e}"
                print(error_log)
                self.error_logger.error(error_log)

                if iteration_count > BREAKPOINT_COUNT:
                    critical_log = (
                        f"BREAKING THE CYCLE because of constantly "
                        f"failing to scrape for {self.cities} with an error: {e}"
                    )
                    print(critical_log)
                    self.critical_logger.critical(critical_log)

                    break
            else:
                print(city_id, city_name, count_of_units)
                self.db_service.save_units_count(city[0], "apartment", count_of_units)
        else:
            self.info_logger.info("Scraping process completed successfully.")
