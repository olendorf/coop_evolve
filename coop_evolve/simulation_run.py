#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time

from app_settings import AppSettings

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
        cfg = AppSettings()             
                     
        self.generations = generations
        self.width = width
        self.length = length
        self.subpop_size = subpop_size
        self.relative_fitnesses = relative_fitnesses
        self.migration_survival = migration_survival
        self.migration_distance = migration_distance
        self.initial_sequence = initial_sequence
        
        self.migration_survival = migration_survival
        self.migration_distance = migration_distance
        self.initial_sequence = initial_sequence
        
        self.data = []
        
        self.population = Population(
            width = self.width, 
            length = self.length, 
            subpop_size = self.subpop_size,
            sequence = self.initial_sequence
        )
                
        
    def run(self):
        cfg = AppSettings()
        
        try:
            os.makedirs(cfg.data_directory + "/run_" + str(time.time() ))
        except:
            os.makedirs(cfg.data_directory + "/run_" + str(time.time() ))
        
        for i in range(self.generations + cfg.data_frequency):
            if (i - 1)%cfg.data_frequency == 0:
                data = {
                    "generation": i
                }
                data["behavior_counts"] = self.population.play_game()
            else:
                self.population.play_game()
            self.population.mutate()
            self.population.mate()
            self.population.reproduce()
            self.population.migrate()
            self.population.cull()
            if (i - 1)%cfg.data_frequency == 0:
                self.data.append(data)
            
            