from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import logging
from utils.index import openServiceConfig, extract_numeric_word
from services.db_service import DataBaseService

log_format = '%(levelname)s:%(name)s:%(asctime)s:%(message)s'


class ScraperService:
    def __init__(self):
        self.serviceConfig = openServiceConfig()
        self.dataBaseService = DataBaseService()

        # TODO: self.info_logger, self.error_logger, self.critical_logger = LoggerFactory(__name__)

        formatter = logging.Formatter(log_format)

        self.info_logger = logging.getLogger(__name__ + '.info')
        self.error_logger = logging.getLogger(__name__ + '.error')
        self.critical_logger = logging.getLogger(__name__ + '.critical')

        error_logger_handler = logging.FileHandler(
            filename='error_level_logs.log', encoding='utf-8')
        error_logger_handler.setFormatter(formatter)
        critical_logger_handler = logging.FileHandler(
            filename='critical_level_logs.log', encoding='utf-8')
        critical_logger_handler.setFormatter(formatter)
        self.error_logger.addHandler(error_logger_handler)
        self.critical_logger.addHandler(critical_logger_handler)
        
        self.error_logger.setLevel(logging.ERROR)
        self.critical_logger.setLevel(logging.CRITICAL)


    def __scrape_apartments_count_for_city(self, city_name):
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


    def process_cities(self, cities):
        self.info_logger.info('Scraping process is running.')
        BREAKPOINT_COUNT = len(cities) + 5
        iteration_count = 0

        while len(cities) > 0:
            iteration_count += 1
            city = cities.pop(0)
            city_id, city_name = city

            try:
                count_of_units = self\
                  .__scrape_apartments_count_for_city(city_name)
            except Exception as e:
                cities.append(city)

                error_log = f"Failed to scrape for {city_name} with an error: {e}"
                print(error_log)
                self.error_logger.error(error_log)
            
                if iteration_count > BREAKPOINT_COUNT:
                    critical_log = (f"BREAKING THE CYCLE because of constantly "
                          f"failing to scrape for {cities} with an error: {e}")
                    print(critical_log)
                    self.critical_logger.critical(critical_log)

                    break
            else:
                print(city_id, city_name, count_of_units)
                self.dataBaseService.save_units_count(city[0], 'apartment',
                                                count_of_units)
        else:
            self.info_logger.info('Scraping process completed successfully.')
