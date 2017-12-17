'''

JsPsychRobot to test expfactory experiments created with jspsych

Copyright (C) 2017 Vanessa Sochat.

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

from .base import ExpfactoryRobot
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import UnexpectedAlertPresentException
from expfactory.logger import bot
from time import sleep
import re
import os
import sys


class JsPsychRobot(ExpfactoryRobot):

    def __str__(self):
        return "[expfactory-robot/jspsych]"

    def __repr__(self):
        return "[expfactory-robot/jspsych]"

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


    def get_continue_key(block, block_tag="cont_key"):
        '''get_continue_key for a black, assuming key in jspsych data structure
           is cont_key
        '''
        if not isinstance(block[block_tag],list):
            block[block_tag] = [block[block_tag]]

        # Not specifying a key means "any key"
        if len(block[block_tag]) == 0:
            continue_key = Keys.ENTER

        else:
            continue_key = self.key_lookup(block[block_tag][0])
        return continue_key



    def test_block(self, pause_time=0, wait_time=0):
        '''test_block
           test a single experiment block, given a browser, running experiment, and pause/wait times
      
        Parameters
        ==========  
        pause_time: time to wait between tasks, in addition to time specified in jspsych
        wait_time: initial wait time, or previously generated wait time based on experiment
        '''

        finished = self._isfinished()

        # Pause from the last block
        sleep(float(pause_time)/1000 + wait_time/1000) # convert milliseconds to seconds
        wait_time = 0

        # Get the current trial (not defined on first page)
        block = self.browser.execute_script("return jsPsych.currentTrial();")

        wait_time = wait_time + pause_time

        if "timing_post_trial" in block:
            wait_time = wait_time + block["timing_post_trial"]
        if "timing_feedback_duration" in block:
            wait_time = wait_time + block["timing_feedback_duration"]

        # This is typically for instruction text, etc.
        if "pages" in block and not re.search("survey-multi-choice",block["type"]):
            number_pages = len(block["pages"])
            for p in range(number_pages):
                if "cont_key" in block:
                    continue_key = get_continue_key(block)
                elif "show_clickable_nav" in block:
                    if block["show_clickable_nav"] == True:  
                        try:  
                            self.browser.execute_script("document.querySelector('#jspsych-instructions-next').click();")
                        except WebDriverException as e:
                            pass
                elif 'key_forward' in block:
                    continue_key = key_lookup(block["key_forward"])
                    self.browser.find_element_by_tag_name('html').send_keys(continue_key)
                # Give time for page to reload 
                sleep(1)

        # This is for the experiment
        elif "timeline" in block:
            timeline = block["timeline"]
            for time in timeline:
                if "choices" in block:
                    if len(block["choices"])>0:
                        choices = block["choices"]
                        # Make a random choice
                        random_choice = choice(choices,1)[0]
                        continue_key = key_lookup(random_choice)
                        self.browser.find_element_by_tag_name('html').send_keys(continue_key)
                    elif "button_class" in time:
                        self.browser.execute_script("document.querySelector('.%s').click();" %time["button_class"])
                # Give time for page to reload 
                sleep(1)

        elif "button_class" in block:
            try:
                buttons = browser.find_elements_by_class_name('%s' %block["button_class"])
                button = choice(buttons,1)[0]
                if button.is_enabled() == False:
                    self.browser.execute_script('document.getElementsByClassName("%s")[0].disabled = false' %block["button_class"])
                button.click()
                sleep(0.5)
            except WebDriverException as e:
                pass


        elif "cont_key" in block:
            continue_key = self.get_continue_key(block)
            self.browser.find_element_by_tag_name('html').send_keys(continue_key)

        elif "choices" in block:
            choices = block["choices"]
            if choices != None and len(choices) > 0:
                try:
                    random_choice = choice(choices,1)[0]
                    continue_key = key_lookup(random_choice)
                    self.browser.find_element_by_tag_name('html').send_keys(continue_key)
                except ValueError:
                    bot.log("ValueError, %s found as choices." %(choices))
            else:
                    self.browser.find_element_by_tag_name('html').send_keys(Keys.ENTER)
            if "type" in block:
                if "type" == "writing":
                    self.browser.execute_script("document.querySelector('#jspsych-writing-box').text = 'beep boop';")


        if "type" in block:

            # Multiple choice buttons
            if re.search("survey-multi-choice", block["type"]):
                self._survey_multi_choice()

            # Radio Buttonlist
            elif re.search("radio-buttonlist",block["type"]):
                self._radio_buttonlist()

            # Free text response
            elif re.search("survey-text",block["type"]):
                self._text_response()

        elif "key_answer" in block:
            continue_key = self.get_continue_key(block, block_tag="key_answer")
            self.browser.find_element_by_tag_name('html').send_keys(continue_key)

        elif len(block) == 0:
            self._close_fullscreen()

        return wait_time,finished

    ############################################################################
    # Specific Browser Interactions
    ############################################################################

  
    # Radio Buttons

    def _radio_click(self, div_id, sleep_time=2):
        '''pass through a radio button block given a particular div id.
           used for both radio buttonlist and survey multi choice blocks.
        '''
        try:
            self.browser.execute_script("$(':radio').click();");
            sleep(sleep_time)
            self.browser.execute_script("document.querySelector('#%s').click();" %div_id)
        except WebDriverException as e:
            pass

    def _survey_multi_choice(self):
        ''' complete a survey multi choice block
        '''
        self._radio_click("jspsych-survey-multi-choice-next")


    def _radio_buttonlist(self):
        ''' complete a radio button list
        '''
        self._radio_click("jspsych-radio-buttonlist-next")


    # Text Response

    def _text_response(self):
        '''write something random and submit a text response.
        '''
        try:    
            self.browser.execute_script("document.querySelector('#jspsych-survey-text-next').click();")
        except WebDriverException as e:
             pass

    # Fullscreen

    def _close_fullscreen(self):
        ''' close_fullscreen will check if the jspsych experiment is waiting
            for the user to go fullscreen. If yes, the screen is closed.
        '''
        fullscreen = self.browser.execute_script("return jsPsych.initSettings().fullscreen;")
        if fullscreen is True:
            try:
                self.browser.execute_script("document.querySelector('#jspsych-fullscreen-btn').click();")
            except WebDriverException as e:
                pass

    # Progress
    def _isfinished(self):
        '''determine if the experiment is finished based on percent complete.
        '''
        percent_complete = self.browser.execute_script("return jsPsych.progress().percent_complete;")
        if percent_complete == 100:
            return True
        return False
        

    def key_lookup(self, keyid):
        lookup = {13:Keys.ENTER,
                  8:Keys.BACKSPACE,
                  9:Keys.TAB,
                  16:Keys.SHIFT,
                  17:Keys.CONTROL,
                  18:Keys.ALT,
                  19:Keys.PAUSE,
                  27:Keys.ESCAPE,
                  32:Keys.SPACE,
                  33:Keys.PAGE_UP,
                  34:Keys.PAGE_DOWN,
                  35:Keys.END,
                  36:Keys.HOME,
                  37:Keys.LEFT,
                  38:Keys.UP,
                  39:Keys.RIGHT,
                  40:Keys.DOWN,
                  45:Keys.INSERT,
                  46:Keys.DELETE,
                  48:"0",
                  49:"1",
                  50:"2",
                  51:"3",
                  52:"4",
                  53:"5",
                  54:"6",
                  55:"7",
                  56:"8",
                  57:"9",
                  65:"a",
                  66:"b",
                  67:"c",
                  68:"d",
                  69:"e",
                  70:"f",
                  71:"g",
                  72:"h",
                  73:"i",
                  74:"j",
                  75:"k",
                  76:"l",
                  77:"m",
                  78:"n",
                  79:"o",
                  80:"p",
                  81:"q",
                  82:"r",
                  83:"s",
                  84:"t",
                  85:"u",
                  86:"v",
                  87:"w",
                  88:"x",
                  89:"y",
                  90:"z",
                  96:Keys.NUMPAD0,
                  97:Keys.NUMPAD1,
                  98:Keys.NUMPAD2,
                  99:Keys.NUMPAD3,
                  100:Keys.NUMPAD4,
                  101:Keys.NUMPAD5,
                  102:Keys.NUMPAD6,
                  103:Keys.NUMPAD7,
                  104:Keys.NUMPAD8,
                  105:Keys.NUMPAD8,
                  106:Keys.MULTIPLY,
                  107:Keys.ADD,
                  109:Keys.SUBTRACT,
                  110:Keys.DECIMAL,
                  111:Keys.DIVIDE,
                  112:Keys.F1,
                  113:Keys.F2,
                  114:Keys.F3,
                  115:Keys.F4,
                  116:Keys.F5,
                  117:Keys.F6,
                  118:Keys.F7,
                  119:Keys.F8,
                  120:Keys.F9,
                  121:Keys.F10,
                  122:Keys.F11,
                  123:Keys.F12,
                  186:Keys.SEMICOLON,
                  187:Keys.EQUALS,
                  "leftarrow":Keys.LEFT,
                  "rightarrow":Keys.RIGHT,
                  "uparrow":Keys.UP,
                  "downarrow":Keys.DOWN}
        if keyid not in lookup:
            if isinstance(keyid,str) or isinstance(keyid,unicode):
                return str(keyid.lower())
        return lookup[keyid]
