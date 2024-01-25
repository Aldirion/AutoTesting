# -*- coding: utf-8 -*-

from selenium import webdriver
import unittest
import logging
from selenium.webdriver.common.by import By
from datetime import datetime
from selenium.webdriver.common.action_chains import ActionChains
from pandas.io.clipboard import clipboard_get
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def get_attributes(driver, element) -> dict:
    return driver.execute_script(
        """
        let attr = arguments[0].attributes;
        let items = {}; 
        for (let i = 0; i < attr.length; i++) {
            items[attr[i].name] = attr[i].value;
        }
        return items;
        """,
        element
    )

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

	#Проверяем работоспособность поиска организации по ИНН – Тест 1
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
	
	#Проверяем работоспособность поиска организации по ОГРН – Тест 2
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

	#Проверяем работоспособность поиска организации по названию – Тест 3
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

	#Проверяем карточку организации – Тест 4
	def test_organization_card(self):
		
		url="https://www.rusprofile.ru/id/2727870"

		self.driver.get(url)
		self.driver.implicitly_wait(1.5)

		#Проверяем, что попали на страницу поиска
		company_page=self.driver.find_element(By.CLASS_NAME,"company-header")
		self.assertIsNotNone(company_page, "Не страница компании")
		logging.info("Открыта страница компании")

	#Проверяем получение выписки из ЕГРЮЛ – Тест 5
	def test_egrul(self):
		
		url="https://www.rusprofile.ru/id/2727870"
		name='ООО "Рога и Копыта"'

		self.driver.get(url)
		self.driver.implicitly_wait(1.5)

		#Проверяем, что попали на страницу компании
		company_page=self.driver.find_element(By.CLASS_NAME,"company-header")
		self.assertIsNotNone(company_page, "Не страница компании")
		self.driver.implicitly_wait(1.5)

		#Ищем нужный пункт меню
		more_btn = self.driver.find_element(By.CLASS_NAME, "company-menu_more")
		self.driver.implicitly_wait(1.5)
		more_btn.click()
		menus=self.driver.find_elements(By.CLASS_NAME,"flexpoint")		
		for m in menus:
			if m.text == "Выписка из ЕГРЮЛ":
					egrul_btn=m
					egrul_btn.click()
					break
		self.driver.implicitly_wait(5.0)

		#Проверяем, что открыли страницу для получения выписки из ЕГРЮЛ для конкретной организации
		egrul_page = self.driver.find_element(By.CLASS_NAME,"page-egrul-egrip")
		self.assertIsNotNone(egrul_page, "Не страница выписки из ЕГРЮЛ")
		cur_name = self.driver.find_element(By.CLASS_NAME,"statement-name").text
		self.assertEqual(name.upper(), cur_name)
		logging.info(f"Открыта страница 'Выписка из ЕГРЮЛ' для организации {cur_name}")

	#Проверяем получение реквизитов – Тест 6
	def test_requisites(self):
		
		url="https://www.rusprofile.ru/id/2727870"
		name='ООО "Рога и Копыта"'
		ogrn="1022800536440"

		self.driver.get(url)
		self.driver.implicitly_wait(1.5)

		#Проверяем, что попали на страницу компании
		company_page=self.driver.find_element(By.CLASS_NAME,"company-header")
		self.assertIsNotNone(company_page, "Не страница компании")
		self.driver.implicitly_wait(1.5)

		#Ищем нужный пункт меню
		more_btn = self.driver.find_element(By.CLASS_NAME, "company-menu_more")
		self.driver.implicitly_wait(1.5)
		more_btn.click()
		menus=self.driver.find_elements(By.CLASS_NAME,"flexpoint")		
		for m in menus:
			if m.text == "Реквизиты":
					egrul_btn=m
					egrul_btn.click()
					break
		self.driver.implicitly_wait(5.0)

		#Проверяем, что открыли страницу для получения выписки из ЕГРЮЛ для конкретной организации
		requisites_page = self.driver.find_element(By.CSS_SELECTOR,".content-frame__title").text
		self.assertEqual(requisites_page,"Реквизиты", "Не страница выписки из ЕГРЮЛ")
		cur_ogrn = self.driver.find_element(By.ID,"clip_ogrn").text
		self.assertEqual(ogrn, cur_ogrn)
		logging.info(f"Открыта страница 'Реквизиты' для организации {name}")

	#Проверяем копирование реквизитов в буфер обмена – Тест 7
	def test_clipboard(self):
		url="https://www.rusprofile.ru/requisites/2727870"
		name='ООО "Рога и Копыта"'
		ogrn="1022800536440"

		self.driver.get(url)
		self.driver.implicitly_wait(1.5)
		e_ogrn=self.driver.find_elements(By.CLASS_NAME, "requisites-item")
		requisites=self.driver.find_elements(By.CLASS_NAME, "requisites-item")
		for requisite in requisites:
			if requisite.find_element(By.CLASS_NAME, "requisites-item__name").text=="ОГРН":
				e_ogrn=requisite.find_element(By.CLASS_NAME, "requisites-item__value")
				break
		hover = ActionChains(self.driver).move_to_element(e_ogrn) #имитируем наведение мыши на элемент для отображения кнопки "Скопировать"
		hover.perform()
		ogrn_btn=e_ogrn.find_element(By.TAG_NAME, "button")
		ogrn_btn.click()
		self.driver.implicitly_wait(5.0)
		cb_text=clipboard_get()
		self.assertEqual(ogrn,cb_text)
		logging.info(f"Скопированное значение ОГРН: {cb_text}")

	#Проверяем вход в личный кабинет – Тест 8	
	def test_auth(self):
		
		url="https://www.rusprofile.ru/"
		name="John"
		email = "fewiyi1850@wuzak.com"
		pwd = "t37SvI82"

		self.driver.get(url)
		self.driver.implicitly_wait(500.0)
		#--------------------------------------------

		profile=WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='menu-personal-trigger']")))
		
		#Выполняем шаги тест-кейса
		profile.click()

		email_ph=self.driver.find_element(By.XPATH, "//*[@id='v-root']/div/div[1]/div[3]/div[2]/div/input")
		email_ph.send_keys(email)
		self.driver.implicitly_wait(2.5)

		pwd_ph=self.driver.find_element(By.XPATH, "//*[@id='v-root']/div/div[1]/div[3]/div[3]/div/input")
		pwd_ph.send_keys(pwd)
		self.driver.implicitly_wait(2.5)

		sub_btn=WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='v-root']/div/div[1]/div[3]/div[4]/button")))
		self.driver.implicitly_wait(2.5)
		sub_btn.click()
		self.driver.implicitly_wait(2.5)

		
		self.driver.implicitly_wait(2.5)
		auth_check=self.driver.find_element(By.ID,"menu-personal-trigger").find_element(By.CLASS_NAME, "btn-text").text
		self.driver.implicitly_wait(2.5)

		self.assertEqual(name, auth_check)
		logging.info(f"Произведен вход в аккаунт: {auth_check}")
		self.driver.implicitly_wait(2.5)

