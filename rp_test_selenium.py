# -*- coding: utf-8 -*-

from selenium import webdriver
import unittest
import logging
from selenium.webdriver.common.by import By
from datetime import datetime


class TestRP(unittest.TestCase):
	def setUp(self):
		logging.basicConfig(level=logging.INFO, filename="LOG.log",filemode="a",format="%(asctime)s %(levelname)s %(message)s")
		dt=datetime.now()
		logging.warning(f"Start log:{dt}")
		self.driver = webdriver.Chrome()
		self.addCleanup(self.driver.quit)

	#Проверяем доступность web-приложения
	def test_driver_connection(self):
		
		url="https://www.rusprofile.ru/"
		self.driver.get(url)

		title = self.driver.title
		description=self.driver.find_element(By.XPATH,"//meta[@name='description']").get_attribute("content")
		cur_url=self.driver.find_element(By.XPATH,"//meta[@property='og:url']").get_attribute("content")
		self.assertEqual(url,cur_url)
		self.driver.implicitly_wait(0.5)
		logging.warning("Переход на сайт выполнен успешно")
		logging.info(f"Title: {title}")
		logging.info(f"Description: {description}")
		self.driver.implicitly_wait(5.0)

	#Проверяем работоспособность поиска организации по ИНН
	def test_search_by_inn(self):
		
		url=url="https://www.rusprofile.ru/"
		inn="2801068082"

		self.driver.get(url)
		self.driver.implicitly_wait(0.5)
		#--------------------------------------------

		#Находим элементы (поисковая строка и кнопка "Найти")
		search_box=self.driver.find_element(By.CLASS_NAME,"index-search-input")
		search_submit=self.driver.find_element(By.CSS_SELECTOR, ".search-btn")

		#Выполняем шаги тест-кейса
		search_box.send_keys(inn)
		self.driver.implicitly_wait(2.5)
		search_submit.click()

		target_inn=self.driver.find_element(By.ID,"clip_inn").text

		#Проверяем совпадает ли искомый ИНН с ИНН в открытой карточке организации
		logging.info(f"Искомый ИНН: {inn}")
		logging.warning(f"Открытый ИНН: {target_inn}")
		self.assertEqual(inn,target_inn)
		logging.info(f"Тест успешен. Искомый ИНН ({inn}) совпадает с ИНН в открытой карточке ({target_inn})")

		#Проверяем работоспособность поиска организации по ИНН
	
	#Проверяем работоспособность поиска организации по ОГРН
	def test_search_by_ogrn(self):
		
		url=url="https://www.rusprofile.ru/"
		ogrn="1022800536440"

		self.driver.get(url)
		self.driver.implicitly_wait(1.5)
		#--------------------------------------------

		#Находим элементы (поисковая строка и кнопка "Найти")
		search_box=self.driver.find_element(By.CLASS_NAME,"index-search-input")
		search_submit=self.driver.find_element(By.CSS_SELECTOR, ".search-btn")

		#Выполняем шаги тест-кейса
		search_box.send_keys(ogrn)
		self.driver.implicitly_wait(2.5)
		search_submit.click()

		target_ogrn=self.driver.find_element(By.ID,"clip_ogrn").text

		#Проверяем совпадает ли искомый ИНН с ИНН в открытой карточке организации
		logging.info(f"Искомый ОГРН: {ogrn}")
		logging.warning(f"Открытый ОГРН: {target_ogrn}")
		self.assertEqual(ogrn,target_ogrn)
		logging.info(f"Тест успешен. Искомый ОГРН ({ogrn}) совпадает с ОГРН в открытой карточке ({target_ogrn})")

	#Проверяем работоспособность поиска организации по ОГРН
	def test_search_by_name(self):
		
		url=url="https://www.rusprofile.ru/"
		name='ООО "Рога и Копыта"'
		c=name.count(" ")+1

		self.driver.get(url)
		self.driver.implicitly_wait(1.5)
		#--------------------------------------------

		#Находим элементы (поисковая строка и кнопка "Найти")
		search_box=self.driver.find_element(By.CLASS_NAME,"index-search-input")
		search_submit=self.driver.find_element(By.CSS_SELECTOR, ".search-btn")

		#Выполняем шаги тест-кейса
		search_box.send_keys(name)
		self.driver.implicitly_wait(2.5)
		search_submit.click()

		self.driver.implicitly_wait(5.0)

		#Проверяем, что попали на страницу поиска
		search_page=self.driver.find_element(By.CLASS_NAME,"search-result-page")
		self.assertIsNotNone(search_page, "Не страница поиска")
		logging.info("Открыта страница поиска")

		#Проверяем, что выдача соответствует запросу
		search_result_elems=self.driver.find_elements(By.CLASS_NAME,"finded-text")
		sres=" "
		print(len(search_result_elems))
		self.driver.implicitly_wait(5.0)
		for e in range(0,c):
			sres += search_result_elems[e].text + " "
			# sres.join(search_result_elems[e].text)
		
		self.driver.implicitly_wait(5.0)
		self.assertRegex(sres,name)

		logging.warning(f"Искомая строка: {name}")
		logging.warning(f"Полученная из поисковой выдачи строка: {sres}")







def suite():
	suite=unittest.TestSuite()
	# suite.addTest(TestRP('test_search_by_inn'))
	# suite.addTest(TestRP('test_search_by_ogrn'))
	suite.addTest(TestRP('test_search_by_name'))
	return suite
		
if __name__ == '__main__':
	# unittest.main()
	runner = unittest.TextTestRunner()
	runner.run(suite())