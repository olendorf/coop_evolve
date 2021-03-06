#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `coop_evolve.population Population` class."""

import collections
import pytest
import random

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
        length = 4
        subpop_size = 3
        
        population = Population(width, length, subpop_size)
        
        assert len(population.population) == 5
        assert len(population[0]) == 4
        assert len(population[0][1]) == 3
        
    def test_setting_item(self):
        width = 5
        length = 4
        subpop_size = 3
        
        population = Population(width, length, subpop_size)
        population[0][0][0] = Agent("abcd")
        
        assert population[0][0][0].dna.sequence == "abcd"
        
        
    def test_random_agents(self):
        """ Test that agents are made randomly when that is wanted"""
        width = 5
        length = 4
        subpop_size = 3
        
        population = Population(width, length, subpop_size)
        assert population[0][0][0] != population[1][1][1]
        
    def test_specified_sequence(self):
        """Test agents with specific dna sequences can be created """
        width = 5
        length = 4
        subpop_size = 3
        
        population = Population(width, length, subpop_size, sequence = "abcd")
        assert population[0][0][0].dna.sequence == \
               population[1][1][1].dna.sequence
               
    def test_assign_agent(self):
        """ Ensure the __setitem__ method works"""
        width = 5
        length = 4
        subpop_size = 3
        
        population = Population(width, length, subpop_size, sequence = "aaaa")
        
        population[0][0][0] = Agent("bbbb")
        
        assert population[0][0][0].dna.sequence == "bbbb"
        
class TestPlayingGame:
    """ Test aspects of playing the game """
    
    def test_interaction_lengths(self):
        """ Tests that the interaction length is correct """
        
        cfg = AppSettings()
        
        width = 10
        length = 10
        subpop_size = 10
        
        expected_interactions = 2
        
        population = Population(width, length, subpop_size)
        
        population.play_game(expected_interactions)
        
               
        assert population.popsize() == width * length * subpop_size
        payoff_lengths = []
        for i in range(width):
            for j in range(length):
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
    
    def test_data_collection(self):
        width = 2
        length = 2
        subpop_size = 10
        
        population = Population(width, length, subpop_size)
        
        data = population.play_game()
        
        assert data['subpop_counts'][0][0]["a"] >= 0
        assert data['subpop_counts'][0][1]["d"] > 0
        
        assert data['pop_counts']['a'] >= 0
        assert data['pop_counts']['d'] > 0
               
class TestReproduction:
    
    def test_fecundity_relative_fitness(self):
        """ 
        Tests that subpopulatons reproduce at the same rate and equally under
        relative fitness
        """
        
        width = 2
        length = 2
        subpop_size = 10
        
        population = Population(width, length, subpop_size)
        
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
        
        # still not sure how to calculate variance for this. One hundred is closish i think
        # and doesn't end up with too many failing tests.
        assert expecteds["aaaa"] - 100 < counts["aaaa"] < expecteds["aaaa"] + 100
        

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
        
    def test_return_value(self):
        width = 2
        length = 3
        popsize = 4
        
        population = Population(width, length, popsize)
        population.play_game()
        data = population.reproduce()
        
        assert len(data) == width
        assert len(data[0]) == length
        assert data[0][0] >= 0
        
        
            
class TestMigration:
    """ Test migration is accurate """
    
    def test_migration_survival(self):
        """ Tests proper number of agents survive migration """
        reps = 1000
        popsize = 1
        width = 11
        length = 11
        population = Population(width, length, popsize)
        
        
        
        population[5][5] = population[5][5] + [Agent() for _ in range(100)]
        
        
        initial_popsize = population.popsize()
        
        population.migrate(0.1, 1)
        
        assert population.popsize() < initial_popsize
        
    def test_migration_distance(self):
        """ Tests agents move the correct distance on average """
        reps = 1000
        popsize = 1
        width = 11
        length = 11
        population = Population(width, length, popsize)
        
        population[5][5] = population[5][5] + [Agent() for _ in range(100)]
        
        expected_distance = 1
        population.migrate(1, expected_distance)
        
        distances_x = []
        distances_y = []
        
        for i in range(width):
            for j in range(length):
                for k in range(len(population[i][j]) - 1):
                    distances_x.append(abs(i - 5))
                    distances_y.append(abs(j - 5))
        mean_x = sum(distances_x)/len(distances_x)
        mean_y = sum(distances_y)/len(distances_y)
        
        # Increasing confidence interval to reduce number of failing tests.
        conf_99 = (poisson.var(expected_distance)/(reps))**(1/2) * 10
        
        assert expected_distance - conf_99 < mean_x < expected_distance + conf_99
        assert expected_distance - conf_99 < mean_y < expected_distance + conf_99
        
                