#Проверяем надежность пароля в личный кабинет – Тест 9	
	def test_password(self):
		
		url="https://www.rusprofile.ru/"
		name="John"
		email = "fewiyi1850@wuzak.com"
		pwd1 = "t37SvI82"
		pwd2 = "1236F"

		pwd_check_ok="input-text-help has-ok"
		

		self.driver.get(url)
		self.driver.implicitly_wait(5.0)
		#--------------------------------------------

		profile=self.driver.find_element(By.ID, "menu-personal-trigger")
		
		#Выполняем шаги тест-кейса 
		profile.click()
		self.driver.implicitly_wait(200.0)
		reg_btn=self.driver.find_element(By.CLASS_NAME, "vModal-bottom").find_element(By.CLASS_NAME,"btn-link")
		print(reg_btn.text)
		reg_btn.click()
		self.driver.implicitly_wait(2.5)

		pwd_ph=self.driver.find_element(By.XPATH, "//*[@id='v-root']/div/div[1]/div[3]/div[4]/div[1]/input")
		message=self.driver.find_element(By.CLASS_NAME, "input-text-help")
		pwd_ph.send_keys(pwd1)
		self.driver.implicitly_wait(2.5)
		
		attrs=get_attributes(self.driver, message)
		
		self.assertEqual(attrs.get('class'),pwd_check_ok)
		logging.info(f"Пароль {pwd1} проходит проверку 'надежности'")
		pwd_ph.clear()
		pwd_ph.send_keys(pwd2)
		self.driver.implicitly_wait(2.5)
		attrs=get_attributes(self.driver, message)

		self.assertNotEqual(attrs.get('class'),pwd_check_ok)
		logging.info(f"Пароль {pwd2} не проходит проверку 'надежности'")
		

		self.driver.implicitly_wait(2.5)

		



		# if name_flag == 0:
		# 	name_ph=self.driver.find_elements(By.CLASS_NAME, "form-row")
		# 	for elem in name_ph:
		# 		if elem.find_element(By.CLASS_NAME, "control-label-block").text == "Имя":
		# 			name_ph = elem
		# 			name_flag = 1
		# 			break

