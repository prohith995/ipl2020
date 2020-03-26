# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 00:20:49 2020

@author: nxf55806
"""

import random
import numpy as np

class innings:
    
    _registry = []
    
    def __init__(self, name):
        self._registry.append(self)
        self.name = name
    
    def add_batsmen(self, batsmen):
        self.batsmen = batsmen

    def add_bowlers(self, bowlers):
        self.bowlers = bowlers
    
    def start_batting(self):
        self.remaining_batsmen = self.batsmen
        self.batsmen_score = {}
        # self.final_batsmen_score = {}
        # self.last_batsman = None
        self.current_batsman = self.batsmen[0]
        self.current_runner = self.batsmen[1]
        self.batsmen_score[self.current_batsman] = 0            
        self.batsmen_score[self.current_runner] = 0            
        self.over = 1
        self.ball = 1
        self.wickets = 0
        self.team_score = 0

    # def start_batting(self):
    #     self.remaining_bowlers = self.bowlers
    #     self.batsmen_score = {}
    #     # self.final_batsmen_score = {}
    #     self.current_batsman = self.batsmen[0]
    #     self.current_runner = self.batsmen[1]
    #     self.batsmen_score[self.current_batsman] = 0            
    #     self.batsmen_score[self.current_runner] = 0            
    #     self.over = 1
    #     self.ball = 1
    #     self.wickets = 0
    #     self.team_score = 0

    def ball_bowled(self, runs, wicket):
        self.team_score = self.team_score + runs
        if wicket == 1:
            self.batsmen_score[self.current_batsman] = self.batsmen_score[self.current_batsman] + runs
            # self.last_batsman = self.current_batsman
            if self.wickets <= 9:
                self.current_batsman = self.remaining_batsmen[0]
                self.remaining_batsmen = self.remaining_batsmen[1:]
                self.batsmen_score[self.current_batsman] = 0
            else:
                return ('All Out')
            self.wickets = self.wickets+1
            if self.ball == 6:
                self.ball == 0
                self.over = self.over+1
                if runs % 2 == 0:
                    self.current_batsman, self.current_runner = self.current_runner, self.current_batsman
            else:
                self.ball = self.ball + 1
                if runs % 2 == 1:
                    self.current_batsman, self.current_runner = self.current_runner, self.current_batsman
        else:
            self.batsmen_score[self.current_batsman] = self.batsmen_score[self.current_batsman] + runs
            if self.ball == 6:
                self.ball = 0
                self.over = self.over+1
                if runs % 2 == 0:
                    self.current_batsman, self.current_runner = self.current_runner, self.current_batsman
            else:
                self.ball = self.ball + 1
                if runs % 2 == 1:
                    self.current_batsman, self.current_runner = self.current_runner, self.current_batsman
        
        if self.over > 20:
            return 'Innings Over'            
 
teamA_name = 'team1'
teamB_name = 'team2'

def play_match(teamA_name, teamB_name):

    toss = random.randint(1,2)
    if toss == 1:
        team1 = innings(teamA_name)
        team2 = innings(teamB_name)
        team1.add_batsmen(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k'])
        team2.add_batsmen(['l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v'])
    else:
        team1 = innings(teamB_name)
        team2 = innings(teamA_name)
        team2.add_batsmen(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k'])
        team1.add_batsmen(['l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v'])

    for teamobj in innings._registry:
        teamobj.start_batting()
        for over in range(20):
            for ball in range(6):
                # Simulate ball  
                run_prob = [[0,1,2,3,4,6], [0.2,0.3,0.2,0.05,0.15,0.1]]
                wicket_prob = [[0, 1], [0.95, 0.05]]
                teamobj.ball_bowled(np.random.choice(run_prob[0], p=run_prob[1]), 
                                 np.random.choice(wicket_prob[0], p=wicket_prob[1]))

play_match(teamA_name, teamB_name)
