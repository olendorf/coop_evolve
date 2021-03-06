#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

from app_settings import AppSettings
from numpy import random as nrand
from scipy.stats import nbinom
from scipy.stats import poisson


class Chromosome:
    """The genetics of the system."""
    
    def __init__(self, sequence = None):
        if sequence is not None: 
            self.sequence = sequence
            return
        
        cfg = AppSettings()
        self.sequence = ""
        p = cfg.chromosome_length/(1 + cfg.chromosome_length)
        
        while(random.random() <= p):
            self.sequence += random.choice(self.nucleotides())
    
    def substitutions(self):
        """
        Randomly changes charcters in the dna. 
        
        The number of substitutions us drawn from the poisson 
        distribution where mu = chromosome_length * mutation_rate.
        
        """
           
        cfg = AppSettings()
        num = poisson.rvs(cfg.mutation_rate * len(self.sequence))
        if len(self.sequence) > 0:
            positions = nrand.randint(0, len(self.sequence), size=num)
            for pos in positions:
                self.sequence = self.sequence[:pos] + \
                                random.choice(self.nucleotides()) + \
                                self.sequence[(pos + 1):]
                            
    def deletion(self):
        """
        Deletes a random sequence of characters from a random position on the string. 
           
        The lengt of the deletion h is taken from the negative binomial distribution.
        """
           
        # Prevents an out of bounds error for random.randint()
        if(len(self.sequence) == 0):
            return
        
        pos = random.randint(0, len(self.sequence) - 1)
        
        cfg = AppSettings()
        p = cfg.mutation_length/(1 + cfg.mutation_length)
        
        while(random.random() <= p):
            self.sequence = self.sequence[:pos] + self.sequence[(pos + 1):]
            
        
    def insertion(self):
        """
        
        Inserts a random length of random nucleotide characters into a sequence
        at a random location. 
        
        The position of the insertion is uniformly random across the sequence. The length 
        of the insertion is drawn from the negative binomial distribution.
        
        """
           
        if(len(self.sequence) <= 1):
            pos = 0
        else:
            pos = random.randint(0, len(self.sequence) - 1)
        
        cfg = AppSettings()
        p = cfg.mutation_length/(1 + cfg.mutation_length)
            
        while(random.random() <= p):
            self.sequence = self.sequence[:pos] + \
            random.choice(self.nucleotides()) + \
            self.sequence[pos:]
            
    
    def inversion(self):
        """
        Reverses the order of a random slice of the sequence. 
        
        The position
        on the string is randomly chosen from a uniform distribution. The length
        conforms to the negative binomial distribution.
        
        """
        
        if(len(self.sequence) <= 1):
            pos = 0
        else:
            pos = random.randint(0, len(self.sequence) - 1)
            
        cfg = AppSettings()
        p = cfg.mutation_length/(1 + cfg.mutation_length)
        
        length = nbinom.rvs(
            1, 
            cfg.mutation_length/(1 + cfg.mutation_length)
        )
        
        self.sequence = self.sequence[:pos] + \
                        self.sequence[pos:(pos + length)][::-1] + \
                        self.sequence[(pos + length):]
                        
    
    def mutate(self):
        self.substitutions()
        self.insertion()
        self.deletion()
        self.inversion()
        

        
    @staticmethod
    def crossover(dna1, dna2):
        """
        Swaps slices of sequence between the two sequences. 
        
        The number of swaps isinstance
        drawn from the poisson distribution, the position of each swap is random across the 
        shortest sequence.
        
        Parameters
        ----------
        dna1: Chromosome
            A chromosome to be crosse dover
        dna2: Chromosome
            A chromosome to be crossed over
        """
        
        cfg = AppSettings()
        min_len =  len(min([dna1.sequence, dna2.sequence], key=len)) 
        num = poisson.rvs(cfg.crossover_rate * min_len)
        
        if min_len > 0:
            
             
            positions = nrand.randint(0, min_len , size=num)
            
            for pos in positions:
                seq1 = dna1.sequence
                dna1.sequence = dna1.sequence[:pos] + dna2.sequence[pos:]
                dna2.sequence = dna2.sequence[:pos] + seq1[pos:]
        

    @staticmethod
    def nucleotides():
        """Returns all the nucleotides that can be used in a dna string"""
        cfg = AppSettings()
        return(
            cfg.behaviors + 
            cfg.gene_delimiter + 
            cfg.receptor_delimiter + 
            cfg.wildcards
            )
    
    @staticmethod
    def default_behavior():
        """Returns the last nucleotide which is the default behavior."""
        cfg = AppSettings()
        return cfg.behaviors[-1]
        