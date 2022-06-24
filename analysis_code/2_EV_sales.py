#We will calculate sales of EVs per economy per year

#%%
#CONFIG
execfile("../config.py")#usae this to load libraries and set variables. Feel free to edit that file as you need


#%%

#import stocks data to calcualte expected sales per year *we will irgnore the degradation of EVs in the future*
data = pd.read_csv('../input_data/Transport_Energy_Stocks_Macro_wide.csv')#thisis a fiole contaiing the stocks data from 8th edition

#%%
#this section will format the data to be used in the analysis
data_2 = data[data['Measure'] == 'Stocks']
data_2 = data_2[data_2['Drive'] == 'BEV']
data_2 = data_2[data_2['Vehicle Type'] == 'LV']

data_2 = data_2.drop(columns=['Measure', 'Drive', 'Drive_2','Drive_3','Vehicle Type', 'Technology', 'Transport Type'])
data_2 = data_2.drop_duplicates()

#create years col
data_2 = data_2.melt(id_vars=['Economy', 'Region', 'Scenario'], var_name='Year', value_name='Value')
#reove years values not between max and min years
data_2 = data_2.loc[data_2['Year'].astype('int32').isin(range(MIN_YEAR, MAX_YEAR+1))]

data_2 = data_2.sort_values(by=['Year'])

#%%
#OPERATION
#group by categories and calc the diff
data_3 = data_2.copy()
data_3['Sales'] = data_3.groupby(['Economy', 'Region', 'Scenario'])['Value'].diff(periods=1)

#%%
#we may be missing data,especially on the first year, so we will just pad it
data_3['Sales'] = data_3.groupby(['Economy', 'Region', 'Scenario'])['Sales'].fillna(method="bfill")
#%%

data_3['Unit'] = 'Million'
sales = data_3.copy().set_index('Year')

#%% 
# create a stocks df for use in looking at inputs in final output data, so copy above process but also create economy and region groupings
Stocks = data[data['Measure'] == 'Stocks']
Stocks = Stocks[Stocks['Vehicle Type'] == 'LV']
Stocks = Stocks[Stocks['Drive_3'].isin(['BEV', 'ICE'])]

Stocks = Stocks.drop(columns=['Measure', 'Vehicle Type', 'Technology', 'Transport Type','Drive_2', 'Drive'])
# Stocks = Stocks.drop(columns=[str(i) for i in range(2051,2071)])
Stocks = Stocks.drop_duplicates()
Stocks = Stocks.groupby(['Economy', 'Region', 'Scenario', 'Drive_3']).sum().reset_index()

Stocks = Stocks.melt(id_vars=['Economy', 'Region', 'Scenario', 'Drive_3'], var_name='Year', value_name='Value')

#reove years values not between max and min years
Stocks = Stocks.loc[Stocks['Year'].astype('int32').isin(range(MIN_YEAR, MAX_YEAR+1))]

Stocks = Stocks.pivot(index=['Economy', 'Region', 'Scenario', 'Year'], columns='Drive_3', values='Value').reset_index()

#times by Million
Stocks['BEV']  = Stocks['BEV'] * 1e6
Stocks['ICE']  = Stocks['ICE'] * 1e6

#rename columns
Stocks = Stocks.rename(columns={'BEV': 'BEV_stocks', 'ICE': 'ICE_stocks'})

#sum up stocks per economy and scenario
Stocks_economy = Stocks.groupby(['Year', 'Economy', 'Region', 'Scenario']).sum().reset_index()
#sum up stocks per region and scenario
Stocks_region = Stocks.groupby(['Year', 'Region', 'Scenario']).sum().reset_index()
#sum up stocks per scenario
Stocks_scenario = Stocks.groupby(['Year', 'Scenario']).sum().reset_index()

#%%
#save sales
sales.to_csv('../intermediate_data/Stocks_sales_by_economy.csv')

#save stocks
Stocks_scenario.to_csv('../intermediate_data/Stocks_by_scenario.csv', index=False)
Stocks_economy.to_csv('../intermediate_data/Stocks_by_economy.csv', index=False)
Stocks_region.to_csv('../intermediate_data/Stocks_by_region.csv', index=False)

#%%
#############################################################################################################################################################

#%%

#quickly plot all the above
import plotly.express as px
pd.options.plotting.backend = "plotly"#set pandas backend to plotly plotting instead of matplotlib
import plotly.io as pio
pio.renderers.default = "browser"#allow plotting of graphs in the interactive notebook in vscode #or set to notebook

#%%
#melt stocks scenario so we have a drive col
Stocks_plot = Stocks.melt(id_vars=['Year', 'Scenario'], var_name='Drive', value_name='Value')
#plot stocks per scenario
title = 'Stocks of EVs per year'

#plot
fig2 = px.line(Stocks_plot.reset_index(), x="Year", y="Value", color="Drive", line_dash = 'Drive', facet_col='Scenario', title=title)#,

import plotly
plotly.offline.plot(fig2, filename='../plotting_output/' + title + '.html')
fig2.write_image("../plotting_output/static/" + title + '.png')

#%%
#save stocks