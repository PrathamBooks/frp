from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def test_selenium_basic():
  # Use webdriver.Ie() for Internet Explorer
  driver = webdriver.Firefox()
  driver.get("http://frp-test.prathambooks.org/")
  assert "Pratham" in driver.title
  assert "Calligraphy" in driver.page_source
  driver.close()

