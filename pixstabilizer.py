# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 17:29:17 2020

@author: Dustin Tengdyantono
"""

#run_left_sided_servo this code is meant to run the left armed servo

class pixelstabilizer:
    
    def __init__(self):
        self.forehead = list()
        self.distance = list()
        self.n = 15 #pixel counter
        self.div = 5 #it's 5 because we're only taking the last 5 values from 15 pixels
        
    def forehead__y(self,fhy):
        self.forehead.append(fhy)
        print(self.forehead)
        if len(self.forehead) == self.n:
            total_fivehead = sum (self.forehead[self.n-4:self.n])
            print(total_fivehead)
            avgforehead = float(list_of_last_fivehead/ self.div)
            print(avgforehead)
            self.forehead = list()
            favgf= float(avgforehead)
            return favgf
        else:
            return False
    def distance_(self,dy):
        self.distance.append(dy)
        if len(self.distance) == self.n:
            total_fivedistaces = sum (self.distance[self.n-4:self.n])
            avgdistances = float(total_fivedistaces/self.div)
            self.distance = list()
            favgd = float(avgdistances)
            return favgd
        else:
            return False
    
    
                                                            
        
        