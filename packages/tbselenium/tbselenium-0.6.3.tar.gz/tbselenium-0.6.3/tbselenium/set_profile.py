import tempfile

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from time import sleep
from os.path import isdir
profile = tempfile.mkdtemp("firefox-profile")

options = Options()
options.binary = "/usr/bin/firefox"
options.log.level = "trace"
# options.add_argument("-profile")
# options.add_argument(profile)
options.profile = profile

options.set_preference("browser.startup.page", "https://example.com")
options.set_preference("browser.startup.homepage", "https://example.com")
options.set_preference("browser.startup.firstrunSkipsHomepage", "false")
# , service_args=["--marionette-port", "2828"]
driver = webdriver.Firefox(options=options)
sleep(3)
driver.get('http://cnn.com')

prof_temp_dir = driver.capabilities["moz:profile"]
print("CAPS", prof_temp_dir)
print("profile", profile)
sleep(30)
driver.quit()
sleep(3)
print("CAPS", prof_temp_dir, isdir(prof_temp_dir))
print("profile", profile, isdir(profile))

