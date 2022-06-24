#%%
execfile("../config.py")#usae this to load libraries and set variables. Feel free to edit that file as you need

#%%
# sales = pd.read_csv('../intermediate_data/Stocks_sales_by_economy.csv')
# Battery_cost_per_EV_USA_China_World_interpolated = pd.read_csv('../intermediate_data/Battery_cost_per_EV_USA_China_World_interpolated.csv')
# Stocks_scenario = pd.read_csv('../intermediate_data/Stocks_by_scenario.csv')

Total_cost_by_scenario = pd.read_csv('../intermediate_data/Total_cost_of_batteries_in_sales_Total_cost_by_scenario.csv')
Total_cost_by_region = pd.read_csv('../intermediate_data/Total_cost_of_batteries_in_sales_Total_cost_by_region.csv')
Total_cost_by_economy = pd.read_csv('../intermediate_data/Total_cost_of_batteries_in_sales_Total_cost_by_economy.csv')

Stocks_scenario = pd.read_csv('../intermediate_data/Stocks_by_scenario.csv')
Stocks_economy = pd.read_csv('../intermediate_data/Stocks_by_economy.csv')
Stocks_region = pd.read_csv('../intermediate_data/Stocks_by_region.csv')

#%%
#merge the stocks data into the total cost dfs to create full df
Total_cost_by_scenario = Total_cost_by_scenario.merge(Stocks_scenario, how = 'left', on=['Scenario', 'Year'])
Total_cost_by_region = Total_cost_by_region.merge(Stocks_region, how = 'left', on=['Region', 'Scenario', 'Year'])
Total_cost_by_economy = Total_cost_by_economy.merge(Stocks_economy, how = 'left', on=['Region', 'Economy', 'Scenario', 'Year'])

#%%
#create simplified dataset by using world battery cosots and averageing max and min

#filter regon = world
Total_cost_by_scenario_world = Total_cost_by_scenario.loc[(Total_cost_by_scenario['Battery_cost_Region'] == 'World')]
Total_cost_by_region_world = Total_cost_by_region.loc[(Total_cost_by_region['Battery_cost_Region'] == 'World')]
Total_cost_by_economy_world = Total_cost_by_economy.loc[(Total_cost_by_economy['Battery_cost_Region'] == 'World')]

#We will also take the .mean() between max and min in Battery_cost_Measure
#first remove Battery_cost_Measure from the data
Total_cost_by_scenario_world = Total_cost_by_scenario_world.drop(columns=['Battery_cost_Measure', 'Battery_cost_Region'])
Total_cost_by_region_world = Total_cost_by_region_world.drop(columns=['Battery_cost_Measure', 'Battery_cost_Region'])
Total_cost_by_economy_world = Total_cost_by_economy_world.drop(columns=['Battery_cost_Measure', 'Battery_cost_Region'])

#%%
#now calc mean since all values are either duplicated or in max and min form, so we will either get the same value or avg of max and min
Total_cost_by_scenario_world = Total_cost_by_scenario_world.groupby(['Scenario', 'Year']).mean()
Total_cost_by_region_world = Total_cost_by_region_world.groupby(['Scenario', 'Region', 'Year']).mean()
Total_cost_by_economy_world = Total_cost_by_economy_world.groupby(['Scenario', 'Region', 'Economy', 'Year']).mean()

#%%
#save data to output xlsx
# create a excel writer object
with pd.ExcelWriter("../output/Total_cost_of_batteries_in_sales_detailed.xlsx") as writer:
  
    #now save
    Total_cost_by_scenario.to_excel(writer, sheet_name='Total_cost_by_scenario',merge_cells=False)
    Total_cost_by_region.to_excel(writer, sheet_name='Total_cost_by_region',merge_cells=False)
    Total_cost_by_economy.to_excel(writer, sheet_name='Total_cost_by_economy',merge_cells=False)

with pd.ExcelWriter("../output/Total_cost_of_batteries_in_sales_simple.xlsx") as writer:

    #now save
    Total_cost_by_scenario_world.to_excel(writer, sheet_name='Total_cost_by_scenario',merge_cells=False)
    Total_cost_by_region_world.to_excel(writer, sheet_name='Total_cost_by_region',merge_cells=False)
    Total_cost_by_economy_world.to_excel(writer, sheet_name='Total_cost_by_economy',merge_cells=False)

#%%