#Проверяем регистрацию в личный кабинет – Тест 10	
	def test_registrarion(self):
		
		url="https://www.rusprofile.ru/"
		name="John"
		email = "fewiyi1850@wuzak.com"
		pwd = "t37SvI82"
		

		self.driver.get(url)
		self.driver.implicitly_wait(500.0)
		#--------------------------------------------

		profile=self.driver.find_element(By.ID, "menu-personal-trigger")
		
		#Выполняем шаги тест-кейса
		profile.click()
		self.driver.implicitly_wait(200.0)
		reg_btn=self.driver.find_element(By.CLASS_NAME, "vModal-bottom").find_element(By.CLASS_NAME,"btn-link")
		print(reg_btn.text)
		reg_btn.click()
		self.driver.implicitly_wait(2.5)

		name_ph=self.driver.find_element(By.XPATH, "//*[@id='v-root']/div/div[1]/div[3]/div[2]/div/input")
		name_ph.send_keys(name)
		self.driver.implicitly_wait(2.5)

		email_ph=self.driver.find_element(By.XPATH, "//*[@id='v-root']/div/div[1]/div[3]/div[3]/div/input")
		email_ph.send_keys(email)
		self.driver.implicitly_wait(2.5)

		pwd_ph=self.driver.find_element(By.XPATH, "//*[@id='v-root']/div/div[1]/div[3]/div[4]/div[1]/input")
		pwd_ph.send_keys(pwd)
		self.driver.implicitly_wait(2.5)

		# checkbox=self.driver.find_element(By.CLASS_NAME,"checkbox-holder")
		WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.XPATH,"//*[@id='reg_agree']"))).click()
		
		# checkbox=self.driver.find_element(By.XPATH, "//*[@id='v-root']/div/div[1]/div[3]/div[5]")
		# hover = ActionChains(self.driver).move_to_element(checkbox) #имитируем наведение мыши на элемент для отображения кнопки "Скопировать"
		# hover.perform()
		# checkbox.click()
		self.driver.implicitly_wait(2.5)

		pwd_ph=self.driver.find_element(By.XPATH, "//*[@id='v-root']/div/div[1]/div[3]/div[6]/button")

		self.driver.implicitly_wait(2.5)



		# if name_flag == 0:
		# 	name_ph=self.driver.find_elements(By.CLASS_NAME, "form-row")
		# 	for elem in name_ph:
		# 		if elem.find_element(By.CLASS_NAME, "control-label-block").text == "Имя":
		# 			name_ph = elem
		# 			name_flag = 1
		# 			break


def suite():
	suite=unittest.TestSuite()
	# suite.addTest(TestRP('test_search_by_inn'))
	# suite.addTest(TestRP('test_search_by_ogrn'))
	# suite.addTest(TestRP('test_search_by_name'))
	# suite.addTest(TestRP('test_organization_card'))
	# suite.addTest(TestRP('test_egrul'))
	# suite.addTest(TestRP('test_requisites'))
	# suite.addTest(TestRP('test_clipboard'))
	suite.addTest(TestRP('test_auth'))
	# suite.addTest(TestRP('test_password'))
	# suite.addTest(TestRP('test_registration'))
	return suite
		
if __name__ == '__main__':
	# unittest.main()
	runner = unittest.TextTestRunner()
	runner.run(suite())