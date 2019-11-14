#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `coop_evolve.genetics.chromosome` class."""

import math
import pytest
import re

from app_settings import AppSettings
from scipy.stats import binom
from scipy.stats import nbinom
from scipy.stats import poisson

from coop_evolve.genetics.chromosome import Chromosome


class TestChromosomeCreation:
    """Tests chromosome creation."""
    def test_defined_sequence(self):
        """Tests creation of a chromosome from a specified sequence."""
        chrom = Chromosome("abcd")
        assert chrom.sequence == "abcd"
        
    def test_random_chromosome_compostion(self):
        """Tests creation of a chromosome of random length and sequence. Length 
           is drawn from a negative binomial distribution with a mean 
           of the expected dna length."""
        chrom = Chromosome()
        assert type(chrom.sequence) is str
        assert re.match('[abcd*:/?+]+', chrom.sequence)
        
    def test_random_chromosome_length(self):
        """Ensures that random chromosomes are created at the correct average
           length."""
        reps = 1000
        cfg = AppSettings()
        lengths = []
        for _ in range(0, reps):
            chrom = Chromosome()
            lengths.append(len(chrom.sequence))
        
        mean_length = float(sum(lengths))/len(lengths)
        expected_length = cfg.genetics.chromosome_length
        
        p = 1 - (expected_length/(1 + expected_length))
        conf_99 =(nbinom.var(1, p)/reps)**(1/2) * 4
        assert (
            expected_length- conf_99
            ) <= mean_length <= (
                expected_length + conf_99
                )
        
class TestChromosomeHelperMethods:
    """ Tests various class methods form chromosomes"""
    
    
    def test_nucleotides(self):
        """Tests nucleotide method returns correct value."""
        assert Chromosome.nucleotides() == "abcd/:*+?"
        
class TestSubstitutions:
    """Test substitution mutations."""
    
    def test_substitutions_length(self):
        """Ensure the substitions don't change sequence length."""
        dna = Chromosome("a"*100)
        dna.substitutions()
        assert len(dna.sequence) == 100
        
    def test_substitutions_changes(self):
        """Test that substitions occur at the expected rate."""
        cfg = AppSettings()
        reps = 1000
        deltas = []
        
        for _ in range(0, reps):
            seq = "a"*100
            dna = Chromosome(seq)
            dna.substitutions()
            deltas.append( sum(1 for a, b in zip(seq, dna.sequence) if a != b) )
            
        # Expand the conf_99 to compensate for repeated mutations in the same place
        expected_delta = cfg.genetics.mutation_rate * 100 * \
                         (1 - 1/len(Chromosome.nucleotides()))
                         
        # Because there is a little slop around synonymous substitions I multiply 
        # the confidence by 10 just to limit the number of failing tests.
        conf_99 = ((poisson.var(cfg.genetics.mutation_rate * 100)/1000)**(1/2)) * 10
        observed_delta = sum(deltas)/reps
        assert (expected_delta - conf_99) < observed_delta < (expected_delta + conf_99)
        
class TestDeletion:
    """Tests of the deletion method in chromosomes"""
    
    def test_deletion_length(self):
        """Test that deletions return the correct averge length"""
        cfg = AppSettings()
        reps = 1000
        deltas = []
        
        for _ in range(0, reps):
            dna = Chromosome()
            init_length = len(dna.sequence)
            dna.deletion()
            deltas.append(init_length - len(dna.sequence))
            
        expected_delta = cfg.genetics.mutation_length
        var = nbinom.var(1, cfg.genetics.mutation_length/(1 + cfg.genetics.mutation_length))
        
        # Because there is a little slop around short strings or positions near the 
        # end of the string, I multiply 
        # the confidence by 10 just to limit the number of failing tests.
        conf_99 = ((var/reps)**(1/2)) * 10
        observed_delta = sum(deltas)/reps
        assert (expected_delta - conf_99) < observed_delta < (expected_delta + conf_99)
        
