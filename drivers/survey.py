'''
survey.py: plugin to work with expfactory package to generate survey

Copyright (C) 2017 Vanessa Sochat.

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

from .base import ExpfactoryRobot
from selenium.common.exceptions import UnexpectedAlertPresentException

class SurveyRobot(ExpfactoryRobot):

    def __str__(self):
        return "[expfactory-robot/survey]"        

    def __repr__(self):
        return "[expfactory-robot/survey]"   

    def _validate(self, folder):
        ''''validate is subclass specific function to validate a survey.
            it is called by ExpfactoryRobot in primary function "validate"
        '''
        if self.started is False:
            self.get_server()

        base = os.path.abspath(folder)

        # Set up a web browser
        os.chdir(base)
        self.get_browser()
        self.browser.implicitly_wait(3) # if error, will wait 3 seconds and retry
        self.browser.set_page_load_timeout(10)

        bot.log("STARTING TEST OF SURVEY")
        self.get_page("http://localhost:%s" %self.port)

        sleep(3)

        count=1
        while True:
            bot.log("Testing page %s" %count)
            try:
                finished = self.advance_survey()
                if finished is True:
                    break
                count+=1
            except UnexpectedAlertPresentException:
                bot.log("Found alert: closing.")
                try:
                    alert = browser.switch_to_alert()
                    alert.accept()
                except:
                    pass

        bot.log("FINISHING TEST OF SURVEY")

    # Stop the server
    self.httpd.server_close()

    def advance_survey(self):
        '''click the next button and fill in current page question content / questions
        '''

        # Click all checkboxes and radio buttons
        self.browser.execute_script('$(":radio").click();')
        self.browser.execute_script('$(":checkbox").click();')

        # If there are text boxes on the page, fill them (numeric and regular)
        textfields = self.browser.execute_script('var elements = []; var tmp = $(".mdl-textfield__input"); $.each(tmp,function(i,e){elements.push(e)}); return elements;')
        for text in textfields:
            element_id = text.get_attribute('id')
            textbox_type = text.get_attribute('type')
            if textbox_type == "number":
                fill_input = str('$("input[id=%s]").val(711);' %(element_id))
            elif textbox_type == 'text':
                fill_input = str('$("input[id=%s]").val("beep boop!");' %(element_id))
            self.browser.execute_script(fill_input)
    
        # Click the forward button, click it
        forward = self.browser.find_element_by_class_name('forward').click()
    
        # Have we reached the end?
        finished = self.browser.execute_script("return expfactory_finished;")
        return finished
