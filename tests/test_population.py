#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `coop_evolve.population Population` class."""

import pytest

from app_settings import AppSettings

from coop_evolve.agent import Agent
from coop_evolve.population import Population


class TestPopulationCreation:
    """Test population creation."""
    
    def test_dimensions(self):
        width = 5
        height = 4
        subpop_size = 3
        
        population = Population(width, height, subpop_size)
        
        assert len(population.population) == 5
        assert len(population[0]) == 4
        assert len(population[0][1]) == 3
        
    def test_random_agents(self):
        width = 5
        height = 4
        subpop_size = 3
        
        population = Population(width, height, subpop_size)
        assert population[0][0][0] != population[1][1][1]
        
    def test_specified_sequence(self):
        width = 5
        height = 4
        subpop_size = 3
        
        population = Population(width, height, subpop_size, sequence = "abcd")
        assert population[0][0][0].dna.sequence == \
               population[1][1][1].dna.sequence
               
    def test_assign_agent(self):
        width = 5
        height = 4
        subpop_size = 3
        
        population = Population(width, height, subpop_size, sequence = "aaaa")
        
        population[0][0][0] = Agent("bbbb")
        
        assert population[0][0][0].dna.sequence == "bbbb"
        
               
    
        
        
        