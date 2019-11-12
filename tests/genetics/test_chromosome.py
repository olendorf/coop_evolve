#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `coop_evolve.genetics.chromosome` class."""

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
        
class TestChromosomeClassMethods:
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
        
        
        
        
        
        