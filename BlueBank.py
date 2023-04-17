# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 20:05:02 2023

@author: pijan_000
"""

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Opening json file
json_file=open('loan_data_json.json')
data=json.load(json_file)
#Creating dataframe from dict
loandata=pd.DataFrame(data)

#finding unique values in purpoes column
loandata['purpose'].unique()

#describe data
loandata.describe()

#using exp function in order to achive actual income
# Adding column to dataframe
income = np.exp(loandata['log.annual.inc'])
loandata['AnnualIncome'] = income

#Creating function for fico category flag

def add_ficocat_column(loandata):
    ficocat = []
    for category in loandata['fico']:
        try: 
            if category >= 300 and category < 400:
                cat = 'Very Poor'
            elif category >= 400 and category < 600:
                cat = 'Poor'
            elif category >= 601 and category < 660:
                cat = 'Fair'
            elif category >= 660 and category < 700:
                cat = 'Good'
            elif category >= 700:
                cat = 'Excellent'
            else:
                cat = 'Unknown'
        except:
            cat = 'Error - Unknown'
        ficocat.append(cat)
    loandata['ficocat'] = ficocat
    return loandata

loandata = add_ficocat_column(loandata)

#Creating a new column based of interest rate value

loandata.loc[loandata['int.rate'] > 0.12, 'int.rate.type'] = 'High'
loandata.loc[loandata['int.rate'] <= 0.12, 'int.rate.type'] = 'Low'

#counting fico category and purpouse items and vizualize on a bar plot

catplot = loandata.groupby(['ficocat']).size()
catplot.plot.bar()
plt.show()

purposecount = loandata.groupby(['purpose']).size()
purposecount.plot.bar(color='yellow', width = 0.4)
plt.show()

#Saving csv
loandata.to_csv('loan_cleaned.csv', index=True)




