from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def wait(driver,time=5):
	driver.implicitly_wait(time)

def find_until_located(driver,find_by,name,timeout=60):
	return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((find_by, name)))

def find_until_clicklable(driver,find_by,name,timeout=60):
	return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((find_by, name)))

def scroll_to_element(driver,element):
	driver.execute_script("arguments[0].scrollIntoView();", element)
