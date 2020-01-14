#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import os
import psycopg2
import pytest

from app_settings import AppSettings
from os import listdir

from coop_evolve.simulation_run import SimulationRun
from coop_evolve.db_setup import DB_Setup

class TestSimulationRunCreation:
    
    def test_defaults(self):       
        width = 100
        length = 10
        subpop_size = 10
        
        run = SimulationRun(width = width, length = length, subpop_size = subpop_size)
 
        
        assert run.generations == 10000
        assert run.width == width
        assert run.length == length
        assert run.subpop_size == subpop_size
        assert run.relative_fitness == True
        assert run.migration_survival == 0.1
        assert run.migration_distance == 1
        assert run.initial_sequence == None
        
    def test_population_creation(self):
        width = 5
        length = 4
        subpop_size = 3
        simulation = SimulationRun(
            width = width, 
            length = length, 
            subpop_size = subpop_size
        )
        
        assert len(simulation.population.population) == width
        assert len(simulation.population[0]) == length
        assert len(simulation.population[0][0]) == subpop_size
        
class TestSimulationRun:

    def test_stable_population_size(self):
        width = 5
        length = 4
        subpop_size = 3
        generations = 10
        run = SimulationRun(
            width = width, 
            length = length, 
            subpop_size = subpop_size, 
            generations = generations
        )
        
        run.run(1)
        
        assert run.population.popsize() == width * length * subpop_size
        

class TestDataCollection:

    
    def test_subpop_data_length(self):
        
        db = DB_Setup()
        db.reset()
        width = 2
        length = 2
        subpop_size = 2
        generations = 50
        run = SimulationRun(
            width = width, 
            length = length, 
            subpop_size = subpop_size, 
            generations = generations
        )
        
        run_id = run.run(simulation_id = 1)
        
        
        cfg = AppSettings()
        
        conn = psycopg2.connect(
            f"dbname= '{cfg.database}' " + 
            f"user='{cfg.db_user}' " + 
            f"password={cfg.db_password} " + 
            f"host=localhost"
        )
        cur = conn.cursor()
        
        
        cur.execute(f"SELECT COUNT(*) FROM (SELECT * FROM test.subpop_data WHERE run_id = {run_id}) as foo")
        
        expected = cur.fetchall()[0][0]
        
        assert expected == width * length * generations/10
    
    def test_pop_data_length(self):
    
        db = DB_Setup()
        db.reset()
        width = 2
        length = 2
        subpop_size = 2
        generations = 50
        run = SimulationRun(
            width = width, 
            length = length, 
            subpop_size = subpop_size, 
            generations = generations
        )
        
        run_id = run.run(1)
        
        
        cfg = AppSettings()
        
        conn = psycopg2.connect(
            f"dbname= '{cfg.database}' " + 
            f"user='{cfg.db_user}' " + 
            f"password={cfg.db_password} " + 
            f"host=localhost"
        )
        cur = conn.cursor()
        
        
        cur.execute(f"SELECT COUNT(*) FROM (SELECT * FROM test.pop_data WHERE run_id = {run_id}) as foo")
        
        expected = cur.fetchall()[0][0]
        
        assert expected == generations/10
            
        
    
        
        
        