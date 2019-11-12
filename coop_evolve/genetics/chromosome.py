# -*- coding: utf-8 -*-

import random

from app_settings import AppSettings
from numpy import random as nrand
from scipy.stats import poisson


class Chromosome:
    """The genetics of the system."""
    
    def __init__(self, sequence = None):
        if sequence is not None: 
            self.sequence = sequence
            return
        
        cfg = AppSettings()
        self.sequence = ""
        p = cfg.genetics.chromosome_length/(1 + cfg.genetics.chromosome_length)
        
        while(random.random() <= p):
            self.sequence += random.choice(self.nucleotides())
    
    def substitutions(self):
        """Randomly changes charcters in the dna according to the poisson 
           distribution. expected changes length * mutation rate * nonsynomous
           substitutions."""
           
        cfg = AppSettings()
        num = poisson.rvs(cfg.genetics.mutation_rate * len(self.sequence))
        positions = nrand.randint(0, len(self.sequence), size=num)
        for pos in positions:
            self.sequence = self.sequence[:pos] + \
                            random.choice(self.nucleotides()) + \
                            self.sequence[(pos + 1):]
                            
    def deletion(self):
        """Deletes a random sequence of characters from a random position on the string. 
           The length is taken from the negative binomial distribution."""
           
        # Prevents an out of bounds error for random.randint()
        if(len(self.sequence) == 0):
            return
        
        pos = random.randint(0, len(self.sequence) - 1)
        
        cfg = AppSettings()
        p = cfg.genetics.mutation_length/(1 + cfg.genetics.mutation_length)
        
        while(random.random() <= p):
            self.sequence = self.sequence[:pos] + self.sequence[(pos + 1):]
            
        
    def insertion(self):
        """Inserts a random length of random nucleotide characters into a sequence
           at a random location. """
           
        if(len(self.sequence) <= 1):
            pos = 0
        else:
            pos = random.randint(0, len(self.sequence) - 1)
        
        cfg = AppSettings()
        p = cfg.genetics.mutation_length/(1 + cfg.genetics.mutation_length)
            
        while(random.random() <= p):
            self.sequence = self.sequence[:pos] + \
            random.choice(self.nucleotides()) + \
            self.sequence[pos:]
        
        

    @staticmethod
    def nucleotides():
        """Returns all the nucleotides that can be used in a dna string"""
        cfg = AppSettings()
        return(
            cfg.genetics.behaviors + 
            cfg.genetics.gene_delimiter + 
            cfg.genetics.receptor_delimiter + 
            cfg.genetics.wildcards
            )
        