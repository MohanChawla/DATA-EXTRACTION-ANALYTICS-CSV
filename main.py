# Project: Data_Extraction and Analytics from CSV file
# Author: Mohan Chawla

import pandas as pd

P_PERCENTAGE = 1.03
P_AMOUNT = 150

# reading the csv file into dataframe
data = pd.read_csv("07_june_2022.csv")

# getting unique values from SKU column in list format
data_list = data.sku.unique()

# Creating a separate data frame for each SKU
# From each file, remove column SKU and add columns amt having values in sz, wght columns multiplied
# Add another column s_num and fill with -1
# Convert it to csv file with name as SKU name
for sku in data_list:
    new_df = data[data.sku == sku]
    new_df.drop('sku', axis=1, inplace=True)
    new_df["amt"] = new_df.sz * new_df.wght
    new_df = new_df.round(2)
    new_df = new_df.reindex(columns=new_df.columns.tolist() + ["s_num"])
    new_df.s_num = -1
    new_df.to_csv(f"extracted_files/{sku}.csv", index=False)

# In each file, check:
# For every procure entry in the type column, check if there is any sold entry
# that satisfy 3 conditions such that:
# sold entry weight > procure entry weight*percentage
# sold entry amount is greater than procure entry amount by P_Amount
# sold entry size = procure entry size
# mark all such entries
for sku in data_list:
    temp_df = pd.read_csv(f"extracted_files/{sku}.csv")
    for index, row in temp_df.iterrows():
        if row.type == "procure" and row.s_num == -1:
            for ind, rw in temp_df.iterrows():
                if rw.type == "sold" and row.sz == rw.sz and rw.s_num == -1 \
                        and rw.wght > row.wght * P_PERCENTAGE and rw.amt - row.amt > P_AMOUNT:
                    temp_df.loc[ind, 's_num'] = index
                    temp_df.loc[index, 's_num'] = ind
                    break
    temp_df.to_csv(f"extracted_files/{sku}.csv")

    # For each file, remove marked procure, sold pairs and create a new csv file
    for index, row in temp_df.iterrows():
        if row.s_num != -1:
            temp_df.drop(index, inplace=True)
    temp_df.to_csv(f"simplified_files/{sku}_Simplified.csv")
