#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

from app_settings import AppSettings

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
        # needed to make population iterable
        self.population = list(self.population)
        
    def play_game(self, interactions = 1):
        """
        Agents play the game with others from the same population.
        
        Within each subpopulation, two agents are chosen randomly to interact. This 
        is repeated `interactions` times for each subpopulation.is
        
        Parameters
        ---------
        interactions: integer, default = 1
            The number of interactions per agent. If interactions = 2, and there are
            10 agents in the population, then there are 20 interactions and each agent
            is expected to take part in 40 interactions. 
        """
        cfg = AppSettings()
        
        for i in range(self.width):
            for j in range(self.height):
                for k in range(interactions * self.subpop_size):
                    index1 = random.randint(0, (self.subpop_size - 1))
                    index2 = random.randint(0, (self.subpop_size - 1))
                    while index1 == index2:
                        index2 = random.randint(0, self.subpop_size - 1)
                    agent1 = self.population[i][j][index1]
                    agent2 = self.population[i][j][index2]
                    Agent.interact(agent1, agent2)
                        
            
    def __getitem__(self, key):
        """
        Allows Population to behave much like an **Array** or **List** by providing
        indexing functions like `pop[0]`.
        
        Parameters
        ----------
        key: Any list indexing or slicing parameters
        
        Returns
        _______
        The specified part of the population
        """
        return self.population[key]
        
    def __setitem__(self, key, value): # pragma: no cover
        """
        Allows items, slices etc to be assigned (or reassigned). For example
        `pop[0] = Agent()`
        
        Parameters
        __________
        key: Any list indexing or slicing parameters
        
        value: Agent|[Agents]
            An agent or list of agents.
            
        """
        self.population[key] = value
        
            

