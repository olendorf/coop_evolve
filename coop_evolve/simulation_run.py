#!/usr/bin/env python
# -*- coding: utf-8 -*-

from coop_evolve.population import Population

class SimulationRun:
    
    def __init__(self, generations = 10000,
                       width = 100,
                       length = 100,
                       subpop_size = 100,
                       relative_fitnesses = True,
                       migration_survival = 0.1,
                       migration_distance = 1,
                       initial_sequence = None
                 ):
        self.generations = generations
        self.width = width
        self.length = length
        self.subpop_size = subpop_size
        self.relative_fitnesses = relative_fitnesses
        self.migration_survival = migration_survival
        self.migration_distance = migration_distance
        self.initial_sequence = initial_sequence
        
        self.data = [{}]
        
        self.population = Population(
            width = self.width, 
            length = self.length, 
            subpop_size = self.subpop_size,
            sequence = self.initial_sequence
        )
                
        
    def run(self):
        
        for _ in range(self.generations):
            data = {}
            self.population.play_game()
            self.population.reproduce()
            self.population.migrate()
            self.population.cull()
            self.data.append(data)
            
            
            