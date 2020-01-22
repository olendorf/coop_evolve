#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psycopg2

from app_settings import AppSettings

class DB_Setup:
    
    def __init__(self):
        pass
    
    def reset(self):
        cfg = AppSettings()        
        conn = psycopg2.connect(
            f"dbname= '{cfg.database}' " + 
            f"user='{cfg.db_user}' " + 
            f"password={cfg.db_password} " + 
            f"host=localhost"
        )
        cur = conn.cursor()
        print("cursor created")
        
        
        cur.execute(f"DROP SCHEMA IF EXISTS {cfg.schema_name} CASCADE")
        
        print("query executed")
        
        # cur.execute("CREATE SEQUENCE test.serial START 101")
        conn.commit()
        cur.close()
        conn.close()
        
        
        self.setup()
        
    def setup(self):
        cfg = AppSettings()        
        conn = psycopg2.connect(
            f"dbname= '{cfg.database}' " + 
            f"user='{cfg.db_user}' " + 
            f"password={cfg.db_password} " + 
            f"host=localhost"
        )
        cur = conn.cursor()
        print("cursor and conn set")
        
        query = f"CREATE SCHEMA IF NOT EXISTS {cfg.schema_name}"
                
        cur.execute(query)
        
        print("schema created")
        
        query = f"CREATE TABLE IF NOT EXISTS {cfg.schema_name}.experiments( \
                id SERIAL PRIMARY KEY, \
                behaviors VARCHAR(16), \
                gene_delimiter CHAR(1), \
                wild_cards VARCHAR(4), \
                chromosome_length INTEGER, \
                mutation_rate REAL, \
                crossover_rate REAL, \
                interaction_length INTEGER \
                );\
                CREATE TABLE IF NOT EXISTS {cfg.schema_name}.subpop_data( \
                    id    SERIAL PRIMARY KEY, \
                    run_id INTEGER, \
                    generation INTEGER, \
                    x_coord INTEGER, \
                    y_coord INTEGER, \
                    mean_fitness REAL, \
                    behavior JSONB, \
                    census JSONB \
                );\
                CREATE TABLE IF NOT EXISTS {cfg.schema_name}.pop_data( \
                    id    SERIAL PRIMARY KEY, \
                    run_id INTEGER, \
                    generation INTEGER, \
                    mean_fitness REAL, \
                    behavior JSONB, \
                    census JSONB \
                );\
                CREATE TABLE IF NOT EXISTS {cfg.schema_name}.runs( \
                 id SERIAL PRIMARY KEY, \
                 simulation_id INTEGER, \
                 generations INTEGER, \
                 width INTEGER, \
                 length INTEGER, \
                 subpop_size INTEGER, \
                 relative_fitnesses BOOLEAN, \
                 migration_distance INTEGER, \
                 migration_survival REAL, \
                 initial_sequence VARCHAR(256)\
                )"
        
        cur.execute(query)
        
        print("tables done")
        conn.commit()
        cur.close()
        conn.close()
        print("commited and closed")