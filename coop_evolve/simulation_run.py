#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
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
        
        # self.data = []
        
        self.population = Population(
            width = self.width, 
            length = self.length, 
            subpop_size = self.subpop_size,
            sequence = self.initial_sequence
        )
                
        
    def run(self):
        cfg = AppSettings()
        
        # try:
        run_dir =  "/run_" + str(time.time() )
        os.makedirs(cfg.data_directory + run_dir)
        behavior_headers = ["generation", "x_coord", "y_coord"]
        for h in range(len(cfg.behaviors)):
            behavior_headers.append(cfg.behaviors[h])
        with open(cfg.data_directory + run_dir + "/behavior_counts.csv", 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames = behavior_headers)
            writer.writeheader()
        
        fitness_headers = ["generation", "x_coord", "y_coord", "mean_fitness"]
        with open(cfg.data_directory + run_dir + "/mean_fitness.csv", 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames = fitness_headers)
            writer.writeheader()
            
        # # except:
        # #     os.makedirs(cfg.data_directory + "/run_" + str(time.time() ))
        
        for i in range(self.generations + cfg.data_frequency):
            if (i - 1)%cfg.data_frequency == 0:
                data =  self.population.play_game()
                with open(cfg.data_directory + run_dir + "/behavior_counts.csv", 'a') as csvfile:
                    for row in data:
                        row["generation"] = i
                        writer = csv.DictWriter(csvfile, fieldnames = behavior_headers)
                        writer.writerow(row)
            else:
                self.population.play_game()
            self.population.mutate()
            self.population.mate()
            if (i - 1)%cfg.data_frequency == 0:
                data = self.population.reproduce()
                with open(cfg.data_directory + run_dir + "/mean_fitness.csv", 'a') as csvfile:
                    for row in data:
                        row["generation"] = i
                        writer = csv.DictWriter(csvfile, fieldnames = fitness_headers)
                        writer.writerow(row)
            else:
                self.population.reproduce()
            self.population.migrate()
            self.population.cull()
                

        
        
            
            