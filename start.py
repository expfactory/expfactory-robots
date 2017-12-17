#!/bin/env python

'''
survey.py: plugin to work with expfactory package to generate survey

Copyright (C) 2017 Vanessa Sochat.

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

import argparse
from expfactory.logger import bot
import sys
import os

## MAIN ########################################################################

def get_parser():

    parser = argparse.ArgumentParser(
    description="expfactory: generate survey from config.json and question file")

    parser.add_argument("--robot",'-r', dest='robot', 
                        choices=['survey', 'jspsych'],
                        help="the survey robot to recruit!",
                        type=str, default="jspsych")

    parser.add_argument("--port",'-p', dest='port', 
                        help="port to run webserver",
                        type=int, default=None)

    parser.add_argument("--browser",'-b', dest='browser', 
                        choices=['Firefox', 'Chrome'],
                        help="browser driver to use for the robot",
                        type=str, default="Chrome")

    parser.add_argument('folders', nargs="+",
                        help='experiments for robot testing')

    return parser

def main():

    parser = get_parser()

    try:
        args = parser.parse_args()
    except:
        sys.exit(0)

    print('Recruiting %s robot!' %args.robot)

    folders = args.folders
    if len(folders) == 0:
        folders = [os.getcwd()]

    # The drivers must be on path
    here = os.path.abspath(os.path.dirname(__file__))
    os.environ['PATH'] = "%s/drivers:%s" %(here,os.environ['PATH'])

    # Load the robot!
    if args.robot == 'jspsych':
        from drivers.jspsych import JsPsychRobot as Robot
    elif args.robot == 'survey':
        from drivers.survey import SurveyRobot as Robot

    robot = Robot(browser=args.browser, port=args.port)
    for folder in folders:
        folder = os.path.abspath(folder)

        if not os.path.exists(folder):
            bot.error("Cannot find %s, check that path exists." %folder)
        else:   
            print('[folder] %s' %folder)
            robot.validate(folder)

    # Clean up shop!
    robot.stop()

if __name__ == '__main__':
    main()    
