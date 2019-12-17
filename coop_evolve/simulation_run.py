#!/usr/bin/env python
# -*- coding: utf-8 -*-

class SimulationRun:
    
    def __init__(self, generations = 10000,
                       width = 100,
                       length = 100,
                       subpop_size = 100,
                       relative_fitnesses = True,
                       migration_survival = 0.1,
                       migration_distance = 1
                 ):
        self.generations = generations
        self.width = width
        self.length = length
        self.subpop_size = subpop_size
        self.relative_fitnesses = relative_fitnesses
        self.migration_survival = migration_survival
        self.migration_distance = migration_distance
        
        