#plpto all; data related to calcualting total capciatal cost of ev batteries in future based on sales data
#load data
#%%
execfile("../config.py")#usae this to load libraries and set variables. Feel free to edit that file as you need

#%%
sales = pd.read_csv('../intermediate_data/Stocks_sales_by_economy.csv')
Battery_cost_per_EV_USA_China_World_interpolated = pd.read_csv('../intermediate_data/Battery_cost_per_EV_USA_China_World_interpolated.csv')
Stocks_scenario = pd.read_csv('../intermediate_data/Stocks_by_scenario.csv')

Total_cost_by_scenario = pd.read_csv('../intermediate_data/Total_cost_of_batteries_in_sales_Total_cost_by_scenario.csv')
Total_cost_by_region = pd.read_csv('../intermediate_data/Total_cost_of_batteries_in_sales_Total_cost_by_region.csv')
Total_cost_by_economy = pd.read_csv('../intermediate_data/Total_cost_of_batteries_in_sales_Total_cost_by_economy.csv')

#%%

# plot all the above
import plotly.express as px
pd.options.plotting.backend = "plotly"#set pandas backend to plotly plotting instead of matplotlib
import plotly.io as pio
pio.renderers.default = "browser"#allow plotting of graphs in the interactive notebook in vscode #or set to notebook

#%%
#to simplify things we will print the data for, Battery_cost_Region   = world, for the region from which average battery size per car is based on, since that is a mix of china and USA vehiel sales

#filter regon = world
Total_cost_by_scenario_world = Total_cost_by_scenario.loc[(Total_cost_by_scenario['Battery_cost_Region'] == 'World')]
Total_cost_by_region_world = Total_cost_by_region.loc[(Total_cost_by_region['Battery_cost_Region'] == 'World')]
Total_cost_by_economy_world = Total_cost_by_economy.loc[(Total_cost_by_economy['Battery_cost_Region'] == 'World')]

#We will also take the .mean() between max and min in Battery_cost_Measure
#first remove Battery_cost_Measure from the data
Total_cost_by_scenario_world = Total_cost_by_scenario_world.drop(columns=['Battery_cost_Measure'])
Total_cost_by_region_world = Total_cost_by_region_world.drop(columns=['Battery_cost_Measure'])
Total_cost_by_economy_world = Total_cost_by_economy_world.drop(columns=['Battery_cost_Measure'])

#now calc mean since all values are either duplicated or in max and min form, so we will either get the same value or avg of max and min
Total_cost_by_scenario_world = Total_cost_by_scenario_world.groupby(['Scenario', 'Year']).mean()
Total_cost_by_region_world = Total_cost_by_region_world.groupby(['Scenario', 'Region', 'Year']).mean()
Total_cost_by_economy_world = Total_cost_by_economy_world.groupby(['Scenario', 'Region', 'Economy', 'Year']).mean()


#%%

title = 'Total cost of batteries sales per year (USD)'

#plot
fig2 = px.line(Total_cost_by_scenario_world.reset_index(), x="Year", y="Total_cost", color="Scenario", line_dash = 'Scenario', title=title)#,

import plotly
plotly.offline.plot(fig2, filename='../plotting_output/' + title + '.html')
fig2.write_image("../plotting_output/static/" + title + '.png')

#%%

title = 'Total cost of batteries sales per year by region (USD)'

#plot
fig2 = px.line(Total_cost_by_region_world.reset_index(), x="Year", y="Total_cost", color="Scenario", facet_col='Region', line_dash = 'Scenario', title=title)#,

import plotly
plotly.offline.plot(fig2, filename='../plotting_output/' + title + '.html')
fig2.write_image("../plotting_output/static/" + title + '.png')
# %%


title = 'Total cost of batteries sales per year by economy (USD)'

Total_cost_by_economy_world = Total_cost_by_economy_world.reset_index().sort_values(by=['Region', 'Year'])
#plot
fig2 = px.line(Total_cost_by_economy_world, x="Year", y="Total_cost", color="Scenario", facet_col = 'Economy',  facet_col_wrap=7, line_dash = 'Scenario', title=title)#,

import plotly
plotly.offline.plot(fig2, filename='../plotting_output/' + title + '.html')
fig2.write_image("../plotting_output/static/" + title + '.png')

#%%

#plotting input data

#Iea price of batteries interpolated plot
title = 'Avg cost of EV batteries per year (USD)'

#plot
fig2 = px.line(Total_cost_by_scenario_world.reset_index(), x="Year", y="Battery_cost", color="Scenario", line_dash = 'Scenario', title=title)#,

import plotly
plotly.offline.plot(fig2, filename='../plotting_output/' + title + '.html')
fig2.write_image("../plotting_output/static/" + title + '.png')

#%%
#sales of evs plot

title = 'Sales of EVs per year'

#plot
fig2 = px.line(Total_cost_by_scenario_world.reset_index(), x="Year", y="Sales", color="Scenario", line_dash = 'Scenario', title=title)#,

import plotly
plotly.offline.plot(fig2, filename='../plotting_output/' + title + '.html')
fig2.write_image("../plotting_output/static/" + title + '.png')

#%%

####################################################################################################################################################
#%%
#now create a simple dataframe for people to easily double check their initiative about the data and whatnot
#merge stocks data to Total_cost_by_scenario_world
all_data_detail = pd.merge(Total_cost_by_scenario_world, Stocks_scenario, how='left', on=['Scenario', 'Year'])

#divide all values by 1million and round to 2 dp
all_data_detail['Total cost in that year (Millions USD)'] =  round(all_data_detail['Total_cost']/1000000, 0)
all_data_detail['Cost per average EV battery (USD)'] = round(all_data_detail['Battery_cost'], 0)
all_data_detail['Sales in that year (Millions)'] = round(all_data_detail['Sales']/1000000, 2)
all_data_detail['BEV_stocks (Millions)'] = round(all_data_detail['BEV_stocks']/1000000, 0)
all_data_detail['ICE_stocks (Millions)'] = round(all_data_detail['ICE_stocks']/1000000, 0)

#save to csv 
all_data_detail.to_csv('../intermediate_data/Stocks_sales_and_cost_data.csv')

#%%
#create a table for viewieng

#filter for years 2020, 2030,3040,4050
all_data_detail = all_data_detail.loc[all_data_detail['Year'].isin([2020, 2030, 2040, 2050])]

#https://plotly.com/python/table/
import plotly.graph_objects as go

title = 'Stocks_sales_and_cost_data_table_millions'

fig = go.Figure(data=[go.Table(
    header=dict(values=[all_data_detail['Scenario'].name, all_data_detail['Year'].name, all_data_detail['BEV_stocks (Millions)'].name, all_data_detail['ICE_stocks (Millions)'].name, all_data_detail['Sales in that year (Millions)'].name,  all_data_detail['Cost per average EV battery (USD)'].name,all_data_detail['Total cost in that year (Millions USD)'].name],
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[all_data_detail['Scenario'], all_data_detail['Year'], all_data_detail['BEV_stocks (Millions)'], all_data_detail['ICE_stocks (Millions)'], all_data_detail['Sales in that year (Millions)'],  all_data_detail['Cost per average EV battery (USD)'],all_data_detail['Total cost in that year (Millions USD)']],
               fill_color='lavender',
               align='left'))
])

import plotly
plotly.offline.plot(fig, filename='../plotting_output/' + title + '.html')
fig.write_image("../plotting_output/static/" + title + '.png')

#%%
