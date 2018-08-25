'''

LabJSRobot to test experiments created with labjs

Copyright (C) 2018 Vanessa Sochat.

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

from .base import ExpfactoryRobot
from selenium.webdriver.common.keys import Keys

from selenium.common.exceptions import (
    WebDriverException, 
    UnexpectedAlertPresentException, 
    NoSuchElementException,
    TimeoutException
)

from expfactory.logger import bot
from random import choice
from time import sleep
import re
import os
import sys


class LabJSRobot(ExpfactoryRobot):

    def __str__(self):
        return "[expfactory-robot/labjs]"

    def __repr__(self):
        return "[expfactory-robot/labjs]"

    def _validate(self, folder):
        ''''validate is subclass specific function to validate a survey.
            it is called by ExpfactoryRobot in primary function "validate"
        '''
        base = os.path.abspath(folder)

        # Set up a web browser
        os.chdir(base)
        self.get_browser()
        self.browser.implicitly_wait(3) # if error, will wait 3 seconds and retry
        self.browser.set_page_load_timeout(10)

        bot.log("STARTING TEST OF EXPERIMENT")
        self.get_page("http://localhost:%s/" %self.port)

        sleep(3)

        while True:
            try:
                wait_time,finished = self.test_block()
                if finished is True:
                    break
            except UnexpectedAlertPresentException:
                bot.log("Found alert: closing.")
                try:
                    alert = self.browser.switch_to_alert()
                    alert.accept()
                except:
                    pass

        bot.log("FINISHING TEST OF EXPERIMENT")


    def test_block(self, pause_time=0, wait_time=0):
        '''test_block
           test a single experiment block, given a browser, 
           running experiment, and pause/wait times
      
           Parameters
           ==========  
           pause_time: time to wait between tasks, in addition to time specified in jspsych
           wait_time: initial wait time, or previously generated wait time based on experiment
        '''

        #TODO: write how to test a block here...

        return wait_time



    ############################################################################
    # Specific Browser Interactions
    ############################################################################

  
    # Text Response

    def _text_response(self):
        '''write something random and submit a text response.
        '''
        try:    
            self.browser.execute_script("document.querySelector('#jspsych-survey-text-next').click();")
        except WebDriverException as e:
             pass


    # Buttons

    def _buttons_click(self, block):
        '''find and undisable buttons, and click them.
        '''
        try:
            buttons = browser.find_elements_by_class_name('%s' %block["button_class"])
            button = choice(buttons,1)[0]
            if button.is_enabled() is False:
                self.browser.execute_script('document.getElementsByClassName("%s")[0].disabled = false' %block["button_class"])
            button.click()
            sleep(0.5)
        except WebDriverException as e:
            pass


    def _forward_timeline(self, block):
        '''detect and move forward through a timeline
        '''
        # TODO: write me
