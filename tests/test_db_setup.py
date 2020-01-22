#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psycopg2
import pytest

from app_settings import AppSettings

from coop_evolve.db_setup import DB_Setup

class TestDBSetup:
    def test_clean_setup(self):        
        cfg = AppSettings()
        
        setup = DB_Setup()
        conn = psycopg2.connect(
            f"dbname= '{cfg.database}' " + 
            f"user='{cfg.db_user}' " + 
            f"password={cfg.db_password} " + 
            f"host=localhost"
        )
        cur = conn.cursor()
        
        
        cur.execute(f"DROP SCHEMA IF EXISTS {cfg.schema_name} CASCADE")
        conn.commit()
        
        setup.setup()
        
        cur.execute(
            "SELECT t.table_name FROM information_schema.tables t WHERE t.table_schema = 'test' AND t.table_type = 'BASE TABLE'"
        )
        
        result = [ table[0] for table in cur.fetchall() ]
        result.sort()
        expected = ['runs', 'subpop_data', 'experiments', 'pop_data']
        expected.sort()
        assert result == expected
        
        

class TestDBReset:
    
    def test_table_creation(self):
        cfg = AppSettings()
        
        setup = DB_Setup()
        setup.reset()
        
        conn = psycopg2.connect(
            f"dbname= '{cfg.database}' " + 
            f"user='{cfg.db_user}' " + 
            f"password={cfg.db_password} " + 
            f"host=localhost"
        )
        cur = conn.cursor()
        
        
        cur.execute(
            "SELECT t.table_name FROM information_schema.tables t WHERE t.table_schema = 'test' AND t.table_type = 'BASE TABLE'"
        )
        
        result = [ table[0] for table in cur.fetchall() ]
        result.sort()
        expected = ['runs', 'subpop_data', 'experiments', 'pop_data']
        expected.sort()
        assert result == expected
        
    def test_subpop_data_table(self):
        cfg = AppSettings()
        
        setup = DB_Setup()
        setup.reset()
        
        conn = psycopg2.connect(
            f"dbname= '{cfg.database}' " + 
            f"user='{cfg.db_user}' " + 
            f"password={cfg.db_password} " + 
            f"host=localhost"
        )
        cur = conn.cursor()
        
        cur.execute(
            "SELECT column_name FROM information_schema.columns WHERE table_schema = 'test' AND table_name   = 'subpop_data'"
        )
        result = [item[0] for item in cur.fetchall()]
        result.sort()
        expected = ['id', 'run_id', 'generation', 'x_coord', 'y_coord', 'mean_fitness', 'behavior', 'census']
        expected.sort()
        assert result == expected
                
    def test_simulations_table(self):
        cfg = AppSettings()
        
        setup = DB_Setup()
        setup.reset()
        
        conn = psycopg2.connect(
            f"dbname= '{cfg.database}' " + 
            f"user='{cfg.db_user}' " + 
            f"password={cfg.db_password} " + 
            f"host=localhost"
        )
        cur = conn.cursor()
        
        cur.execute(
            "SELECT column_name FROM information_schema.columns WHERE table_schema = 'test' AND table_name = 'experiments'"
        )
        result = [item[0] for item in cur.fetchall()]
        result.sort()
        expected = ['id', 'behaviors', 'gene_delimiter', 'wild_cards', 'chromosome_length', 'mutation_rate', 'crossover_rate', 'interaction_length']
        expected.sort()
        assert result == expected
        
    def test_pop_data_table(self):
        cfg = AppSettings()
        
        setup = DB_Setup()
        setup.reset()
        
        conn = psycopg2.connect(
            f"dbname= '{cfg.database}' " + 
            f"user='{cfg.db_user}' " + 
            f"password={cfg.db_password} " + 
            f"host=localhost"
        )
        cur = conn.cursor()
        cur.execute(
            "SELECT column_name FROM information_schema.columns WHERE table_schema = 'test' AND table_name = 'pop_data'"
        )
        result = [item[0] for item in cur.fetchall()]
        result.sort()
        expected = ['id', 'run_id', 'generation', 'mean_fitness', 'behavior', 'census']
        expected.sort()
        assert result == expected
        
    def test_runs_table(self):
        cfg = AppSettings()
        
        setup = DB_Setup()
        setup.reset()
        
        conn = psycopg2.connect(
            f"dbname= '{cfg.database}' " + 
            f"user='{cfg.db_user}' " + 
            f"password={cfg.db_password} " + 
            f"host=localhost"
        )
        cur = conn.cursor()     
        
        cur.execute(
            "SELECT column_name FROM information_schema.columns WHERE table_schema = 'test' AND table_name   = 'runs'"
        )
        result = [item[0] for item in cur.fetchall()]
        result.sort()
        expected = ['id', 'simulation_id', 'generations', 'width', 'length', 'subpop_size', 'relative_fitnesses', 
                    'migration_distance', 'migration_survival', 'initial_sequence']
        expected.sort()
        assert result == expected
        
