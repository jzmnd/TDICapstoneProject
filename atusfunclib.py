#! /usr/bin/env python
"""
atusfunclib.py
Functions for processing ATUS dataset

Created by Jeremy Smith on 2017-09-08
j.smith.03@cantab.net
"""

import os
import pandas as pd


def group_filter_average(df, groupbycol, filtercol, fval, fab='a', weights='TUFNWGTP'):
    # Filtered dataframes and excluding NA values
    if fab == 'a':
        df_filter = df[df[filtercol] >= fval].dropna(subset=[groupbycol])
    elif fab == 'b':
        df_filter = df[df[filtercol] <= fval].dropna(subset=[groupbycol])
    elif fab == 'equal':
        df_filter = df[df[filtercol] == fval].dropna(subset=[groupbycol])
    else:
        df_filter = df.dropna(subset=[groupbycol])

    # Group by
    df_group = df_filter.groupby(groupbycol)

    # Average minutes per day on a particular activity (across all groups)
    df_av = df_filter.filter(like='_W').filter(like='t').sum() / df_filter[weights].sum()

    # Weighted average activity times by group
    df_av_group_times = df_group.sum().filter(like='_W').filter(like='t').divide(df_group[weights].sum(), axis='index')
    # Mean metrics by group
    df_av_group_mets = df_group.mean().filter(like='metric')

    del df_filter

    df_av_group = df_av_group_times.join(df_av_group_mets, how='left')

    del df_av_group_times
    del df_av_group_mets

    return [df_av, df_group, df_av_group]


def load_actcodes(loc='data', loc_codes="code_tables"):
    # Import activity code dictionary csv to df
    dfactcodes = pd.read_csv(os.path.join(loc, loc_codes, "activity_codes.csv"),
                             index_col=False,
                             sep=';',
                             dtype={'CODE': str, 'NAME': str})

    # Import short names and merge
    defactshrt = pd.read_csv(os.path.join(loc, loc_codes, "activity_codes_short.csv"),
                             index_col=False,
                             sep=';',
                             dtype={'CODE': str, 'SHORTNAME': str})
    dfactcodes = dfactcodes.merge(defactshrt, how='outer', on='CODE')

    return dfactcodes


def load_data(loc='data', loc_clean="cleaned_data", loc_codes="code_tables"):
    # Import all data from pickle
    if os.path.isfile(os.path.join(loc, loc_clean, "alldata_0315_df.pkl")):
        df = pd.read_pickle(os.path.join(loc, loc_clean, "alldata_0315_df.pkl"))
    elif os.path.isfile(os.path.join(loc, loc_clean, "alldata_0315.csv")):
        df = pd.read_csv(os.path.join(loc, loc_clean, "alldata_0315.csv"), index_col=0)
    else:
        df = pd.DataFrame()

    # Import activity code dictionary csv to df
    dfactcodes = load_actcodes(loc='data', loc_codes="code_tables")

    # Add codepoint level (1, 2 or 3) and sort
    dfactcodes['LEVEL'] = dfactcodes.CODE.str.len() / 2
    dfactcodes = dfactcodes.sort_values('CODE').reset_index(drop=True)

    # Import education level code dictionary csv to df
    dfeducodes = pd.read_csv(os.path.join(loc, loc_codes, "edu_codes.csv"),
                             index_col=False,
                             sep=';',
                             dtype={'CODE': str, 'NAME': str})

    # Import income level code dictionary csv to df
    dfinccodes = pd.read_csv(os.path.join(loc, loc_codes, "inc_codes.csv"),
                             index_col=False,
                             sep=';',
                             dtype={'CODE': str, 'NAME': str})

    # Import age code dictionary csv to df
    dfagecodes = pd.read_csv(os.path.join(loc, loc_codes, "age_codes.csv"),
                             index_col=False,
                             sep=';',
                             dtype={'CODE': str, 'NAME': str})

    # Import employment status code dictionary csv to df
    dfempcodes = pd.read_csv(os.path.join(loc, loc_codes, "employ_codes.csv"),
                             index_col=False,
                             sep=';',
                             dtype={'CODE': str, 'NAME': str})

    # Import industry and occupation code dictionary csv to df
    dfindcodes = pd.read_csv(os.path.join(loc, loc_codes, "indocc_codes.csv"),
                             index_col=False,
                             sep=';',
                             dtype={'FLAG': str, 'CODE': str, 'NAME': str})

    # Import race code dictionary csv to df
    dfraccodes = pd.read_csv(os.path.join(loc, loc_codes, "race_codes.csv"),
                             index_col=False,
                             sep=';',
                             dtype={'CODE': str, 'NAME': str, 'NAME2012': str})

    # Import location (state) code dictionary csv to df
    dfloccodes = pd.read_csv(os.path.join(loc, loc_codes, "state_codes.csv"),
                             index_col=False,
                             sep=';',
                             dtype={'CODE': str, 'NAME': str,
                                    'LONGNAME': str, 'ABV': str, 'SLUG': str,
                                    'LATITUDE': float, 'LONGITUDE': float,
                                    'POPULATION': float, 'AREA': float})

    # Import "who activity is performed with" code dictionary csv to df
    dfwhocodes = pd.read_csv(os.path.join(loc, loc_codes, "who_codes.csv"),
                             index_col=False,
                             sep=';',
                             dtype={'CODE': str, 'NAME': str})

    # Import input codes
    dfdemocodes = pd.read_csv(os.path.join(loc, loc_codes, "demographic_codes.csv"),
                              index_col=False,
                              sep=';',
                              dtype={'CODE': str, 'NAME': str})

    return [df, dfactcodes, dfeducodes, dfinccodes, dfagecodes,
            dfempcodes, dfindcodes, dfraccodes, dfloccodes, dfwhocodes,
            dfdemocodes]
