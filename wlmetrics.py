#! /usr/bin/env python
"""
wlmetrics.py
Activity times lib

Created by Jeremy Smith on 2017-10-12
j.smith.03@cantab.net
"""

import numpy as np
import pandas as pd


# Metric 1: Weighted sum(life) - sum(work) normalized to (0,1)
def w_l_balance_weighted_ratio(df, pos, neg, weights_p, weights_n):
    df_p = df[['t' + a for a in pos]]
    df_n = df[['t' + a for a in neg]]
    wl = df_p.dot(weights_p) - df_n.dot(weights_n)
    wl -= wl.min()
    wl /= wl.max()
    return wl


# Metric 2: More than 10h work in the day
def w_l_balance_workday(df, workid='0501', hours=10):
    wl = df['t' + workid] > hours * 60
    return wl


# Metric 3: % of day spent on Personal Care
def w_l_balance_personalcare(df):
    pc = ['010101', '0102', '0103', '1101']
    pc_c = ['t' + a for a in pc]
    wl = df[pc_c].sum(axis=1) / (24. * 60.)
    return wl


# Metric 4: % of day spent on Leisure and Socializing
def w_l_balance_leisuresocial(df):
    ls = ['1201', '1202', '1203', '1204', '1301', '1302', '14']
    ls_c = ['t' + a for a in ls]
    wl = df[ls_c].sum(axis=1) / (24. * 60.)
    return wl


# Metric 5: More than 8h childcare and/or housework
def w_l_balance_housework(df, hours=5):
    workids = ['0301', '0302', '0303', '0201', '0202', '0209']
    workids_c = ['t' + a for a in workids]
    wl = df[workids_c].sum(axis=1) > hours * 60
    return wl
