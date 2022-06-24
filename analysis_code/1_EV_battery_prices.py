#this is different fromall otehr files as it is not just about graphing the data from hughs modelling. It will calculate average battery size, times the average cost of batteries in those years. 

#In the next file we will calculate sales of EVs per economy per year, and times that by the average cost per batteru which will give us a kind of estimate of the expected capital cost of switching to EVs in that economy.

#NOTE THAT THIS FILE WILL CURRENTLY REMOVE PHEVS FROM THE DATA BUT EVENTUALLY IT WOULD BE GOOD TO INCLDUDE THEM.
#%%
#CONFIG
execfile("../config.py")#usae this to load libraries and set variables. Feel free to edit that file as you need


#%%
#take in stock data

#take in Sales shares 
Sales_share_by_model = pd.read_excel('../input_data/2022_EV_sales_details_and_battery_cost.xlsx', sheet_name='Sales_share_by_model', header=0, index_col=0)
#and model specs data  to go with sales shares
Model_specs = pd.read_excel('../input_data/2022_EV_sales_details_and_battery_cost.xlsx', sheet_name='Model_specs', header=0, index_col=0)
#take in battery cost data
Battery_cost = pd.read_excel('../input_data/2022_EV_sales_details_and_battery_cost.xlsx', sheet_name='Battery_cost', header=0, index_col=0)

#%%
# Remove PHEVs from the data
#we have to join model specs to sales shares to do this
Sales_share_by_model = Sales_share_by_model.join(Model_specs, how='inner')
Sales_share_by_model = Sales_share_by_model[Sales_share_by_model['Drive'] != 'PHEV']

#%%
# FORMAT
#calcualte sales shars from data:

#select Share Worldwide and Name columns
Sales_share_by_model_world = Sales_share_by_model.filter(['Name', 'Share Worldwide'])
#remove na
Sales_share_by_model_world = Sales_share_by_model_world.dropna()
#sum columns   
sum_ = Sales_share_by_model_world.sum(axis=0)
#divide by sum
Sales_share_by_model_world = Sales_share_by_model_world.divide(sum_, axis=1)

#select Share China and Name columns
Sales_share_by_model_china = Sales_share_by_model.filter(['Name', 'Share China'])
#remove na
Sales_share_by_model_china = Sales_share_by_model_china.dropna()
#sum columns   
sum_ = Sales_share_by_model_china.sum(axis=0)
#divide by sum
Sales_share_by_model_china = Sales_share_by_model_china.divide(sum_, axis=1)

#select Share USA and Name columns
Sales_share_by_model_usa = Sales_share_by_model.filter(['Name', 'Share USA'])
#remove na
Sales_share_by_model_usa = Sales_share_by_model_usa.dropna()
#sum columns
sum_ = Sales_share_by_model_usa.sum(axis=0)
#divide by sum
Sales_share_by_model_usa = Sales_share_by_model_usa.divide(sum_, axis=1)

#%%
#merge these to the model specs data
Sales_share_and_specs = Model_specs.merge(Sales_share_by_model_usa, how = 'left', left_index=True, right_index=True)
Sales_share_and_specs = Sales_share_and_specs.merge(Sales_share_by_model_china,how = 'left',  left_index=True, right_index=True)
Sales_share_and_specs = Sales_share_and_specs.merge(Sales_share_by_model_world,how = 'left',  left_index=True, right_index=True)

#%%
#now we have the share of sales by model in china usa and the world. We now times these by their respectuve battery kwh's and sum to get the average battery size for all economys in APERC 
Sales_share_and_specs['USA_KWH_share'] = Sales_share_and_specs['Share USA'] * Sales_share_and_specs['KWH']
Sales_share_and_specs['China_KWH_share'] = Sales_share_and_specs['Share China'] * Sales_share_and_specs['KWH']
Sales_share_and_specs['World_KWH_share'] = Sales_share_and_specs['Share Worldwide'] * Sales_share_and_specs['KWH']


#sum the columns
Sales_share_and_specs['USA_KWH_share_sum'] = Sales_share_and_specs['USA_KWH_share'].sum()
Sales_share_and_specs['China_KWH_share_sum'] = Sales_share_and_specs['China_KWH_share'].sum()
Sales_share_and_specs['World_KWH_share_sum'] = Sales_share_and_specs['World_KWH_share'].sum()

#%%
#add sums to battery cost data, repeated for each row in battery cost data
Battery_cost_and_sales_shares_USA = Battery_cost.assign(USA_KWH_share_sum = Sales_share_and_specs['USA_KWH_share_sum'][0])
Battery_cost_and_sales_shares_China = Battery_cost.assign(China_KWH_share_sum = Sales_share_and_specs['China_KWH_share_sum'][0])
Battery_cost_and_sales_shares_World = Battery_cost.assign(World_KWH_share_sum = Sales_share_and_specs['World_KWH_share_sum'][0])

#%%
#calculate battery cost per measure for each year segment
Battery_cost_and_sales_shares_USA[2020] = Battery_cost_and_sales_shares_USA['USA_KWH_share_sum'] * Battery_cost_and_sales_shares_USA[2020]
Battery_cost_and_sales_shares_USA[2030] = Battery_cost_and_sales_shares_USA['USA_KWH_share_sum'] * Battery_cost_and_sales_shares_USA[2030]
Battery_cost_and_sales_shares_USA[2050] = Battery_cost_and_sales_shares_USA['USA_KWH_share_sum'] * Battery_cost_and_sales_shares_USA[2050]
Battery_cost_and_sales_shares_USA['Measure'] = 'Average cost of battery'
Battery_cost_and_sales_shares_USA['Region'] = 'USA'

