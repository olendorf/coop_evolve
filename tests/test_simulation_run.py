#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pytest

from coop_evolve.simulation_run import SimulationRun

class TestSimulationRunCreation:
    
    def test_defaults(self):
        run = SimulationRun()
        
        assert run.generations == 10000
        assert run.width == 100
        assert run.length == 100
        assert run.subpop_size == 100
        assert run.relative_fitnesses == True
        assert run.migration_survival == 0.1
        assert run.migration_distance == 1