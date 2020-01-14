#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import json
import os
import psycopg2
import sys
import time

from app_settings import AppSettings

from coop_evolve.population import Population

class SimulationRun:
    
    def __init__(self, generations = 10000,
                       width = 100,
                       length = 100,
                       subpop_size = 100,
                       relative_fitness = True,
                       migration_survival = 0.1,
                       migration_distance = 1,
                       initial_sequence = None,
                       fecundity = 1
                 ):
        cfg = AppSettings()             
                     
        self.generations = generations
        self.width = width
        self.length = length
        self.subpop_size = subpop_size
        self.relative_fitness = relative_fitness
        self.migration_survival = migration_survival
        self.migration_distance = migration_distance
        self.initial_sequence = initial_sequence
        self.fecundity = fecundity
        
        self.population = Population(
            width = self.width, 
            length = self.length, 
            subpop_size = self.subpop_size,
            sequence = self.initial_sequence
        )
                
        
    def run(self, simulation_id = None):
        cfg = AppSettings()
        conn = psycopg2.connect(
            f"dbname= '{cfg.database}' " + 
            f"user='{cfg.db_user}' " + 
            f"password={cfg.db_password} " + 
            f"host=localhost"
        )
        cur = conn.cursor()
        
        if self.initial_sequence == None:
            query = f"INSERT INTO {cfg.schema_name}.runs (\
                            simulation_id, generations, width, length, subpop_size, \
                            relative_fitnesses, migration_distance, migration_survival) \
                     VALUES ( \
                        {simulation_id}, {self.generations}, {self.width}, {self.length}, \
                        {self.subpop_size}, {self.relative_fitness}, \
                        {self.migration_distance}, {self.migration_survival} \
                     )"
        else:
            query = f"INSERT INTO {cfg.schema_name}.runs (\
                            simulation_id, generations, width, length, subpop_size, \
                            relative_fitnesses, migration_distance, migration_survival, \
                            initial_sequence ) \
                     VALUES ( \
                        {simulation_id}, {self.generations}, {self.width}, {self.length}, \
                        {self.subpop_size}, {self.relative_fitness}, \
                        {self.migration_distance}, {self.migration_survival}, \
                        {self.initial_sequence}\
                      )"
        try:
            cur.execute(query)
        except psycopg2.Error as e:
            print('Unable to insert: ').format(e)
            sys.exit(1)
        conn.commit()
        
        print("run inserted")
        
        query = f"SELECT id FROM {cfg.schema_name}.runs ORDER BY id LIMIT 1"
        cur.execute(query)
        
        run_id = cur.fetchall()[0][0]
        
        for g in range(self.generations):
            data = self.population.generation(
                relative_fitnesses=self.relative_fitness,
                interactions = cfg.interaction_length,
                fecundity = self.fecundity,
                migration_distance = self.migration_distance,
                migration_survival = self.migration_survival
                )
                
            census = self.population.census()
                  
            conn = psycopg2.connect(
                f"dbname= '{cfg.database}' " + 
                f"user='{cfg.db_user}' " + 
                f"password={cfg.db_password} " + 
                f"host=localhost"
            )
            cur = conn.cursor()
            for i in range(self.width):
                for j in range(self.length):   
                    
                    behaviors = json.dumps(data['behavior_data']['subpop_counts'][i][j])
                    sequences = json.dumps(census['subpop_data'][i][j])
                    
                    query = f"INSERT INTO {cfg.schema_name}.subpop_data (\
                                    run_id, generation, x_coord, y_coord, mean_fitness, \
                                    behavior, census) \
                            VALUES(%s, %s, %s, %s, %s, %s, %s)"
                    
                    cur.execute(query, (run_id, g, i, j, data['fitness_data'][i][j], behaviors, sequences))
                    conn.commit()
            conn.close()
        return run_id
            
            
            
        
        
        
                

        
        
            
            