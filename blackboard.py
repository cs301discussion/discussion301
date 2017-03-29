#!/usr/bin/env python3

import urllib, os, time, sys

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import common, google

BASE_URL    = "https://mycourses.binghamton.edu"
COURSE_TEXT = 'CS-301-91'
BB_USERNAME = 'dmcneil2'
BB_PWD_ENV  = 'BBPASS'

COURSE_LIST_ID  = 'div_3_1'
#COURSE_LIST_ID  = '_3_1termCourses_noterm'

# For easily grabbing the content iFrame
def getContentFrame(driver):
    # Selenium doesn't know when an iframe is loaded, so we need to wait
    main_iframe = driver.find_element_by_id('contentFrame')
    driver.switch_to.frame(main_iframe)

def parseDiscussion(driver):
    table = driver.find_element_by_id("listContainer_databody")
    rows = table.find_elements_by_tag_name("tr")
    total = dict((s, [0,0]) for s in common.STUDENTS)
    extras = []
    for i, row in enumerate(rows):
        extras.append(row.find_element_by_tag_name('a').get_attribute('href'))

    for link in extras:
        driver.get(link)
        responses = driver.find_elements_by_class_name('msg-nexus')
        for p in responses:
            name = p.find_element_by_class_name('profileCardAvatarThumb')
            cont = p.find_element_by_class_name('dbThreadBody')
            total[name.text][0] += 1
            total[name.text][1] += len(cont.text.split())
    return total

def getDiscussionPage(discpost):

    driver = webdriver.PhantomJS()

    # Can use a normal browser like firefox if PhantomJS 
    # not working
    # driver = webdriver.Firefox()

    # Tells the browser to wait a certain amount of time before
    # throwing an error if an element does not appear
    driver.implicitly_wait(10)

    # Load the main page
    driver.get(BASE_URL)

    # Find the login form
    username = driver.find_element_by_id("username")
    password = driver.find_element_by_id("password") 

    # Enter form information
    username.send_keys(BB_USERNAME)
    password.send_keys(os.environ[BB_PWD_ENV])
    username.send_keys(Keys.ENTER)
    driver.save_screenshot('scrot.png')

    # Get the course listing div
    course_listings = driver.find_element_by_id(COURSE_LIST_ID)
    # Get link for the desired course
    course_link     = course_listings.find_element_by_partial_link_text(COURSE_TEXT)

    # Go to that page
    course_link.click()

    # Iterate over the desired discussion posts to be checked
    for post in discpost:
        # Go to the discussions page for that course
        driver.find_element_by_link_text('Discussions').click()

        # Find the discussion post index
        index = common.DISCUSSIONS[post]

        # Check that we are on the right discussion page
        page = int(driver.find_element_by_class_name('currentPage').text)
        if index > 24 and page == 1: 
            driver.find_element_by_id("listContainer_nextpage_top").click()
            index = index % 25
        elif index <= 24 and page == 2:
            driver.find_element_by_id("listContainer_prevpage_top").click()

        discuss = driver.find_element_by_id("listContainer_databody")
        rows = discuss.find_elements_by_tag_name("tr")
        link = rows[index].find_element_by_link_text(post)
        link.click()
        total = parseDiscussion(driver)
        google.insertData(total, post)
    driver.quit()

if __name__ == '__main__':
    if len(sys.argv) < 2: 
        print("Enter one or more discussion post numbers\n")
        sys.exit(1)
    sess = sys.argv[1:]
    getDiscussionPage(sess)
