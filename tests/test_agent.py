#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `coop_evolve.agent Agent` class."""

import pytest

from app_settings import AppSettings

from coop_evolve.agent import Agent
from coop_evolve.chromosome import Chromosome

from scipy.stats import nbinom

class TestAgentCreation:
    """ Test agent creation and initialization """
    
    def test_has_chromosome(self):
        """ Tests that an agent has a chromosome """
        agent = Agent()
        assert agent.dna.__class__.__name__ == "Chromosome"
        
    def test_specific_sequence(self):
        """ Tests that an agent is made with the correct specified sequence"""
        agent = Agent(sequence = "abcd")
        assert agent.dna.sequence == "abcd"
        
class TestAgentStrategy:
    """ Tests method(s) related to the strategy """
    
    def test_strategy_with_match(self):
        """Tests a known sequence """
        agent = Agent(sequence = "*c:c/")
        assert agent.strategy() == [('*c', 'c')]
        
    def test_strategy_no_match(self):
        """ Tests no match strategy """
        agent = Agent(sequence = "")
        assert agent.strategy() == []
        
class TestAgentResponse:
    """ Tests that the correct response is returned for a given interaction history"""
    
    def test_receptor_matched(self):
        """ Test the correct response is given when a receptor is matched """
        
        agent = Agent("*c:c/*d:+?d/aac*:*a/")
        his1 = "aabc"
        his2 = "aabd"
        his3 = "aacb"
        his4 = "bbbb"
        
        assert agent.response(his1) == "c"
        assert agent.response(his2) == "d"
        assert agent.response(his3) == "a"
        assert agent.response(his4) == Chromosome.default_behavior()
        
class TestAgentInteraction:
    """ Tests two agents playing the game """
    
    def test_interaction_length(self):
        """ Tests that agents have the expected number of interactions """
        
        cfg = AppSettings()
        reps = 1000
        
        lengths = []
        diffs = []
        
        for _ in range(0, reps):
            agent1 = Agent("*d:d/*:c/")
            agent2 = Agent("*:d/")
            Agent.interact(agent1, agent2)
            
            lengths.append(len(agent1.payoffs))
            diffs.append( abs(len(agent1.payoffs) - len(agent2.payoffs)) )
        
        
        assert sum(diffs) == 0
        
        mean_length = sum(lengths)/len(lengths)
        expected_length = cfg.interaction_length
        
        p = 1 - (expected_length/(1 + expected_length))
        conf_99 =(nbinom.var(1, p)/reps)**(1/2) * 5
        assert (
            expected_length- conf_99
            ) <= mean_length <= (
                expected_length + conf_99
                )
                
    def test_interaction_payoffs(self):  
        """ Test the the payoffs and fitness generated from an interaction are correct."""
        
        cfg = AppSettings()
        reps = 1000
        
        # Generate the observed fitness. Fitness is the 
        # mean payoff.
        fitnesses1 = []
        fitnesses2 = []
        for _ in range(0, reps):
            agent1 = Agent("*d:d/*:c/")
            agent2 = Agent("*:d/")
            Agent.interact(agent1, agent2)
            fitnesses1.append(agent1.fitness())
            fitnesses2.append(agent2.fitness())
            
        p = 1 - cfg.interaction_length/(1 + cfg.interaction_length)
            
        # Calculating the expected fitness for each dna
        # based on the fitness for the number of interactions
        # times the probability of that interaction length
        pmfs = []
        k = 0
        expected_fitness1 = 0
        expected_fitness2 = 0
        
        # If zero plays (interaction length) the mean of the 
        # matrix cells are used.
        pmf = nbinom.pmf(k, 1, p)
        matrix_mean = sum(cfg.payoffs.values())/len(cfg.payoffs)
        expected_fitness1 += (matrix_mean * pmf)
        expected_fitness2 += (matrix_mean * pmf)
        pmfs.append(pmf)
        k += 1
        
        # Calculate the rest of the weighted fitnesses.
        while sum(pmfs) < 0.9999:
            pmf = nbinom.pmf(k, 1, p)
            
            # for agent 1 (tft) we know the first move
            # will be zero, then 3 after that.
            expected_fitness1 +=  pmf * ((k - 1) * 3)/k 
            
            # agent 2 (d) gets 10 on the first move then
            # three after that.
            expected_fitness2 +=  pmf * (10 + ((k-1) * 3))/k 
            
            pmfs.append(pmf)
            k += 1
            
        fitness1 = sum(fitnesses1)/len(fitnesses1)
        fitness2 = sum(fitnesses2)/len(fitnesses2)
        
        conf_99 = ((nbinom.var(1, p) * 3**2)/reps)**(1/2) * 5
        
        assert expected_fitness1 - conf_99 < fitness1 < expected_fitness1 + conf_99
        assert expected_fitness2 - conf_99 < fitness2 < expected_fitness2 + conf_99
            
                
        
            

class TestFitness:
    """ Test the fitness method"""
    
    def test_payoffs_length_greater_than_zero(self):
        agent = Agent()
        payoffs = [1, 2, 3, 4, 5, 6]
        agent.payoffs = payoffs
        assert agent.fitness() == sum(payoffs)/len(payoffs)
        
    def test_payoffs_length_zero(self):
        cfg = AppSettings()
        agent = Agent()
        assert agent.fitness() == sum(cfg.payoffs.values())/len(cfg.payoffs)
        
        
    
class TestPayOff:
    """ Tests the payoff method """
    
    def test_moves_match(self):
        assert Agent.payoff("dd") == 3
        assert Agent.payoff("cd") == 10
        
    def test_move_not_matched(self):
        assert Agent.payoff("aa") == 0
        
class TestReset:
    """ Tests reset method """
    
    def test_payoff_reset(self):
        agent = Agent()
        agent.payoffs = [1, 2, 3]
        
        agent.reset()
        
        assert len(agent.payoffs) == 0
        
        