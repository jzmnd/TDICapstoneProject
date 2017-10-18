#! /usr/bin/env python
"""
create_db.py
Creates a postgresql database

Created by Jeremy Smith on 2017-09-21
j.smith.03@cantab.net
"""

import os
from atusfunclib import load_data
from sqlalchemy import create_engine
import yaml

# Load config file
with open('config', 'r') as f:
    print "Loading config..."
    config = yaml.load(f)
    SQL_PASSWORD = config['sql']['pass']
    SQL_USERNAME = config['sql']['user']
    PATH = config['data']['path']

# Import all data
print "Loading all data..."
data_import = load_data(loc="data", loc_clean="cleaned_data", loc_codes="code_tables")

# Unpack individual dataframes
df, dfactcodes, dfeducodes, dfinccodes, dfagecodes, \
    dfempcodes, dfindcodes, dfraccodes, dfloccodes, dfwhocodes, \
    dfdemocodes = data_import

# Dtype conversion dictionary
dtypedict = {'int64': 'BIGINT', 'float64': 'REAL', 'category': 'TEXT'}

# Code tables
codedfs = {'actcodes': dfactcodes, 'educodes': dfeducodes, 'inccodes': dfinccodes,
           'agecodes': dfagecodes, 'empcodes': dfempcodes, 'indcodes': dfindcodes,
           'raccodes': dfraccodes, 'loccodes': dfloccodes, 'whocodes': dfwhocodes,
           'democodes': dfdemocodes}

# Data tables
datadfs = {'actimesw3': df.filter(regex=r'TUCASEID|t\d{6}_W'),
           'actimes3':  df.filter(regex=r'TUCASEID|t\d{6}$'),
           'actimesw2': df.filter(regex=r'TUCASEID|t\d{4}_W'),
           'actimes2':  df.filter(regex=r'TUCASEID|t\d{4}$'),
           'actimesw1': df.filter(regex=r'TUCASEID|t\d{2}_W'),
           'actimes1':  df.filter(regex=r'TUCASEID|t\d{2}$'),
           'demow':     df.filter(regex=r'TUCASEID|^[A-Z]+_W'),
           'demo':      df.filter(regex=r'TUCASEID|^[A-Z]+[^_W]$')}

# Database name
databasename = 'atusdata'
# Username
username = SQL_USERNAME
# Password
password = SQL_PASSWORD
# Port
port = 5432

# Postgres engine for atusdata database
engine = create_engine("postgresql://{}:{}@localhost:{}/{}".format(username,
                                                                   password,
                                                                   port,
                                                                   databasename))

# Create code tables (small tables - OK to use pandas)
print "Creating code tables..."
for k in codedfs.keys():
    try:
        codedfs[k].to_sql(k, engine)
    except ValueError:
        print "Table '{}' already exists in '{}'".format(k, databasename)

# Create csv subfiles from data dfs
print "Creating clean csv subfiles..."
for k in datadfs.keys():
    filenamestring = os.path.join(PATH, "cleaned_data", "{}.csv".format(k))
    datadfs[k].to_csv(filenamestring)

# SQL statements for table create, copy and drop table
sql_create_statement = """
    CREATE TABLE IF NOT EXISTS {}
        ({});
    """
sql_copy_statement = """
    COPY {} FROM '{}'
        WITH (FORMAT csv, HEADER);
    """
sql_droptable_statement = """
    DROP TABLE {};
"""

# Delete tables
print "Drop tables if already present..."
for k in datadfs.keys():
    try:
        engine.execute(sql_droptable_statement.format(k))
        print "  Table '{}' dropped".format(k)
    except:
        print "  Table '{}' OK to create".format(k)

# Create tables
print "Creating tables..."
for k in datadfs.keys():
    header = datadfs[k].keys().tolist()
    dtypes = [dtypedict[i.name] for i in datadfs[k].dtypes.tolist()]

    schemestring = "index BIGINT, " + ", ".join([" ".join(i) for i in zip(header, dtypes)])

    engine.execute(sql_create_statement.format(k, schemestring))

# Copy data from csv files into tables
print "Copying data from csv to tables..."
for k in datadfs.keys():
    filenamestring = os.path.join(PATH, "cleaned_data", "{}.csv".format(k))
    print filenamestring

    with engine.connect().execution_options(autocommit=True) as con:
        con.execute(sql_copy_statement.format(k, filenamestring))
