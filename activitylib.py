#! /usr/bin/env python
"""
activitylib.py
Activity times lib

Created by Jeremy Smith on 2017-10-11
j.smith.03@cantab.net
"""

from atusfunclib import load_actcodes

# Load activity codes
dfactcodes = load_actcodes()

# Activities that we are interested in
positiveWL = ['010101', '0102', '0103', '050201',
              '050203', '1101', '1201', '1202',
              '1203', '1204', '1301', '1302', '14']

negoccWL = ['05', '0501', '0504', '1805']

neghomeWL = ['0201', '0202', '0203', '0204', '0209',
             '0301', '0302', '0303', '0304', '0305',
             '0802', '0803']

neutral = ['06', '07', '09', '18']

activities = positiveWL + negoccWL + neghomeWL + neutral

activities_t = ['t'+ a for a in activities]

# Activity names dictionaries
activities_n_dict = dict(zip(dfactcodes.CODE, dfactcodes.NAME))
activities_n_dict_inter = dict([d for d in zip(dfactcodes.CODE, dfactcodes.NAME) if d[0] in activities])

# Activity codes dictionary
activities_c_dict = dict(zip(dfactcodes.NAME, dfactcodes.CODE))
activities_c_dict_inter = dict([d for d in zip(dfactcodes.NAME, dfactcodes.CODE) if d[1] in activities])

# Infodict for all values
ACTINFO = {'positiveWL': positiveWL,
           'negoccWL': negoccWL,
           'neghomeWL': neghomeWL,
           'neutral': neutral,
           'activities': activities,
           'activities_t': activities_t,
           'activities_n_dict': activities_n_dict,
           'activities_n_dict_inter': activities_n_dict_inter,
           'activities_c_dict': activities_c_dict,
           'activities_c_dict_inter': activities_c_dict_inter}
