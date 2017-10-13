#! /usr/bin/env python
"""
import_clean_data.py
Script to:
(a) Import data
(b) Select required features
(c) Create categories
(d) Create weighted columns
(e) Export to new csv and pickle

Created by Jeremy Smith on 2017-09-21
j.smith.03@cantab.net
"""

import os
import pandas as pd


# Note: Values of -4, -3, -2, -1 indicate variable, blank, don't know or refused therefore convert to NaN
na_values = [-4, -3, -2, -1]

# Import summary csv to df (basic summary of activity times (each activity has a separate column))
fn = os.path.join("data", "atussum_0315", "atussum_0315.csv")
print "Loading... {}".format(fn)
dfsum = pd.read_csv(fn,
                    index_col=False,
                    na_values=na_values)

# Import respondent csv to df (more info on the respondent of the survey (i.e. TULINENO = 1))
fn = os.path.join("data", "atusresp_0315", "atusresp_0315.csv")
print "Loading... {}".format(fn)
dfresp = pd.read_csv(fn,
                     index_col=False,
                     na_values=na_values)

# Import activity csv to df
fn = os.path.join("data", "atusact_0315", "atusact_0315.csv")
print "Loading... {}".format(fn)
dfact = pd.read_csv(fn,
                    index_col=False,
                    na_values=na_values,
                    dtype={'TRCODEP': str})

# Import who file csv to df (who was involved in activity)
fn = os.path.join("data", "atuswho_0315", "atuswho_0315.csv")
print "Loading... {}".format(fn)
dfwho = pd.read_csv(fn,
                    index_col=False,
                    na_values=na_values)

# Import CPS file csv to df
fn = os.path.join("data", "atuscps_0315", "atuscps_0315.csv")
print "Loading... {}".format(fn)
dfcps = pd.read_csv(fn,
                    index_col=False,
                    na_values=na_values)

# Import activity code dictionary csv to df
fn = os.path.join("data", "code_tables", "activity_codes.csv")
print "Loading... {}".format(fn)
dfactcodes = pd.read_csv(fn,
                         index_col=False,
                         sep=';',
                         dtype={'CODE': str, 'NAME': str})

# Add codepoint level (1, 2 or 3) and sort
dfactcodes['LEVEL'] = dfactcodes.CODE.str.len() / 2
dfactcodes = dfactcodes.sort_values('CODE').reset_index(drop=True)

# Useful columns for actvity df
dfact_use = dfact[['TUCASEID', 'TUACTIVITY_N',              # Case ID, Actvity number
                   'TUACTDUR24', 'TUACTDUR',                # Activity duration (24h cap), Activity duration
                   'TEWHERE', 'TRCODEP',                    # Activity where code, Activity code
                   'TUSTARTTIM', 'TUSTOPTIME']].copy()      # Start time, Stop time


# Useful columns for who file df
dfwho_use = dfwho[['TUCASEID', 'TUACTIVITY_N',              # Case ID, Actvity number
                   'TULINENO', 'TUWHO_CODE']].copy()        # Person line number, Who code


# Useful columns for respondent df
dfresp_use = dfresp[['TUCASEID', 'TRNUMHOU',                # Case ID, Number of people in household
                     'TRMJOCGR', 'TRDTOCC1', 'TRMJIND1',    # Major occupation, Detailed occupation, Major industry
                     'TUFWK', 'TUABSOT', 'TEIO1COW',        # Work code, Job code, Individual class of worker code
                     'TEERNPER',                            # Easiest way for you to report your earnings
                     'TUDIS',                               # Disability status
                     'TRERNHLY', 'TRERNWA']].copy()         # Hourly earnings, Weekly earnings

# Calculate actual weekly and hourly earnaings i.e. divide by 100 to get dollar amount
print "Calculating..."
dfresp_use.TRERNHLY = dfresp_use.TRERNHLY / 100.
dfresp_use.TRERNWA = dfresp_use.TRERNWA / 100.

# Add weekly earning category
bins = [0, 200, 400, 600, 800, 1000, 1500, 2000, 3000]
labels = ["1", "2", "3", "4", "5", "6", "7", "8"]
dfresp_use['TRERNWA_CAT'] = pd.cut(dfresp_use['TRERNWA'], bins, labels=labels, right=True)

