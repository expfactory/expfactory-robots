#!/bin/env python

'''
survey.py: plugin to work with expfactory package to generate survey

Copyright (C) 2017 Vanessa Sochat.

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

import argparse
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

    parser.add_argument("--folder", dest='folder', 
                         help="survey folder for the robot to test (default is PWD)", 
                         type=str, default=None)

    return parser

def main():

    parser = get_parser()

    try:
        args = parser.parse_args()
    except:
        sys.exit(0)

    print('Recruiting %s robot!' %args.robot)

    folder = args.folder
    if folder is None:
        folder = os.getcwd()
    folder = os.path.abspath(folder)
    print('[folder] %s' %folder)

    if not os.path.exists(folder):
        bot.error("Cannot find %s, check that path exists." %folder)
        sys.exit(1)

    # The drivers must be on path
    here = os.path.abspath(os.path.dirname(__file__))
    os.environ['PATH'] = "%s/drivers:%s" %(here,os.environ['PATH'])

    # Load the robot!
    if args.robot == 'jspsych':
        from drivers.jspsych import JsPsychRobot as Robot
    elif args.robot == 'survey':
        from drivers.survey import SurveyRobot as Robot

    robot = Robot()
    robot.validate(folder)

if __name__ == '__main__':
    main()    