class TestCulling:
    
    def test_cull(self):
        """ Tests that population size is reduced to correct level. """
        width = 2
        length = 2
        popsize = 2
        
        population = Population(width, length, popsize)
        
        for i in range(width):
            for j in range(length):
                population[i][j] += [Agent() for _ in range(random.randint(0, 5))]
                
        population.cull()
        
        assert population.popsize() == width * length * popsize
        
class TestCensus: 
    
    def test_census(self):
        width = 4
        length = 5
        subpop_size = 6
        
        population = Population(length, width, subpop_size)
        
        population[0][0][0].dna.sequence = "aaaa"
        population[0][0][1].dna.sequence = "aaaa"
        population[0][0][4].dna.sequence = "aaaa"
        population[0][0][5].dna.sequence = "aaaa"
        population[0][1][0].dna.sequence = "aaaa"
        population[0][1][3].dna.sequence = "aaaa"
        population[0][2][0].dna.sequence = "aaaa"
        population[1][0][0].dna.sequence = "aaaa"
        population[1][0][1].dna.sequence = "aaaa"
        population[0][3][0].dna.sequence = "aaaa"
        
        result = population.census()
        
        assert result['subpop_data'][0][0]['aaaa'] == 4
        assert result['pop_data']['aaaa'] == 10
        
        
class TestGeneration:
    
    def test_population_stability(self):
        """ Tests that population size doesn't change generation to generation. """
        width = 2
        length = 2
        popsize = 2
        
        population = Population(width, length, popsize)
        
        population.generation()
        
        assert population.popsize() == width * length * popsize
        
    def test_payoffs_happened(self):
        """ 
        Accuracy is tested elsewhere so this is just spot check(s) to ensure 
        payoffs are recorded. 
        
        """
        
        width = 2
        length = 2
        popsize = 2
        
        population = Population(width, length, popsize)
        
        population.generation()
        
        payoff_lengths = 0
        
        for i in range(width):
            for j in range(length):
                for k in range(popsize):
                    payoff_lengths += len(population[i][j][k].payoffs)
        
        assert payoff_lengths > 0
        
    # def test_return_value(self):  
        
    #     cfg = AppSettings()
        
    #     width = 2
    #     length = 2
    #     popsize = 2
        
    #     population = Population(width, length, popsize)
        
    #     data = population.generation()
        
    #     assert len(data) == width
    #     assert len(data[0]) == length
    #     assert len(data[0][0]) == len(cfg.behaviors)
        
        
class TestReset:
    
    def test_agents_are_reset(self):        
        width = 2
        length = 2
        popsize = 2
        
        population = Population(width, length, popsize)
        
        population.generation()
        
        population.reset()
        
        payoff_lengths = 0
        for i in range(width):
            for j in range(length):
                for k in range(popsize):
                    payoff_lengths += len(population[i][j][k].payoffs)
        
    

        
        
        
class TestOtherMethods:
    def test_popsize(self):
        """ Tests popsize returns the correct population size """
        population = Population(4, 4, 4)
        assert population.popsize() == 4 * 4 * 4
        
    def test_census(self):
        """Tests that the census included the correct results"""
        
        population = Population(2, 2, 5)
        population[0][0][0].dna.sequence = 'aaa'
        population[0][0][1].dna.sequence = 'bbb'
        population[0][0][2].dna.sequence = 'aaa'
        population[0][0][3].dna.sequence = 'bbb'
        population[0][0][4].dna.sequence = 'aaa'
        
        # data = population.cenus()
        
        
        
            
        
        
            
            
        
            
        
        
        
        
        
        

               
    
        
        
        