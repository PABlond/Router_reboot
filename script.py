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

def append_log_file(): # add a line to your log file 
    with open("internet_failure.log", "a") as myfile:
        myfile \
            .write("reboot at {} \n" \
                .format(time \
                    .localtime(time.time())))

def box_reboot():
    password = <PASSWORD> # replace with your current password
    binary = FirefoxBinary('/usr/bin/firefox') # replace with your firefox binary filepath
    browser = webdriver.Firefox(firefox_binary=binary)
    browser.get('http://192.168.1.1/reboot')
    elem_login = browser.find_element_by_id('login')  
    elem_password = browser.find_element_by_id('password')  
    elem_login.send_keys('admin')
    elem_password.send_keys(password)
    browser.find_element_by_xpath('//button[contains(text(), "Valider")]').click()
    elem_reboot = browser.find_element_by_xpath('//button[contains(text(), "Redémarrer")]')
    elem_reboot.click()
    browser.quit()  
    append_log_file()  
    time.sleep(300)

def check_internet():
    try:
        urllib.urlopen('http://www.google.com')
    except HTTPError as e:
        box_reboot()
    except URLError as e:
        box_reboot()

setInterval(check_internet,5)