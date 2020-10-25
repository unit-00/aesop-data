#!/bin/bash
python pipeline/run_pipeline.py --db_config '{
        "host": "localhost", 
        "port": 27017, 
        "database": "story", 
        "collection": "aesop"
    }'