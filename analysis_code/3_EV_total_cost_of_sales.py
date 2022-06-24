#We will take sales of EVs per economy per year, and times that by the average cost per batteru which will give us a kind of estimate of the expected capital cost of switching to EVs in that economy.

#%%
#CONFIG
execfile("../config.py")#usae this to load libraries and set variables. Feel free to edit that file as you need


#%%

#import stocks data to calcualte expected sales per year *we will irgnore the degradation of EVs in the future*
sales = pd.read_csv('../intermediate_data/Stocks_sales_by_economy.csv')
Battery_cost_per_EV_USA_China_World_interpolated = pd.read_csv('../intermediate_data/Battery_cost_per_EV_USA_China_World_interpolated.csv')

#%%
#convert sales from millions
sales['Sales'] = sales['Sales'] * 1000000
#remove unit and value col
sales = sales.drop(columns=['Unit', 'Value'])
#%%
#merge data and then cacualate
data = Battery_cost_per_EV_USA_China_World_interpolated.merge(sales, how = 'left', on='Year')

#%%
#melt so we have the battery cost data in one colummn
data = pd.melt(data, id_vars=['Year', 'Economy', 'Region', 'Scenario', 'Sales'] , var_name='Battery_cost_measure', value_name='Battery_cost')

#make year the index
data = data.set_index('Year')
#%%
#calcultate total cost of new vars per year per row
data['Total_cost'] = data['Sales'] * data['Battery_cost']

#%%
#create new columns which splits battery cost measure into Region and max/min using the _
data['Battery_cost_Region'] = data['Battery_cost_measure'].str.split('_').str[0]
data['Battery_cost_Measure'] = data['Battery_cost_measure'].str.split('_').str[1]
#%%
#now start creating subsets of that data from which to analyse
#group by scenarios and calc the sums
Total_cost_by_scenario = data.groupby(['Scenario', 'Battery_cost_Region', 'Battery_cost_Measure','Year', 'Battery_cost']).sum().reset_index()
Total_cost_by_region = data.groupby(['Scenario', 'Region', 'Battery_cost_Region', 'Battery_cost_Measure', 'Year', 'Battery_cost']).sum().reset_index()

Total_cost_by_economy = data.copy().reset_index()

#%%
#save data to csvs 
Total_cost_by_scenario.to_csv('../intermediate_data/Total_cost_of_batteries_in_sales_Total_cost_by_scenario.csv', index=False)
Total_cost_by_region.to_csv('../intermediate_data/Total_cost_of_batteries_in_sales_Total_cost_by_region.csv', index=False)
Total_cost_by_economy.to_csv('../intermediate_data/Total_cost_of_batteries_in_sales_Total_cost_by_economy.csv', index=False)


#%%



