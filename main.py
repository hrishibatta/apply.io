from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import time
import re
import json
import sys

class EasyApplyLinkedin:

    def __init__(self, data):
        """Parameter initialization"""

        self.email = data['email']
        self.password = data['password']
        self.keywords = data['keywords']
        self.location = data['location']

        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def login_linkedin(self):
        """This function logs into your personal LinkedIn profile"""

        # go to the LinkedIn login url
        self.driver.get("https://www.linkedin.com/login")

        # introduce email and password and hit enter
        login_email = self.driver.find_element_by_name('session_key')
        login_email.clear()
        login_email.send_keys(self.email)
        login_pass = self.driver.find_element_by_name('session_password')
        login_pass.clear()
        login_pass.send_keys(self.password)
        login_pass.send_keys(Keys.RETURN)

    def url_generator(self):
        """Generates url for LinkedIn job search with location and job title"""
        base = "https://www.linkedin.com/jobs/search/?keywords="
        keywords = self.keywords.replace(" ","%20")+"&location="
        location = self.location.replace(" ","%20")

        if self.location:
            location = self.location.replace(" ","%20")+"%2C%20"
            url = base+keywords+location+"&start=30"
        else:
            url = base + keywords + location + "&start=30"

        self.driver.get(url)

    def filter(self):
        """This function filters all the job results by 'Easy Apply'"""

        # select all filters, click on Easy Apply and apply the filter
        time.sleep(2)

        move = self.driver.find_element_by_xpath("(//button[@class='peek-carousel-controls__button'])[2]")
        move.click()

        easy_apply_button = self.driver.find_element_by_xpath("//button[@aria-label='Easy Apply filter.' and @class='artdeco-pill artdeco-pill--slate artdeco-pill--2 artdeco-pill--choice ember-view search-reusables__filter-pill-button']")
        easy_apply_button.click()

    def applyToJobs(self):
        """This function applies to the jobs"""

        pane = self.driver.find_element_by_class_name("jobs-search-results")

        # start from your target element, here for example, "header"
        all_li = pane.find_elements_by_tag_name("li")
        for li in all_li:
            ### Loop through the job postings and press the whitelink, changing current job view
            print(li)

        sys.exit(1)


        self.quickApplyButton()
        time.sleep(5)
        self.nextButton()
        time.sleep(5)
        self.reviewButton()
        time.sleep(5)
        self.submitApplication()

    def quickApplyButton(self):
        try:
            QuickApply = self.driver.find_element_by_xpath("//button[@class='jobs-apply-button artdeco-button artdeco-button--3 artdeco-button--primary ember-view']")
            QuickApply.click()
        except:
            pass

    def nextButton(self):
        try:
            nextButton = self.driver.find_element_by_xpath("//button[@aria-label='Continue to next step' and @class='artdeco-button artdeco-button--2 artdeco-button--primary ember-view']")
            nextButton.click()
        except:
            pass

    def reviewButton(self):
        try:
            review = self.driver.find_element_by_xpath("//button[@aria-label='Review your application' and @class='artdeco-button artdeco-button--2 artdeco-button--primary ember-view']")
            review.click()
        except:
            pass

    def submitApplication(self):
        try:
            submitApplication = self.driver.find_element_by_xpath("//button[@aria-label='Submit application' and @class='artdeco-button artdeco-button--2 artdeco-button--primary ember-view']")
            submitApplication.click()

            exit = self.driver.find_element_by_xpath("//button[@aria-label='Dismiss' and @class='artdeco-modal__dismiss artdeco-button artdeco-button--circle artdeco-button--muted artdeco-button--2 artdeco-button--tertiary ember-view']")
            exit.click()

        except:
            pass

    def close_session(self):
        """This function closes the actual session"""
        self.driver.close()

    def apply(self):
        """Apply to job offers"""

        self.driver.maximize_window()
        self.login_linkedin()
        time.sleep(2)
        self.url_generator()
        time.sleep(2)
        self.filter()
        time.sleep(2)

        self.applyToJobs()
        time.sleep(2)
        #self.close_session()


if __name__ == '__main__':

    with open('data.json') as config_file:
        data = json.load(config_file)

    bot = EasyApplyLinkedin(data)
    bot.apply()
