#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import os
import pytest

from app_settings import AppSettings

from coop_evolve.simulation_run import SimulationRun

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
        assert run.relative_fitnesses == True
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
    
    def teardown_method(self, test_method):
        try:
            os.system('rm -rf temp')
        except:
            pass
    
    def test_stable_population_size(self):
        width = 5
        length = 4
        subpop_size = 3
        generations = 100
        run = SimulationRun(
            width = width, 
            length = length, 
            subpop_size = subpop_size, 
            generations = generations
        )
        
        run.run()
        
        assert run.population.popsize() == width * length * subpop_size
        
    def test_generation_length(self):
        cfg = AppSettings()
        width = 5
        length = 4
        subpop_size = 3
        generations = 100
        run = SimulationRun(
            width = width, 
            length = length, 
            subpop_size = subpop_size, 
            generations = generations
        )
        
        run.run()
        assert len(run.data) == math.floor((generations + cfg.data_frequency)/cfg.data_frequency)


class test_data_collection:
    
    def test_behavior_data(self):
        width = 2
        length = 2
        subpop_size = 2
        
        