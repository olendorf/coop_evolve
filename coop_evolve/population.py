#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import numpy
import random

from app_settings import AppSettings

from coop_evolve.agent import Agent

from scipy.stats import poisson

class Population:
    
    def __init__(self, width, length, subpop_size, sequence = None):
        self.width = width
        self.length = length
        self.subpop_size = subpop_size
        
        self.population = []
        for i in range(self.width):
            row = []
            for j in range(self.length):
                subpop = []
                for k in range(self.subpop_size):
                    subpop.append(Agent(sequence))
                row.append(subpop)
            self.population.append(row)
        # needed to make population iterable
        self.population = list(self.population)
        
    def popsize(self):
        """
        The number of agents currenlty in the populatoin.The
        
        Returns
        -------
        
        popsize: Integer 
        
        """
        
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
        
        behavior_counts = []
        
        for i in range(self.width):
            for j in range(self.length):
                counts = {"x_coord": i, "y_coord": j}
                for h in range(len(cfg.behaviors)):
                    counts[cfg.behaviors[h]] = 0
                for _ in range(interactions * self.subpop_size):
                    index1 = random.randint(0, (self.subpop_size - 1))
                    index2 = random.randint(0, (self.subpop_size - 1))
                    while index1 == index2:
                        index2 = random.randint(0, self.subpop_size - 1)
                    agent1 = self.population[i][j][index1]
                    agent2 = self.population[i][j][index2]
                    histories = Agent.interact(agent1, agent2)
                    
                    for h in range(len(cfg.behaviors)):
                        counts[cfg.behaviors[h]] += \
                            (histories[0] + histories[1]).count(cfg.behaviors[h])
                behavior_counts.append(counts)
                        
                    
        return behavior_counts

                    
    def mutate(self):
        for i in range(self.width):
            for j in range(self.length):
                for k in range(self.subpop_size):
                    self.population[i][j][k].mutate()
    def mate(self):
        cfg = AppSettings()
        
        for i in range(self.width):
            for j in range(self.length):
                for _ in range(int(round(self.subpop_size * cfg.mating_rate * 0.5))):
                    index1 = random.randint(0, (self.subpop_size - 1))
                    index2 = random.randint(0, (self.subpop_size - 1))
                    while index1 == index2:
                        index2 = random.randint(0, self.subpop_size - 1)
                    agent1 = self.population[i][j][index1]
                    agent2 = self.population[i][j][index2]
                    Agent.mate(agent1, agent2)

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
            
    def mutations(self):
        for i in range(self.width):
            for j in range(self.length):
                for k in range(self.subpop_size):
                    self.population[i][j][k].mutations()
            
    def migrate(self, survival=0.1, distance=1):
        """
        If a subpopulation has surplus agents after reproducing they migrate to 
        nearby subpopulations. 
        
        Migrating agents migrate a distance on average too
        the distance in both x and y drawn from the poisson distribution. Agents also
        have a survival probability, so that if survival is 0.1, 1 in 10 agents survive
        migration.
        
        Parameters
        ----------
        survival: Float, default = 0.1
            The probability the agent survives migration.
            
        distance: Integerm defaykt = 1
            The average distance an agent moves in both X and Y directions, drawn
            from the poisson distribution.
        """
        
        migrants = []
        for i in range(self.width):
            row = []
            for j in range(self.length):
                row.append([])
            migrants.append(row)
            
        for i in range(self.width):
            for j in range(self.length):
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
            for j in range(self.length):
                self.population[i][j] = self.population[i][j] + migrants[i][j]
                        
    def cull(self):
        """
        Randomly removes agents from subpopulations until they are down to carrying capacity
        """
        for i in range(self.width):
            for j in range(self.length):
                while(len(self.population[i][j]) > self.subpop_size):
                    self.population[i][j].pop(
                        random.randrange(len(self.population[i][j])))
                        
    def generation(self, interactions = 1, 
                         fecundity = 1, 
                         relative_fitnesses = True,
                         migration_distance = 1,
                         migration_survival = 0.1):
        """
        Goes through one full lifecycle of a population.
        
        parameters
        ---------
        interactions Integer, default = 1
            The expected number of interactions an agent has in a generation.
        
        fecundity: Integer, default = 1
            The expected number of offspring per agent per generation. 
            
        relative_fitnesses: Boolean, default = True
            If true agents reproduce based on relative fitness. Each subpopuation produces
            exactly *fecundity* * N offspring. If False, absolute fitness is used, where each
            agent gets *fecundity* chances to reproduce based on its performance vs the max possible.
            
        migration_distance: Integer, default = 1
            How far in both x and y directions an agent moves if it survives migration.
            
        migration_survival: Float, default 0.1
            If chosen to migrate, the probability an agent survives migration. 
        """
        
        self.play_game(interactions)
        self.reproduce(fecundity, relative_fitnesses)
        self.migrate(migration_distance, migration_survival)
        self.cull()
        
    def reset(self):
        """
        Resets the population to starting state for the next genration in the simulation.Resets
        """
        
        for i in range(self.width):
            for j in range(self.length):
                for k in range(self.subpop_size):
                    self.population[i][j][k].reset
                        
            
    def __reproduce_with_relative_fitness(self, fecundity):
        """
        Agents reproduce according to relative fitness within its subpopulation. Each 
        subpopulation produces exactly *fecundity* * *subpop_size* new agents. The probability
        each agent reproduces is proportianal to its fitness relative the to subpopulations fitness.
        
        parameters
        ---------
        fecundity: Integer
            The number of agents produced per agent in a subpopulation.
        """
        
        for i in range(self.width):
            for j in range(self.length):
                relative_fitnesses = []
                for k in range(self.subpop_size):
                    relative_fitnesses.append(self.population[i][j][k].fitness())
                
                # Need to protect against dividing by zero if all the payoffs are zero.
                # Since they are all equal (zero) assume each is equally likely to reproduce
                if sum(relative_fitnesses) == 0:
                    relative_fitnesses = numpy.cumsum(
                        [(1/len(relative_fitnesses)) for _ in range(len(relative_fitnesses))] )
                else:
                    relative_fitnesses = numpy.cumsum(
                        [(f/sum(relative_fitnesses)) for f in relative_fitnesses]).tolist()
                for _ in range(fecundity * self.subpop_size):
                    index = 0
                    rand = random.random()
                    while rand > relative_fitnesses[index]:
                        index += 1
                    self.population[i][j].append(copy.deepcopy(self.population[i][j][index]))
                    
    def __reproduce_with_absolute_fitness(self, fecundity):
        """
        Agents reproduce using absolute fitness. Each agent gets *fecundity* chances to reproduce. 
        The probability it reproduces is equal to its fitness/max_possible_fitness. The amount
        of reproduction in a population depends on the fitness of its agents.amount
        
        parameters
        ----------
        
        fecundity: Integer
            The number of chances each agent is given to reproduce in a population.
        """
        
        cfg = AppSettings()
        max_payoff = max(cfg.payoffs.values())
        for i in range(self.width):
            for j in range(self.length):
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
        
            

