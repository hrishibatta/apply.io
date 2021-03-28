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

        self.jsonOutput = {}
        self.applicationNumber = 0

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

        try:
            move = self.driver.find_element_by_xpath("(//button[@class='peek-carousel-controls__button'])[2]")
            move.click()
        except:
            pass

        easy_apply_button = self.driver.find_element_by_xpath("//button[@aria-label='Easy Apply filter.' and @class='artdeco-pill artdeco-pill--slate artdeco-pill--2 artdeco-pill--choice ember-view search-reusables__filter-pill-button']")
        easy_apply_button.click()

    def applyToJobs(self):
        """This function applies to the jobs"""

        pane = self.driver.find_element_by_class_name("jobs-search-results__list")

        # start from your target element, here for example, "header"
        all_li = pane.find_elements_by_tag_name("li")

        for li in all_li:
            print(len(li.text))
            if len(li.text) > 60:

                ### Loop through the job postings and press the whitelink, changing current job view
                try:
                    li.click()
                except:
                    try:
                        while (True):
                            noti = self.driver.find_element_by_xpath("//button[@class='artdeco-toast-item__dismiss artdeco-button artdeco-button--circle artdeco-button--muted artdeco-button--1 artdeco-button--tertiary ember-view']")
                            noti.click()
                            time.sleep(.5)
                    except:
                        time.sleep(.5)
                        li.click()

                print("moved")

                time.sleep(1)
                self.quickApplyButton()
                print("quick APplied")
                time.sleep(2)

                if self.checkEasy():
                    self.nextButton()
                    time.sleep(1)

                    if self.checkEasy():
                        self.reviewButton()
                        time.sleep(1)


                        self.submitApplication()
                        self.jobInfo()
                        print(self.jsonOutput)

                    else:

                        self.abort()



                else:
                    self.abort()










        with open('dataOutput.json', 'w') as outfile:
            json.dump(self.jsonOutput, outfile)
        print(self.applicationNumber)



    def jobInfo(self):
        try:
            jobtitle = self.driver.find_element_by_class_name("jobs-details-top-card__job-title").text

            company = self.driver.find_element_by_class_name("jobs-details-top-card__company-url").text

            if jobtitle not in self.jsonOutput or self.jsonOutput[jobtitle] != company:

                self.jsonOutput[jobtitle] = company
                self.applicationNumber += 1

        except:
            pass

    def abort(self):
        cancel = self.driver.find_element_by_xpath("//button[@aria-label='Dismiss' and @class='artdeco-modal__dismiss artdeco-button artdeco-button--circle artdeco-button--muted artdeco-button--2 artdeco-button--tertiary ember-view']")
        cancel.click()

        time.sleep(1)
        dismiss = self.driver.find_element_by_xpath("//button[@class='artdeco-modal__confirm-dialog-btn artdeco-button artdeco-button--2 artdeco-button--primary ember-view']")
        dismiss.click()


    def checkEasy(self):
        try:
            #QuickApply = self.driver.find_element_by_xpath("//input[@class='ember-text-field ember-view fb-single-line-text__input']")
            type = self.driver.find_element_by_xpath("//h3[@class='t-16 t-bold']").text

            if type == "Additional Questions" or type == "Home address" or type == "Additional" or type == "Voluntary self identification":
                return False
            return True
        except:
            return True


    def quickApplyButton(self):
        try:
            QuickApply = self.driver.find_element_by_xpath("//button[@class='jobs-apply-button artdeco-button artdeco-button--3 artdeco-button--primary ember-view']")
            QuickApply.click()
        except:
            pass

    def nextButton(self):
        try:
            i = 0
            while(True):
                nextButton = self.driver.find_element_by_xpath("//button[@aria-label='Continue to next step' and @class='artdeco-button artdeco-button--2 artdeco-button--primary ember-view']")
                nextButton.click()
                i += 1
                if i > 5:
                    break
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

            time.sleep(2)
            exit = self.driver.find_element_by_xpath("//button[@aria-label='Dismiss']")
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
