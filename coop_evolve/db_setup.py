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
        
        
        cur.execute(f"DROP SCHEMA IF EXISTS {cfg.schema_name} CASCADE")
        
        # cur.execute("CREATE SEQUENCE test.serial START 101")
        # conn.commit()
        
        
        
        query = f"CREATE SCHEMA {cfg.schema_name} \
                    CREATE TABLE experiments( \
                        id SERIAL PRIMARY KEY, \
                        behaviors VARCHAR(16), \
                        gene_delimiter CHAR(1), \
                        wild_cards VARCHAR(4), \
                        chromosome_length INTEGER, \
                        mutation_rate REAL, \
                        crossover_rate REAL, \
                        interaction_length INTEGER \
                    )\
                    CREATE TABLE subpop_data( \
                        id    SERIAL PRIMARY KEY, \
                        runid INTEGER, \
                        x_coord INTEGER, \
                        y_coord INTEGER, \
                        mean_fitness REAL, \
                        behavior JSONB, \
                        census JSONB \
                    )\
                    CREATE TABLE runs( \
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
        conn.commit()
        cur.close()
        conn.close()