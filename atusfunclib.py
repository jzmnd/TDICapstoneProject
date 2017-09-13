#! /usr/bin/env python
"""
atusfunclib.py
Functions for processing ATUS data

Created by Jeremy Smith on 2017-09-08
j.smith.03@cantab.net
"""

import os
import pandas as pd


def group_filter_average(df, groupbycol, filtercol, fval, weights='TUFNWGTP'):
    # Filtered dataframes and excluding NA values
    df_filter = df[df[filtercol] >= fval].dropna(subset=[groupbycol])

    # Group by and fiter by respondents age >= 18
    df_group = df_filter.groupby(groupbycol)

    # Weighted average activity times by group
    df_av_group = df_group.sum().filter(like='_W').filter(like='t').divide(df_group[weights].sum(), axis='index')

    return [df_filter, df_group, df_av_group]


def load_data(loc='data'):
    # Import all data
    df = pd.read_csv(os.path.join(loc, "alldata_0315.csv"), index_col=0)

    # Import activity code dictionary csv to df
    dfactcodes = pd.read_csv(os.path.join(loc, "activity_codes.csv"),
                             index_col=False,
                             sep=';',
                             dtype={'CODE': str, 'NAME': str})

    # Add codepoint level (1, 2 or 3) and sort
    dfactcodes['LEVEL'] = dfactcodes.CODE.str.len() / 2
    dfactcodes = dfactcodes.sort_values('CODE').reset_index(drop=True)

    # Import education level code dictionary csv to df
    dfeducodes = pd.read_csv(os.path.join(loc, "edu_codes.csv"),
                             index_col=False,
                             sep=';',
                             dtype={'CODE': str, 'NAME': str})

    # Import income level code dictionary csv to df
    dfinccodes = pd.read_csv(os.path.join(loc, "inc_codes.csv"),
                             index_col=False,
                             sep=';',
                             dtype={'CODE': str, 'NAME': str})

    # Import age code dictionary csv to df
    dfagecodes = pd.read_csv(os.path.join(loc, "age_codes.csv"),
                             index_col=False,
                             sep=';',
                             dtype={'CODE': str, 'NAME': str})

    # Import employment status code dictionary csv to df
    dfempcodes = pd.read_csv(os.path.join(loc, "employ_codes.csv"),
                             index_col=False,
                             sep=';',
                             dtype={'CODE': str, 'NAME': str})

    # Import industry and occupation code dictionary csv to df
    dfindcodes = pd.read_csv(os.path.join(loc, "indocc_codes.csv"),
                             index_col=False,
                             sep=';',
                             dtype={'FLAG': str, 'CODE': str, 'NAME': str})

    # Import race code dictionary csv to df
    dfraccodes = pd.read_csv(os.path.join(loc, "race_codes.csv"),
                             index_col=False,
                             sep=';',
                             dtype={'CODE': str, 'NAME': str, 'NAME2012': str})

    # Import location (state) code dictionary csv to df
    dfloccodes = pd.read_csv(os.path.join(loc, "state_codes.csv"),
                             index_col=False,
                             sep=';',
                             dtype={'CODE': str, 'NAME': str})

    # Import "who activity is performed with" code dictionary csv to df
    dfwhocodes = pd.read_csv(os.path.join(loc, "who_codes.csv"),
                             index_col=False,
                             sep=';',
                             dtype={'CODE': str, 'NAME': str})

    return [df, dfactcodes, dfeducodes, dfinccodes, dfagecodes,
            dfempcodes, dfindcodes, dfraccodes, dfloccodes, dfwhocodes]
