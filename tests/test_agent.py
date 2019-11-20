#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `coop_evolve.agent Agent` class."""

import pytest

from coop_evolve.agent import Agent
from coop_evolve.chromosome import Chromosome

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
        
class TestGentesponse:
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
        