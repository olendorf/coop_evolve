#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import statistics
import time

from app_settings import AppSettings
from coop_evolve.chromosome import Chromosome
from os import listdir



class Reporter:
    
    def generate(self):
        
        dna = Chromosome()
        cfg = AppSettings()
        
        print("making files")
        
        if not os.path.exists(cfg.report_directory):  # pragma: no cover
            os.makedirs(cfg.report_directory)
            
        print(cfg)
        print(listdir('.'))
        print(listdir(cfg.report_directory))
            
        f = open( cfg.report_directory + "/_" + str(int(time.time())) + ".txt", "w")
        f.write(
            "==========================\n" + 
            "==========================\n" +
            "==\n"
            "== Genetics\n\n" + 
            "nucleotides: " + dna.nucleotides() + "\n" + 
            "expected length: " + str(cfg.chromosome_length) + "\n\n" + 
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