# Useful columns for activity summary df
dfsum_use = dfsum[['TUCASEID', 'TEAGE', 'TESEX',            # Case ID, Respondent age, Respondent sex
                   'TUYEAR', 'TRHOLIDAY', 'TUDIARYDAY',     # Year of study, Holiday boolean, Day of week
                   'GEMETSTA', 'GTMETSTA',                  # Metropolitan status (old), (new)
                   'TEHRUSLT', 'TELFS',                     # Hours worked per week, Labor force status
                   'TRDPFTPT',                              # FT or PT employment code
                   'TRSPPRES', 'TESPEMPNOT',                # Presence of S/P, employment status of S/P
                   'TESCHENR', 'TESCHLVL',                  # Enrolled in school, School level
                   'PEEDUCA', 'PTDTRACE',                   # Highest education level, Race code
                   'TRCHILDNUM',                            # Number of household children < 18
                   'TUFNWGTP']].copy()                      # Final ATUS weight

# Fix GEMETSTA with new values
dfsum_use.GEMETSTA = dfsum_use.GEMETSTA.fillna(dfsum_use.GTMETSTA)

# Add a weekend indicator
dfsum_use['TRWEEKEND'] = pd.Series((dfsum_use.TUDIARYDAY == 1) | (dfsum_use.TUDIARYDAY == 7), dtype=int)

# Add age category
bins = [0, 17, 25, 30, 35, 40, 45, 50, 60, 70, 100]
labels = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
dfsum_use['TEAGE_CAT'] = pd.cut(dfsum_use['TEAGE'], bins, labels=labels, right=True)

# Useful columns for CPS df
dfcps_use = dfcps[dfcps.TULINENO == 1][['TUCASEID', 'GESTFIPS']].copy()     # Case ID, State code

# Activity totals columns for activity summary df
dfsum_acttotals = dfsum.filter(regex='TUCASEID|t')

# Add activity columns for supergroups (level 1 and 2)
df_actgrouped = pd.DataFrame()

for c in dfactcodes[dfactcodes.LEVEL == 2].CODE.values:
    df_actgrouped['t' + c] = dfsum_acttotals.filter(like='t' + c).sum(axis='columns')
for c in dfactcodes[dfactcodes.LEVEL == 1].CODE.values:
    df_actgrouped['t' + c] = dfsum_acttotals.filter(like='t' + c).sum(axis='columns')

# Merge Activity Summary and Respondent df with Activity totals merged at end
dfmerged = dfsum_use.merge(dfresp_use,
                           on='TUCASEID',
                           how='left',
                           copy=False) \
                    .merge(dfcps_use,
                           on='TUCASEID',
                           how='left',
                           copy=False) \
                    .merge(dfsum_acttotals,
                           on='TUCASEID',
                           how='left',
                           copy=False) \
                    .join(df_actgrouped,
                          how='left')

# Multiply activity times and other variables by weights (TUFNWGTP) to allow for sampling biases (append _W)
dfsum_acttotals_W = dfsum_acttotals.iloc[:, 1:].multiply(dfsum_use.TUFNWGTP, axis='index')

dfsum_use_W = dfsum_use[['TEHRUSLT', 'TEAGE', 'TRCHILDNUM']].multiply(dfsum_use.TUFNWGTP, axis='index')

dfresp_use_W = dfresp_use[['TRNUMHOU', 'TRERNHLY', 'TRERNWA']].multiply(dfsum_use.TUFNWGTP, axis='index')

df_actgrouped_W = df_actgrouped.multiply(dfsum_use.TUFNWGTP, axis='index')

# Join all data frames together
dfmerged_W = dfmerged.join(dfsum_use_W,
                           how='left',
                           rsuffix='_W') \
                     .join(dfresp_use_W,
                           how='left',
                           rsuffix='_W') \
                     .join(dfsum_acttotals_W,
                           how='left',
                           rsuffix='_W') \
                     .join(df_actgrouped_W,
                           how='left',
                           rsuffix='_W')

# Export final dataframe as .csv
fn = os.path.join("data", "cleaned_data", "alldata_0315.csv")
print "Writing... {}".format(fn)
dfmerged_W.to_csv(fn)

# Pickle dataframe
fn = os.path.join("data", "cleaned_data", "alldata_0315_df.pkl")
print "Pickling... {}".format(fn)
dfmerged_W.to_pickle(fn)
