#!/usr/bin/env python
# coding: utf-8

# # Analysis of IIJA Funding Allocation: Equitability and Political Bias
# 
# ## Introduction:
# This report analyzes the allocation of Infrastructure Investment and Jobs Act (IIJA) funding by State and Territory, examining the relationship between funding per capita, population, and political preferences. Three primary datasets were merged: IIJA funding data, population estimates, and the 2020 election results.
# 
# 

# ## Data Sources:
# 
# #### IIJA Funding Data:
# Source: Infrastructure Investment and Jobs Act funding by State and Territory.
# Attachment in Blackboard.
# 
# #### Population Data:
# Source: Annual Estimates of the Resident Population (NST-EST2023-POP) from April 1, 2020, to July 1, 2023.
# https://www.census.gov/data/tables/time-series/demo/popest/2020s-state-total.html
# 
# #### Election Results:
# Source: 2020 election results.
# https://www.archives.gov/electoral-college/2020
# 

# ## Data Merging:
# Merge IIJA funding, population, and election results datasets.
# 
# ## Calculation:
# Calculate funding per capita by dividing IIJA funding by population.
# 
# ## Political Preferences:
# Determine the political preference (Biden or Trump) for each state based on the 2020 election results.
# 

# In[77]:


#Import 

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch


# IIJAf = Infrastructure Investment and Jobs Act funding 
IIJAf_file_url = "https://github.com/Benson90/Data-608/raw/3b2fad74a5bf78aeb939e4b2a533f2911b737618/IIJA%20FUNDING%20AS%20OF%20MARCH%202023(1).xlsx"
Population_file_url = "https://github.com/Benson90/Data-608/raw/a7c79d29e6c8119b792cee93cfb7d596cd34bac1/NST-EST2023-POP.xlsx"
Election2020_file_url = "https://github.com/Benson90/Data-608/raw/a8f99f9314d498eb12e09c97844ea88d8208e663/2020%20elec.xlsx"


# Pandas DataFrame
IIJAf_df = pd.read_excel(IIJAf_file_url)
Population_df = pd.read_excel(Population_file_url)
Election_df = pd.read_excel(Election2020_file_url)

# Data Cleaning
IIJAf_df['state_lower'] = IIJAf_df['State, Teritory or Tribal Nation'].str.lower()
Population_df['state_lower'] = Population_df['States'].str.lower()
Election_df['state_lower'] = Election_df['State'].str.lower()
Population_df['Pop'] = Population_df['Pop'].astype(float)
Election_df = Election_df.fillna(0)
Election_df['favorite_candidate'] = Election_df.apply(lambda row: 'Biden' if row['Joseph R. Biden Jr.,'] > row['Donald J. Trump,'] else 'Trump', axis=1)


# Merge DataSet
Merged_df = pd.merge(IIJAf_df, Population_df, left_on='state_lower', right_on='state_lower')
Merged_df = pd.merge(Merged_df, Election_df, left_on='state_lower', right_on='state_lower')

print(Merged_df.dtypes)


# ## Analysis:
# The analysis reveals that the top 4 states with the highest funding per capita all align with Trump's political preferences, as per the 2020 election results.

# In[78]:


# Calculate funding per capita
Merged_df['funding_per_capita'] = (Merged_df['Total (Billions)']*1000000)/ Merged_df['Pop']

# Plotting
Merged_df = Merged_df.sort_values(by='funding_per_capita', ascending=False)

plt.figure(figsize=(12, 6))

# Bar chart for funding per capita


plt.subplot(1, 1, 1)
for index, row in Merged_df.iterrows():
    color = 'blue' if row['favorite_candidate'] == 'Biden' else 'red'
    plt.bar(row['state_lower'], row['funding_per_capita'], color=color)
plt.title('IIJA Funding per Capita by State')
plt.xlabel('State')
plt.ylabel('Funding per Capita')
plt.xticks(rotation=45, ha='right')
legend_labels = ['Blue (Biden)', 'Red (Trump)']
legend_handles = [Patch(color='blue', label='Blue (Biden)'), Patch(color='red', label='Red (Trump)')]
plt.legend(handles=legend_handles, labels=legend_labels)


plt.tight_layout()
plt.show()


# ## Conclusions:
# 
# #### Equitability:
# The distribution of IIJA funding per capita does not appear equitable, as the top-performing states are consistent with specific political preferences.
# 
# #### Political Bias:
# The allocation of funds demonstrates a potential bias favoring the political interests of the Trump administration.
