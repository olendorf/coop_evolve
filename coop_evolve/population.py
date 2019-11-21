#!/usr/bin/env python
# -*- coding: utf-8 -*-

from coop_evolve.agent import Agent

class Population:
    
    def __init__(self, width, height, subpop_size, sequence = None):
        self.width = width
        self.height = height
        self.subpop_size = subpop_size
        
        self.population = []
        for i in range(self.width):
            row = []
            for j in range(self.height):
                subpop = []
                for k in range(self.subpop_size):
                    subpop.append(Agent(sequence))
                row.append(subpop)
            self.population.append(row)
        self.population = list(self.population)
            
    def __getitem__(self, key):
        return self.population[key]
        
            

