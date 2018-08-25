'''
survey.py: plugin to work with expfactory package to generate survey

Copyright (C) 2017 Vanessa Sochat.

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

from selenium.common.exceptions import TimeoutException
from expfactory.validator import ExperimentValidator
from expfactory.logger import bot

from selenium.webdriver.common.keys import Keys
from random import choice
from threading import Thread
from selenium import webdriver
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
import webbrowser
import json
import shutil
import re
import sys
import os


class ExpfactoryServer(SimpleHTTPRequestHandler):
    '''here we subclass SimpleHTTPServer to capture error messages
    '''
    def log_message(self, format, *args):
        '''log to standard error with a date time string,
            and then call any subclass specific logging functions
        '''
        sys.stderr.write("%s - - [%s] %s\n" %
                     (self.address_string(),
                      self.log_date_time_string(),
                      format%args))

        # Workaround for error trying to GET html
        if not re.search("div",format%args) and not re.search("function",format%args):
            if re.search("404",format%args):
                raise IOError(format%args)

    def log_error(self, format, *args):
        '''log_error
        catch errors in the log_messages instead
        '''
        pass



class ExpfactoryRobot(object):
    ''' bring up a server with a custom robot
        
        Defaults
        ==========

        pause_time: time to wait between browser commands
        port: a random choice between 8000 and 9999
    '''
  
    def __init__(self, **kwargs):
        self.Handler = ExpfactoryServer
        if "port" in kwargs:
            self.port = kwargs['port']
        else:       
            self.port = choice(range(8000,9999))
        bot.debug('Selected port is %s' %self.port)
        self.httpd = TCPServer(("", self.port), self.Handler)
        self.server = Thread(target=self.httpd.serve_forever)
        self.server.setDaemon(True)
        self.server.start()
        self.started = True
        self.pause_time = 100
        self.browser = None
        self.headless = False
        self.display = None
        self.driver = "Chrome"
        if "browser" in kwargs:
            self.driver = kwargs['browser']


    def validate(self, folder):
        '''validate is the first entrypoint function for running an experiment
           or survey robot. It ensures that the content is valid,
           and then calls _validate (should be defined in subclass)'''
            
        validator = ExperimentValidator()
        valid = validator.validate(folder)

        if valid is True:

            # IF missing favicon, add
            self._check_favicon(folder)

            valid = self._validate(folder)
            bot.log("[done] stopping web server...")
            self.httpd.server_close()
        else:
            bot.warning('%s is not valid, skipping robot testing.' %folder)


    def _validate(self, folder=None):
        '''_validate is required to be implemented in the subclass
        '''
        raise NotImplementedError


    def _check_favicon(self, folder):
        '''add the expfactory favicon if the user doesn't already have one.
        '''
        here = "%s/favicon.ico" %os.path.abspath(os.path.dirname(__file__))
        there = '%s/favicon.ico' %folder
        if not os.path.exists(there):
            shutil.copyfile(here, there)

    def check_errors(self):
   
        if self.browser is not None:
            # Look at log from last call
            log = self.browser.get_log("browser")
            for log_entry in log:
                assert_equal(log_entry["level"] in ["WARNING","INFO"],True)


    def get_browser(self,name=None):
        '''get_browser 
           return a browser if it hasn't been initialized yet
        '''
        if name is None:
            name=self.driver

        service_log_path = "%s-driver.log" %name.lower()
        if self.browser is None:
            if name.lower() == "Firefox":
                self.browser = webdriver.Firefox(service_log_path=service_log_path)
            else:
                self.browser = webdriver.Chrome(service_log_path=service_log_path)
        return self.browser

    
    def get_page(self, url, name='Chrome'):
        '''get_page
            open a particular url, checking for Timeout
        '''
        if self.browser is None:
            self.browser = self.get_browser(name)

        try:
            return self.browser.get(url)
        except TimeoutException:
            bot.error('Browser request timeout. Are you connected to the internet?')
            self.browser.close()
            sys.exit(1)

    def stop(self):
        '''close any running browser or server, and shut down the robot
        '''
        if self.browser is not None:
            self.browser.close()
        self.httpd.server_close() 

        if self.display is not None:
            self.display.close()


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
            self.browser.execute_script("document.querySelector('#%s').click();" % div_id)
        except WebDriverException as e:
            pass


    # JavaScript

    def run_javascript(browser,code):
        if self.browser is not None:
            return browser.execute_script(code)



    ############################################################################
    # Keys
    ############################################################################


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
