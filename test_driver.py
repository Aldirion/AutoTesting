from selenium import webdriver
import logging
from selenium.webdriver.common.by import By

def test_driver_connection():
	driver = webdriver.Chrome()

	driver.get("https://www.selenium.dev/selenium/web/web-form.html")

	title = driver.title

	driver.implicitly_wait(0.5)

	text_box = driver.find_element(by=By.NAME, value="my-text")
	submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")

	text_box.send_keys("Selenium")
	submit_button.click()

	message = driver.find_element(by=By.ID, value="message")
	text = message.text

	driver.quit()

def test_eight_components():
    driver = webdriver.Chrome()

    driver.get("https://www.selenium.dev/selenium/web/web-form.html")

    title = driver.title
    assert title == "Web form"

    driver.implicitly_wait(0.5)

    text_box = driver.find_element(by=By.NAME, value="my-text")
    submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")

    text_box.send_keys("Selenium")
    submit_button.click()

    message = driver.find_element(by=By.ID, value="message")
    value = message.text
    assert value == "Received!"

    driver.quit()
    
def main():
    #   test_driver_connection()
      test_eight_components()
      


main()	  