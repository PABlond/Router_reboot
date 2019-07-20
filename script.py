import urllib
import threading
import urllib.request as urllib
from urllib.error import URLError, HTTPError
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time

def setInterval(func,time):
    e = threading.Event()
    while not e.wait(time):
        func()

def append_log_file(message): # add a line to your log file 
    with open("internet_failure.log", "a") as logfile:
        logfile.write(message)

def box_reboot():
    try:
        binary = FirefoxBinary('/usr/bin/firefox') # replace with your firefox binary filepath
        browser = webdriver.Firefox(firefox_binary=binary)
        browser.get('http://192.168.1.1/reboot')
        # fulfill login form and access to the reboot page
        browser \
            .find_element_by_id('login') \
            .send_keys('admin') 
        password = "<PASSWORD>" # replace with your current password
        browser \
            .find_element_by_id('password') \
            .send_keys(password)
        browser \
            .find_element_by_xpath('//button[contains(text(), "Valider")]') \
            .click()
        # reboot the router and cloe the browser
        browser \
            .find_element_by_xpath('//button[contains(text(), "Redémarrer")]') \
            .click()
        browser.quit()

        append_log_file("Internet failure at {} \n" \
                    .format(time \
                        .localtime(time.time()))) 
        # wait until your router was restarted
        time.sleep(300)
    except (HTTPError, URLError) as e:
        print('Your router is not accessible')
    

def check_internet():
    try:
        urllib.urlopen('http://www.google.com')
    except (HTTPError, URLError) as e:
        box_reboot()

if __name__ == '__main__':
    setInterval(check_internet,5)