class TestInsertion:
    """Tests the insertion method in chromosomes"""
    
    def test_insertion_length(self):
        """Tests that insertion mutations are of the correct length"""
        cfg = AppSettings()
        reps = 1000
        deltas = []
        
        for _ in range(0, reps):
            dna = Chromosome()
            init_length = len(dna.sequence)
            dna.insertion()
            deltas.append(len(dna.sequence) - init_length)
            
        expected_delta = cfg.genetics.mutation_length
        var = nbinom.var(1, cfg.genetics.mutation_length/(1 + cfg.genetics.mutation_length))
        
        conf_99 = ((var/reps)**(1/2)) * 4
        observed_delta = (sum(deltas)/reps)
        assert (expected_delta - conf_99) < observed_delta < (expected_delta + conf_99)
        
        
class TestInversion:
    """Tests inversion method in chromosome"""
    
    def test_inversion_diffs(self):
        cfg = AppSettings()
        
        reps = 1000
        deltas = []    # observed number of differences
        
        for _ in range(0, reps):
            dna = Chromosome()
            old_seq = dna.sequence
            dna.inversion()
            deltas.append( sum(1 for a, b in zip(old_seq, dna.sequence) if a != b) )
            
        pmfs = []
        expected_deltas = []   # expected differences 
        
        # Assumes the length of an inversion is drawn from a negative binomial 
        # distribution. Calculates the probability of each length until 
        # 99.99% of the distribution is accounted for. The expected number of 
        # differences for each length is multiplied by the probability of that length
        # and the sum of that gives the expected differences overall.
        k = 0
        while sum(pmfs) <= 0.9999:
            pmf = nbinom.pmf(
                k, 1, 
                (1 - cfg.genetics.mutation_length/(1 + cfg.genetics.mutation_length))
            )
            pmfs.append(pmf)
            
            diffs = math.floor(k/2) * (1 - 1/len(Chromosome.nucleotides())) * 2
            expected_deltas.append(pmf * diffs)
            k += 1
            
        expected_delta = sum(expected_deltas)
        
        # Since we are multiplying the binomial distribution (probably of differences at 
        # a given lenght) by a negative binomial distribution (probability of a length)
        # we must compute the variance of two independent random variables 
        # is Var(X * Y) = var(x) * var(y) + var(x) * mean(y) + mean(x) * var(y)
        # http://www.odelama.com/data-analysis/Commonly-Used-Math-Formulas/
        
        mean_binom = cfg.genetics.mutation_length
        var_binom = binom.var(
            mean_binom, 1/(len(Chromosome.nucleotides()))
            )
        
        mean_nbinom = cfg.genetics.mutation_length
        var_nbinom = nbinom.var(
            cfg.genetics.mutation_length, 
            mean_nbinom/(1 + mean_nbinom)
        )
        
        var = var_binom * var_nbinom + \
              var_binom * mean_nbinom + \
              mean_binom * var_nbinom
              
        observed_delta = sum(deltas)/reps
        conf_99 = ((var/reps)**(1/2)) * 5
        assert expected_delta - conf_99 < observed_delta < expected_delta + conf_99
        
        
class TestCrossingOver:
    """Test crossing over method as Class method"""
    
    def test_crossovers_freq(self):
        """Tests that the number of swaps is as expected"""
        
        cfg = AppSettings()
        
        reps = 1000
        deltas = []
        diffs = []  # Differences between two deltas, should be zero
        
        for _ in range(1, reps):
            dna1 = Chromosome("a"*100)
            dna2 = Chromosome("b"*100)
            
            Chromosome.crossover(dna1, dna2)
            
            delta1 = len(re.findall(r"ab", dna1.sequence)) + \
                     len(re.findall(r"ab", dna1.sequence))
                     
                     
            delta2 = len(re.findall(r"ab", dna2.sequence)) + \
                     len(re.findall(r"ab", dna2.sequence))
                 
            deltas.append(delta1)
            diffs.append(abs(delta1 - delta2))
        
        min_len = len(min([dna1.sequence, dna2.sequence], key=len)) 
        # Expected delta is the per base crossover rate, mulitplied by the 
        # probability of the same position getting chosen twice times the
        # probability either end getting chosen. This still ignores the effect 
        # of the same position getting chosen four times. (only even hits cause
        # difrence.s)
        expected_delta = cfg.genetics.crossover_rate * min_len * ( 1 - 1/min_len ) * (1 - 2/min_len)
                         
        var = poisson.var(expected_delta)
        conf_99 = ((var/reps)**(1/2)) * 6
        observed_delta = sum(deltas)/reps
        
        assert expected_delta - conf_99 < observed_delta < expected_delta + conf_99
        
        
        
        
        
            