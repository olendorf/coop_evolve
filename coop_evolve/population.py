#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import numpy
import random

from app_settings import AppSettings

from coop_evolve.agent import Agent

from scipy.stats import poisson

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
        
    def popsize(self):
        popsize = 0
        for i in range(len(self.population)):
            for j in range(len(self.population[i])):
                popsize += len(self.population[i][j])
        return popsize
                
        
    def play_game(self, interactions = 1):
        """
        Agents play the game with others from the same population.
        
        Within each subpopulation, two agents are chosen randomly to interact. This 
        is repeated `interactions` times for each subpopulation.is
        
        Parameters
        ---------
        interactions: Integer, default = 1
            The number of interactions per agent. If interactions = 2, and there are
            10 agents in the population, then there are 20 interactions and each agent
            is expected to take part in 40 interactions. 
        """
        cfg = AppSettings()
        
        for i in range(self.width):
            for j in range(self.height):
                for _ in range(interactions * self.subpop_size):
                    index1 = random.randint(0, (self.subpop_size - 1))
                    index2 = random.randint(0, (self.subpop_size - 1))
                    while index1 == index2:
                        index2 = random.randint(0, self.subpop_size - 1)
                    agent1 = self.population[i][j][index1]
                    agent2 = self.population[i][j][index2]
                    Agent.interact(agent1, agent2)

    def reproduce(self, fecundity = 1, relative_fitnesses = True):
        """
        Agents reproduce based on their relative fitness.
        
        The probability that an agent reproduces is based on its fitness divided by the subpopulation total fitness 
        times fecundity * subpopulation size. So if there are 10 agents, fecundity of one, and the relative 
        fitness is 0.25, the agent will on average have 2.5 offspring.fitness
        
        Parameters
        ----------
        fecundity: Integer, default = 1
            The average number of offspring per agent.
            
        relative_fitnesses: Boolean, default = True
            If true agents relative fitness is used. Agents reproduce proportianal to their relative fitness (fitness)/(sum(subpop_fitness))
            If false, absolute fitness, each agent has the probability of reproducing fitness/max_possible_fitness. Relative fitness reproduction results in 
            equal reproduction across subpopulations. Absolute fitness results in subpopulation reproduction being relative to the mean fitness 
            in the subpopulation
            
        """
        
        if(relative_fitnesses):
            self.__reproduce_with_relative_fitness(fecundity)
        else:
            self.__reproduce_with_absolute_fitness(fecundity)
            
    def migrate(self, survival, distance):
        cfg = AppSettings()
        
        migrants = []
        for i in range(self.width):
            row = []
            for j in range(self.height):
                row.append([])
            migrants.append(row)
            
        for i in range(self.width):
            for j in range(self.height):
                while(len(self.population[i][j]) > self.subpop_size):
                    index = random.randint(0, len(self.population[i][j]) - 1)
                    if random.random() < survival:
                        x = poisson.rvs(distance)
                        x = i + (x * -1) if random.random() < 0.5 else i + x
                        y = poisson.rvs(distance)
                        y = j + (y * -1) if random.random() < 0.5 else j + y
                        
                        if x >= 0 and x < len(migrants) and y >= 0 and y < len(migrants[0]):
                            migrants[x][y].append(self.population[i][j][index])
                    del self.population[i][j][index]
                    
        for i in range(self.width):
            for j in range(self.height):
                self.population[i][j] = self.population[i][j] + migrants[i][j]
                        
                        
                        
            
    def __reproduce_with_relative_fitness(self, fecundity):
        
        for i in range(self.width):
            for j in range(self.height):
                relative_fitnesses = []
                for k in range(self.subpop_size):
                    relative_fitnesses.append(self.population[i][j][k].fitness())
                relative_fitnesses = numpy.cumsum([(i/sum(relative_fitnesses)) for i in relative_fitnesses]).tolist()
                for _ in range(fecundity * self.subpop_size):
                    index = 0
                    rand = random.random()
                    while rand > relative_fitnesses[index]:
                        index += 1
                    self.population[i][j].append(copy.deepcopy(self.population[i][j][index]))
                    
    def __reproduce_with_absolute_fitness(self, fecundity):
        cfg = AppSettings()
        max_payoff = max(cfg.payoffs.values())
        for i in range(self.width):
            for j in range(self.height):
                popsize = len(self.population[i][j])
                for _ in range(fecundity):
                    for k in range(popsize):
                        if random.random() <= self.population[i][j][k].fitness()/max_payoff:
                            self.population[i][j].append(copy.deepcopy(self.population[i][j][k]))
                
                    
                    
                        
                    
            
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
        
    # def __setitem__(self, key, value): # pragma: no cover
    #     """
    #     Allows items, slices etc to be assigned (or reassigned). For example
    #     `pop[0] = Agent()`
        
    #     Parameters
    #     __________
    #     key: Any list indexing or slicing parameters
        
    #     value: Agent|[Agents]
    #         An agent or list of agents.
            
    #     """
    #     self.population[key] = value
        
            

