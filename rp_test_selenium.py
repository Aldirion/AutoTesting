# -*- coding: utf-8 -*-

from selenium import webdriver
import logging
from selenium.webdriver.common.by import By
from datetime import datetime

#Проверяем доступность web-приложения
def test_driver_connection(url):
	driver = webdriver.Chrome()

	driver.get(url)

	title = driver.title
	description=driver.find_element(By.XPATH,"//meta[@name='description']").get_attribute("content")

	driver.implicitly_wait(0.5)

	# print(title)
	# print(description)
	logging.info(f"Title: {title}")
	logging.info(f"Description: {description}")

	driver.quit()

def main():
	logging.basicConfig(level=logging.INFO, filename="LOG.log",filemode="w",format="%(asctime)s %(levelname)s %(message)s")
	dt=datetime.now()
	logging.warning(f"Start log:{dt}")
	turl="https://rusprofile.ru"
	test_driver_connection(turl)

main()