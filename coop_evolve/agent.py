# -*- coding: utf-8 -*-
import re

from coop_evolve.chromosome import Chromosome

class Agent:
    """
    The things that play the game with each other.
    """
    
    strategy_regex = '(?P<receptor>[abcd?*+]+):[*?+:]*(?P<effector>[abcd])[abcd?*+:]*/'
    
    def __init__(self, sequence = None):
        self.dna = Chromosome(sequence)
        
    def strategy(self):
        """
        Returns a list of (receptor, effector) pairs that represent the agent's 
        strategy. 
        
        The chromosome is parses using the regular expression 
        (?P<receptor>[abcd?*+]+):[*?+:]*(?P<effector>[abcd])[abcd?*+:]*/
        
        
        """
        return re.findall(self.strategy_regex, self.dna.sequence)
        
    def response(self, history):
        strategy = self.strategy()
        receptor_regex = re.compile("([?*+])")
        for move in strategy:
            move_regex = "^" + re.sub(receptor_regex, r"[abcd]\g<1>", move[0]) + "$"
            print(move_regex)
            
            if re.match(move_regex, history) != None:
                return move[1]
                
        
        return Chromosome.default_behavior()
            