from os.path import join
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

from tbselenium.tbdriver import TorBrowserDriver
from tbselenium import common as cm
from time import sleep


TBB_PATH = "/home/gacar/apps/tbb/11.0.1-test/tor-browser_en-US/"
tbb_profile_path = join(TBB_PATH, cm.DEFAULT_TBB_PROFILE_PATH)
fx_binary = join(TBB_PATH, cm.DEFAULT_TBB_FX_BINARY_PATH)


def visit(tbb_dir):
    url = "https://check.torproject.org"
    with TorBrowserDriver(tbb_dir) as driver:
        driver.load_url(url)
        # Iterate over a bunch of locales from the drop-down menu
        for lang_code in ["en_US", "fr", "zh_CN", "th", "tr"]:
            select = Select(driver.find_element(By.ID, "cl"))
            select.select_by_value(lang_code)
            print("\n======== Locale: %s ========" % lang_code)
            print(driver.find_element_by("h1.on").text)  # status text
            print(driver.find_element_by(".content > p").text)  # IP address
        print("Finished visiting %s" % url)
        sleep(100)


def test():

    opts = Options()
    opts.add_argument("-profile")
    opts.add_argument(tbb_profile_path)
    opts.binary = fx_binary
    # , options=opts
    with TorBrowserDriver(TBB_PATH, tor_cfg=cm.USE_RUNNING_TOR, options=opts) as driver:
        driver.load_url('https://check.torproject.org')
        print("Finished visiting")


if __name__ == "__main__":
    test()
    # visit(TBB_PATH)
