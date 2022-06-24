#integrate
#%%
#CONFIG
execfile("config.py")#usae this to load libraries and set variables. Feel free to edit that file as you need

#%%
os.chdir("./analysis_code")

execfile("1_EV_battery_prices.py")
execfile("2_EV_sales.py")
execfile("3_EV_total_cost_of_sales.py")
execfile("4_EV_total_cost_plots.py")


# %%


#%%
#CONFIG
#Senareo 