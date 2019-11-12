#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import statistics
import time

from app_settings import AppSettings
from coop_evolve.genetics.chromosome import Chromosome



class Reporter:
    
    def generate(self):
        
        dna = Chromosome()
        cfg = AppSettings()
        
        if not os.path.exists("reports"):
            os.makedirs("reports")
            
        f = open( "reports/_" + str(int(time.time())) + ".txt", "w")
        f.write(
            "==========================\n" + 
            "==========================\n" +
            "==\n"
            "== Genetics\n\n" + 
            "nucleotides: " + dna.nucleotides() + "\n" + 
            "expected length: " + str(cfg.genetics.chromosome_length) + "\n\n" + 
            "Examples: \n"
        )
        for i in range(1, 10):
            dna = Chromosome()
            f.write(dna.sequence + "\n")
            
        lengths = []
        for i in range(1, 1000):
            dna = Chromosome()
            lengths.append(len(dna.sequence))
            
        f.write(f"\n\nmean_length (standard deviation):  " + \
                f"{statistics.mean(lengths)} " + \
                f"({statistics.stdev(lengths)})")
        f.close()