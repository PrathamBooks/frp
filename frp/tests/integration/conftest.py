from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver import ActionChains as ac
from selenium.common.exceptions import TimeoutException
import pytest

@pytest.fixture(scope='module')
def test_browser(request):
	driver = webdriver.Firefox()
	return driver
	def fin():
		driver.quit()
	request.addfinalizer(fin)


