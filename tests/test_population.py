#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `coop_evolve.population Population` class."""

import pytest

from app_settings import AppSettings

from coop_evolve.agent import Agent
from coop_evolve.population import Population

from scipy.stats import nbinom
from scipy.stats import poisson


class TestPopulationCreation:
    """Test population creation."""
    
    def test_dimensions(self):
        """ Test the population is of the correct dimensions"""
        width = 5
        height = 4
        subpop_size = 3
        
        population = Population(width, height, subpop_size)
        
        assert len(population.population) == 5
        assert len(population[0]) == 4
        assert len(population[0][1]) == 3
        
    def test_setting_item(self):
        width = 5
        height = 4
        subpop_size = 3
        
        population = Population(width, height, subpop_size)
        population[0][0][0] = Agent("abcd")
        
        assert population[0][0][0].dna.sequence == "abcd"
        
        
    def test_random_agents(self):
        """ Test that agents are made randomly when that is wanted"""
        width = 5
        height = 4
        subpop_size = 3
        
        population = Population(width, height, subpop_size)
        assert population[0][0][0] != population[1][1][1]
        
    def test_specified_sequence(self):
        """Test agents with specific dna sequences can be created """
        width = 5
        height = 4
        subpop_size = 3
        
        population = Population(width, height, subpop_size, sequence = "abcd")
        assert population[0][0][0].dna.sequence == \
               population[1][1][1].dna.sequence
               
    def test_assign_agent(self):
        """ Ensure the __setitem__ method works"""
        width = 5
        height = 4
        subpop_size = 3
        
        population = Population(width, height, subpop_size, sequence = "aaaa")
        
        population[0][0][0] = Agent("bbbb")
        
        assert population[0][0][0].dna.sequence == "bbbb"
        
class TestPlayingGame:
    """ Test aspects of playing the game """
    
    def test_interaction_lengths(self):
        """ Tests that the interaction length is correct """
        
        cfg = AppSettings()
        
        width = 10
        height = 10
        subpop_size = 10
        
        expected_interactions = 2
        
        population = Population(width, height, subpop_size)
        
        population.play_game(expected_interactions)
        payoff_lengths = []
        for i in range(width):
            for j in range(height):
                for k in range(subpop_size):
                    payoff_lengths.append(len(population[i][j][k].payoffs))
        mean_payoff_length = sum(payoff_lengths)/1000
        
        var_poisson = poisson.var(expected_interactions)
        
        expected_interaction_length = cfg.interaction_length
        
        p = 1 - (expected_interaction_length/(1 + expected_interaction_length))
        var_nbinom = nbinom.var(1, p)
        
        
        var = var_poisson * var_nbinom + \
              var_poisson * expected_interaction_length + \
              expected_interactions * var_nbinom
        conf_99 = (var/1000)**(1/2) * 5
        expected_payoff_length = 2 * expected_interactions * expected_interaction_length
        
        assert (expected_payoff_length - conf_99) < \
               mean_payoff_length < \
               (expected_payoff_length + conf_99)
               
class TestReproduction:
    
    def test_fecundity_relative_fitness(self):
        """ 
        Tests that subpopulatons reproduce at the same rate and equally under
        relative fitness
        """
        
        width = 2
        height = 2
        subpop_size = 10
        
        population = Population(width, height, subpop_size)
        
        fecundity = 2
        
        population.reproduce(fecundity)
        
        assert len(population[0][0]) == subpop_size * (fecundity + 1)
        assert len(population[0][0]) == len(population[1][1])
        
    def test_relative_fitness_reproduction(self):
        """ Tests that the agents reproduce corrctly based on their relaive fitness """
        
        reps = 1000
        popsize = 4
        
        counts = {"a": 0, "aa": 0, "aaa": 0, "aaaa": 0}
        for _ in range(reps):
            population = Population(1,1,popsize)
            
            k = 1
            for agent in population[0][0]:
                agent.dna.sequence = "a"*k
                agent.payoffs = [k]
                k += 1
            
            population.reproduce()
            
            for i in range(4, 8):
                counts[population[0][0][i].dna.sequence] += 1
                
        var = []
        for i in range(popsize):
            var.append(i + 1)
        var = [i/sum(var) for i in var]
        expecteds = {}
        for i in range(popsize):
            expecteds["a"*(i + 1)] = var[i] * popsize * reps
        
        # still not sure how to calculate variance for this. Sixty is closish i think
        # and doesn't end up with too many failing tests.
        assert expecteds["aaaa"] - 60 < counts["aaaa"] < expecteds["aaaa"] + 60
        

    def test_fecundity_absolute_fitness(self):
        """ Tests that agents reproduce at the correct rate using absolute fitness. """
        
        reps = 1000
        popsize = 4       
        fecundity = 2
        popsizes = []
        for _ in range(reps):
            population = Population(1, 1, popsize)     
            k = 1
            for agent in population[0][0]:
                agent.dna.sequence = "a"*k
                agent.payoffs = [k]
                k += 1
            
            population.reproduce(fecundity = fecundity, relative_fitnesses = False)
            popsizes.append(len(population[0][0]))
        
        mean_popsize = sum(popsizes)/len(popsizes)
        payoffs = sum([1,2,3,4])/4/10
        expected_popsize = popsize + (payoffs * popsize * fecundity)
        
        # Again not sure the variacne, but this is close and results in mostly 
        # passing tests.
        assert expected_popsize - 1 < mean_popsize < expected_popsize + 1
            
            
            
        
        
            
            
        
            
        
        
        
        
        
        

               
    
        
        
        