# -*- coding: utf-8 -*-

import random
import re

from app_settings import AppSettings

from coop_evolve.chromosome import Chromosome

class Agent:
    """
    The things that play the game with each other.
    """
    
    strategy_regex = '(?P<receptor>[abcd?*+]+):[*?+:]*(?P<effector>[abcd])[abcd?*+:]*/'
    
    def __init__(self, sequence = None):
        self.dna = Chromosome(sequence)
        self.payoffs = []
        
    def strategy(self):
        """
        Returns a list of (receptor, effector) pairs that represent the agent's 
        strategy. 
        
        The chromosome is parses using the regular expression 
        (?P<receptor>[abcd?*+]+):[*?+:]*(?P<effector>[abcd])[abcd?*+:]*/
        
        
        """
        return re.findall(self.strategy_regex, self.dna.sequence)
        
    def response(self, history):
        """ Gets the agent's response based on the provided history based on the agent's dna."""
        
        strategy = self.strategy()
        receptor_regex = re.compile("([?*+])")
        for move in strategy:
            move_regex = "^" + re.sub(receptor_regex, r"[abcd]\g<1>", move[0]) + "$"
            
            if re.match(move_regex, history) != None:
                return move[1]
                
        
        return Chromosome.default_behavior()
        
    def fitness(self):
        cfg = AppSettings()
        if len(self.payoffs) == 0:
            return sum(cfg.payoffs.values())/len(cfg.payoffs)
        else:
            return sum(self.payoffs)/len(self.payoffs)
        
    @staticmethod
    def interact(agent1, agent2):
        """ 
        Has the agents play the game. 
        
        The agents play the game based on the interaction_length specified
        in settings. The length is a random number drawn from the negative 
        binomial distribution.
        
         Parameters
        ----------
        agent1: Agent
            One agent to interact
        agent2: Agent
            The other interacting agent. 
        """
        cfg = AppSettings()
        p = cfg.interaction_length/(1 + cfg.interaction_length)
        
        history1 = ""
        history2 = ""
        
        while(random.random() <= p):
            history1 += agent1.response(history2)
            history2 += agent2.response(history1)

            # print(history1)
            # print(history2)
            
            agent1.payoffs.append(Agent.payoff(history2[-1] + history1[-1]))
            agent2.payoffs.append(Agent.payoff(history1[-1] + history2[-1]))
    
    @staticmethod
    def payoff(moves):
        cfg = AppSettings()
        
        if moves in cfg.payoffs:
            return cfg.payoffs[moves]
        else:
            return 0
        
        
        
            