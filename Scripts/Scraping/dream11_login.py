# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 14:16:27 2020

@author: nxf55806
"""

import operator
import re
import time
import traceback
from base64 import b64decode
from collections import OrderedDict
from selenium.common.exceptions import WebDriverException
from utils.config import Config
from utils.get_logger import Logger
from utils.config import NoSuchElementException
from utils.config import StaleElementReferenceException
from copy import deepcopy
from utils.database import Database


class Dream11(object):
    def __init__(self):
        self.driver = None
        self.obj = Config()
        self.logger = Logger.get_console_logger()
        self.file_logger = Logger.get_file_logger()
        self.espn_list = list()

    def get_data(self, ipl=True, driver_name = 'phantom'):
        try:
            self.file_logger.info(
                "********************************************************************************")
            result_dict = dict()
            vcap = set()
            cap = set()
            self.logger.info("Initializing driver")
            self.driver = self.obj.get_driver_instance(driver_name)
            self.logger.info("Initialized driver...")
            # Get team data from espn
            if ipl:
                self.get_espn_data()
            self.logger.info("Navigating to dream11 homepage...")
            self.driver.get(self.obj.get_xpath("Target_URL"))
            self.logger.info("Entering username")
            self.obj.send_keys(self.driver, self.obj.get_xpath("Username_input"),
                               self.obj.get_xpath(
                                   "Username"))
            self.logger.info("Entering password")
            self.obj.send_keys(self.driver, self.obj.get_xpath("Password_input"), b64decode(
                self.obj.get_xpath("Password")))
            self.logger.info("Clicking on login")
            self.obj.click_element(self.driver, self.obj.get_xpath("Login_btn"))
            try:
                # Get total teams
                self.logger.info("Selecting match")
                self.obj.click_element(self.driver, self.obj.get_xpath("Match_selector"))
                time.sleep(3)
                self.logger.info("Getting total teams")
                total_teams = self.obj.wait_for_elements(self.driver, self.obj.get_xpath(
                    "Total_teams"))
                for each_team in total_teams:
                    self.logger.info("Clicking on teams")
                    self.obj.click_element(self.driver, self.obj.get_xpath("Team_select"))
                    each_team.click()
                    time.sleep(3)
                    total_players = self.obj.wait_for_elements(self.driver, self.obj.get_xpath(
                        "Total_players"))
                    for each_player in total_players:
                        player_name = each_player.get_attribute('title')
                        try:
                            each_player.find_element_by_xpath(".//span[@class='vCapIco']")
                            vcap.add(player_name)
                        except (NoSuchElementException, StaleElementReferenceException):
                            pass
                        try:
                            each_player.find_element_by_xpath(".//span[@class='capIco']")
                            cap.add(player_name)
                        except (NoSuchElementException, StaleElementReferenceException):
                            pass
                        if player_name not in result_dict:
                            result_dict[player_name] = 1
                        else:
                            result_dict[player_name] += 1
               # temp = sorted(result_dict.items(), key=operator.itemgetter(1))
                temp = sorted(result_dict.items(), key=operator.itemgetter(0))
                # temp.reverse()
                temp = OrderedDict(temp)
                for key, value in enumerate(temp.iteritems()):
                    self.logger.info("{0} : {1} - {2}".format(key + 1, value[0], value[1]))
                    self.file_logger.info("{0} : {1} - {2}".format(key + 1, value[0], value[1]))
                self.logger.info("**** Captain ****")
                self.file_logger.info("**** Captain ****")
                for each_cap in cap:
                    x = result_dict[each_cap]
                    if x > 1:
                        self.logger.info("{0} is a Captain and put {1} times ".format(each_cap, x))
                        self.file_logger.info("{0} is a Captain and put {1} times ".format(each_cap, x))
                self.logger.info("**** Vice-Captain ****")
                self.file_logger.info("**** Vice-Captain ****")
                for each_vcap in vcap:
                    x = result_dict[each_vcap]
                    if x > 2:
                        self.logger.info("{0} is a Vice-Captain and put {1} times ".format(each_vcap, x))
                        self.file_logger.info("{0} is a Vice-Captain and put {1} times ".format(each_vcap, x))
                if ipl:
                    diff = set(self.espn_list) - set(result_dict.keys())
                    self.logger.info("Players in ESPN List but not in Dream11 {}".format(diff))
                    self.file_logger.info("Players in ESPN List but not in Dream11 {}".format(diff))
                    diff = set(result_dict.keys()) - set(self.espn_list)
                    self.logger.info("Players in Dream11 not in ESPN List {}".format(diff))
                    self.file_logger.info("Players in Dream11 not in ESPN List {}".format(diff))
            except Exception:
                self.logger.info("Exception Occurred... writing to the log file")
                self.file_logger.debug(traceback.format_exc())
            finally:
                # Logout
                self.logger.info("Logging out...")
                self.obj.click_element(self.driver, self.obj.get_xpath("Team_section"))
                self.obj.click_element(self.driver, self.obj.get_xpath("Logout_btn"))

        except WebDriverException:
            self.logger.info("Exception Occurred... writing to the log file")
            self.file_logger.debug(traceback.format_exc())
        finally:
            if self.driver:
                self.driver.quit()
            else:
                print("Driver not initialized")

    def get_espn_data(self):
        try:
            database_obj = Database()
            link = self.obj.get_xpath("Preview_link")
            teams = database_obj.get_teams_from_db(link)
            if teams:
                import json
                self.espn_list.extend(json.loads(teams[0][0]))
                self.espn_list.extend(json.loads(teams[0][1]))
                return
            self.logger.info("Opening espn news page...")
            self.driver.get(link)
            team1 = self.obj.get_text_from_element(self.obj.wait_for_element(self.driver,
                                                                                  self.obj.get_xpath("Team1")))
            team2 = self.obj.get_text_from_element(self.obj.wait_for_element(self.driver,
                                                                                  self.obj.get_xpath(
                                                                                      "Team2")))
            self.logger.info("Getting team names...")
            team_name1 = self.obj.get_text_from_element(self.obj.wait_for_element(self.driver,
                                                                                  self.obj.get_xpath("Team1")+"/b"))
            team_name2 = self.obj.get_text_from_element(self.obj.wait_for_element(self.driver,
                                                                                  self.obj.get_xpath(
                                                                                      "Team2") + "/b"))
            self.logger.info("Formatting the text...")
            team1 = "".join(team1.split(team_name1)).strip(":").strip()
            team2 = "".join(team2.split(team_name2)).strip(":").strip()

            is_change_needed = False
            if is_change_needed:
                with open('/tmp/dream11.txt', 'w') as f:
                    f.truncate()
                with open('/tmp/dream11.txt', 'a') as f:
                    f.write(team1 + '\n')
                    f.write(team2 + '\n')
                # Since we can't rely upon espn cricnfo, it might have text formatting
                # issues, writing to a txt file, verify it, then continue
                import ipdb
                ipdb.set_trace()
                with open('/tmp/dream11.txt', 'r') as f:
                    teams = f.readlines()
                team1 = teams[0].strip("\n")
                team2 = teams[1].strip("\n")
            pt = re.compile(r'\d+\s+')
            res = re.sub(pt, '', team1)
            self.logger.info("Adding team1 players to espn_list")
            for ele in res.split(', '):
                if ele:
                    if '(wk)' in ele:
                        ele = "".join(ele.split('(wk)')).strip()
                    if '(capt)' in ele:
                        ele = "".join(ele.split('(capt)')).strip()
                    if '/' in ele:
                        for x in ele.split('/'):
                            self.espn_list.append(x.strip().strip('.').strip())
                        continue
                    if 'probable' in ele:
                        ele = ''.join(ele.split('(probable) '))
                    if 'possible' in ele:
                        ele = ''.join(ele.split('(possible) '))
                    self.espn_list.append(ele.strip().strip('.').strip())
            self.logger.info("%s Players are %s" % (team_name1, self.espn_list))
            self.logger.info("Total %s Players are %d" % (team_name1, len(self.espn_list)))
            self.file_logger.info("%s Players are %s" % (team_name1, self.espn_list))
            self.file_logger.info("Total %s Players are %d" % (team_name1, len(self.espn_list)))
            self.logger.info("Formatting the text...")
            res = re.sub(pt, '', team2)
            self.logger.info("Adding team2 players to espn_list")
            team1_players = deepcopy(self.espn_list)
            team2_players = []
            for ele in res.split(', '):
                if ele:
                    if '(wk)' in ele:
                        ele = "".join(ele.split('(wk)')).strip()
                    if '(capt)' in ele:
                        ele = "".join(ele.split('(capt)')).strip()
                    if '/' in ele:
                        for x in ele.split('/'):
                            self.espn_list.append(x.strip().strip('.').strip())
                            team2_players.append(x.strip().strip('.').strip())
                        continue
                    if 'probable' in ele:
                        ele = ''.join(ele.split('(probable) '))
                    if 'possible' in ele:
                        ele = ''.join(ele.split('(possible) '))
                    self.espn_list.append(ele.strip().strip('.').strip())
                    team2_players.append(ele.strip().strip('.').strip())
            self.logger.info("%s Players are %s" % (team_name2, team2_players))
            self.logger.info("Total %s Players are %d" % (team_name2, len(team2_players)))
            self.file_logger.info("%s Players are %s" % (team_name2, team2_players))
            self.file_logger.info("Total %s Players are %d" % (team_name2, len(team2_players)))
            database_obj.insert_teams_into_db(link, team1_players, team2_players)

        except WebDriverException:
            self.logger.info("Exception Occurred... writing to the log file")
            self.file_logger.debug(traceback.format_exc())


class Dream11Exception(Exception):
    """
    Custom Exception Class
    """

    def __init__(self, message):
        super(Exception, self).__init__(message)
        self.message = message

    def __str__(self):
        return self.message


if __name__ == "__main__":
    obj = Dream11()
    obj.get_data(ipl=True)