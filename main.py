import numpy as np
import pandas as pd

#  showing all table 
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# loading datas 
data = pd.read_csv('data.csv')
data_GCP = pd.read_csv('gcp.csv')

#  adding point type col to the data table (0,1,2,3) 
data.insert(loc=5, column='POINT.TYPE', value=0)

#  giving each point its code based on its type
for i in range(len(data)):
    for j in range(len(data_GCP)):
        if data.iloc[i, 2] == data_GCP.iloc[j, 0]:
            if pd.isnull(data_GCP.iloc[j, 3]):
                data.iloc[i, 5] = 2
            elif pd.isnull(data_GCP.iloc[j, 1]) and pd.isnull(data_GCP.iloc[j, 2]):
                data.iloc[i, 5] = 3
            else:
                data.iloc[i, 5] = 1

# removing duplicate datas & selecting tie ppints 
code_df = data[data["POINT.TYPE"]==0]['code'].drop_duplicates()
code_list = list(code_df)

# Create a new DataFrame 'new_data' with zeros
new_data = pd.DataFrame(0, index=range(14), columns=code_df)
new_data.insert(0, 'Ran', 0)
new_data.insert(1, 'Pic', 0)
new_data.loc[0:7, 'Ran'] = 1
new_data.loc[7:, 'Ran'] = 2

for i in range(7):
    new_data.loc[i, 'Pic'] = i+1  
    new_data.loc[i+7, 'Pic'] = i+1 

for i in range(len(new_data)): 
    for j in range(2, len(code_list)+2): 
        a =code_list[j-2]
        for k in range(len(data)):  
            if new_data.loc[i, 'Ran'] == data.loc[k, 'ran'] and new_data.loc[i, 'Pic'] == data.loc[k, 'photo']: 
                if a == data.loc[k, 'code']:  
                    new_data.iloc[i,j] = 1 
                     
# creating coefficient matrix  and calculating appriximates values by comformal model //////////////////////////

# khodam------------------------------------------------------------------------------------------

A_e = np.zeros((374,56))

for ran_counter in range(2):

    for pic_counter in range(7):

        for point_counter in range(len(data)):

            for j in range(0,56,4):

                if data.loc[point_counter,'ran'] == ran_counter and data.loc[point_counter,'photo'] == pic_counter :

                    if data.loc[point_counter,"POINT.TYPE"]== 1 :

                        A_e[2*point_counter-1,j:j+4] = [data.loc[point_counter,'x'] , -data.loc[point_counter,'y']  , 1 , 0]

                        A_e[2*point_counter,j:j+4] = [data.loc[point_counter,'y'] , data.loc[point_counter,'x']  , 0 , 1]

                    elif data.loc[point_counter,"POINT.TYPE"]==0 :  

                        A_e[2*point_counter-1,j:j+4] = [5,0,0,0]
                        
                        A_e[2*point_counter,j:j+4] = [5,0,0,5] 


# ----------------------------------------------------------------------------------------------- 

# AI ----------------------------------
# A_e = np.zeros((len(data) * 2, 56))

# # Populate the coefficient matrix
# for ran_counter in range(2):
#     for pic_counter in range(1, 8):  # Adjusted range to match photo IDs from 1 to 7
#         for point_counter in range(len(data)):
#             for j in range(0, 56, 4):
#                 if data.loc[point_counter, 'ran'] == ran_counter + 1 and data.loc[point_counter, 'photo'] == pic_counter:
#                     print("Point matched for ran_counter:", ran_counter, "and pic_counter:", pic_counter)
#                     print("POINT.TYPE:", data.loc[point_counter, "POINT.TYPE"])
#                     print("Indexing:", 2 * point_counter, "and", 2 * point_counter + 1, ":", j, "to", j+4)
#                     if data.loc[point_counter, "POINT.TYPE"] == 1:
#                         A_e[2 * point_counter, j:j+4] = [data.loc[point_counter, 'x'], -data.loc[point_counter, 'y'], 1, 0]
#                         A_e[2 * point_counter + 1, j:j+4] = [data.loc[point_counter, 'y'], data.loc[point_counter, 'x'], 0, 1]
#                         print("Populated with values:", A_e[2 * point_counter, j:j+4], "and", A_e[2 * point_counter + 1, j:j+4])
#                     elif data.loc[point_counter, "POINT.TYPE"] == 0:
#                         A_e[2 * point_counter, j:j+4] = [0, 0, 0, 0]
#                         A_e[2 * point_counter + 1, j:j+4] = [0, 0, 0, 0]
#                         print("Set to zeros.")

print("Coefficient matrix A_e:")
print(A_e)





        














