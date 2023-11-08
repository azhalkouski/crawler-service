from selenium import webdriver
import sys

driver = webdriver.Chrome()
url = "https://selenium.dev"

if len(sys.argv) > 1:
  url = sys.argv[1]

driver.get(url)
driver.quit()