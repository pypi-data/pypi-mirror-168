from selenium import webdriver
from time import sleep
from os.path import isdir

driver = webdriver.Firefox()
driver.get('http://cnn.com')

prof_temp_dir = driver.capabilities["moz:profile"]
print("CAPS", prof_temp_dir)
sleep(300)
driver.quit()
sleep(3)
print("CAPS", prof_temp_dir, isdir(prof_temp_dir))