Battery_cost_and_sales_shares_China[2020] = Battery_cost_and_sales_shares_China['China_KWH_share_sum'] * Battery_cost_and_sales_shares_China[2020]
Battery_cost_and_sales_shares_China[2030] = Battery_cost_and_sales_shares_China['China_KWH_share_sum'] * Battery_cost_and_sales_shares_China[2030]
Battery_cost_and_sales_shares_China[2050] = Battery_cost_and_sales_shares_China['China_KWH_share_sum'] * Battery_cost_and_sales_shares_China[2050]
Battery_cost_and_sales_shares_China['Measure'] = 'Average cost of battery'
Battery_cost_and_sales_shares_China['Region'] = 'China'

Battery_cost_and_sales_shares_World[2020] = Battery_cost_and_sales_shares_World['World_KWH_share_sum'] * Battery_cost_and_sales_shares_World[2020]
Battery_cost_and_sales_shares_World[2030] = Battery_cost_and_sales_shares_World['World_KWH_share_sum'] * Battery_cost_and_sales_shares_World[2030]
Battery_cost_and_sales_shares_World[2050] = Battery_cost_and_sales_shares_World['World_KWH_share_sum'] * Battery_cost_and_sales_shares_World[2050]
Battery_cost_and_sales_shares_World['Measure'] = 'Average cost of battery'
Battery_cost_and_sales_shares_World['Region'] = 'World'

#stack above data together
Battery_cost_and_sales_shares_USA_China_World = pd.concat([Battery_cost_and_sales_shares_USA, Battery_cost_and_sales_shares_China, Battery_cost_and_sales_shares_World])

#%%
#Now we want to get the dataframe in a state ready to interpolate between the years  availble for the years used in model
#make one column frm 'Region','Type'
Battery_cost_and_sales_shares_USA_China_World['Region_Type'] = Battery_cost_and_sales_shares_USA_China_World['Region'] + '_' + Battery_cost_and_sales_shares_USA_China_World['Type']

#filter for useful cols
Battery_cost_and_sales_shares_USA_China_World = Battery_cost_and_sales_shares_USA_China_World[['Region_Type', 2020, 2030, 2050]].reset_index(drop=True)

#melt df so it has years cols as a single column
Battery_cost_and_sales_shares_USA_China_World = pd.melt(Battery_cost_and_sales_shares_USA_China_World, id_vars=['Region_Type'], value_name='Value', var_name='Year').set_index('Year')

#pivot (make wide) so that we have Region_Type as a set of cols
Battery_cost_and_sales_shares_USA_China_World = pd.pivot(Battery_cost_and_sales_shares_USA_China_World,  columns='Region_Type', values='Value')


#%%
#now we will interpolate the data to create a dataframe with the average cost of EV battery for each year of the outlook data

#create a list of years to create a row for each year
Years = range(MIN_YEAR,MAX_YEAR+1)

#craete empty dataframe with years as rows
Battery_cost_per_EV_USA_China_World_interpolated = pd.DataFrame(index=Years)

#merge data from Battery_cost_and_sales_shares_USA_China_World into Battery_cost_per_EV_USA_China_World_interpolated on the year column
Battery_cost_per_EV_USA_China_World_interpolated = Battery_cost_per_EV_USA_China_World_interpolated.merge(Battery_cost_and_sales_shares_USA_China_World, how='left', left_index=True, right_index=True).reset_index()

#reset the index column so we can create dateteime column from the year col
Battery_cost_per_EV_USA_China_World_interpolated.rename(columns = {'index':'Year'}, inplace = True)

#create year col
Battery_cost_per_EV_USA_China_World_interpolated['Year'] = pd.to_datetime(Battery_cost_per_EV_USA_China_World_interpolated['Year'], format='%Y')

#make year col the index again 
Battery_cost_per_EV_USA_China_World_interpolated = Battery_cost_per_EV_USA_China_World_interpolated.set_index('Year')

#%%
#fill in missing values interpolation using years col to specfiy the weighting for distance from closest year with data
Battery_cost_per_EV_USA_China_World_interpolated = Battery_cost_per_EV_USA_China_World_interpolated.interpolate(method='time', limit_direction='both')#by setting limt direction to both we get will be padding data that is on the ends with the closest value

#%%
#convert year col to int
Battery_cost_per_EV_USA_China_World_interpolated = Battery_cost_per_EV_USA_China_World_interpolated.reset_index()
Battery_cost_per_EV_USA_China_World_interpolated['Year'] = Battery_cost_per_EV_USA_China_World_interpolated['Year'].dt.year
#make year col the index again 
Battery_cost_per_EV_USA_China_World_interpolated = Battery_cost_per_EV_USA_China_World_interpolated.set_index('Year')
#%%
#save data to excel as a checpoint. It can now be multiplied by saes of evs per year to calculate the cost of batteries for each economy. We will calculate this using each region's min/max cost of battery and look at the results
Battery_cost_per_EV_USA_China_World_interpolated.to_csv('../intermediate_data/Battery_cost_per_EV_USA_China_World_interpolated.csv')

#%%
