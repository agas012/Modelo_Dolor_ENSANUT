#navigate folders 
from pathlib import Path
#dataframe
import pandas as pd


#%% get current directory
cwd = Path.cwd()
out_path_files = Path(cwd, "Out/")

#%% read the files
DataI22 = pd.read_csv(Path('In/info_home/2022/data.csv'), sep=';', encoding="utf-8")
ValueI22 = pd.read_csv(Path('In/info_home/2022/values.csv'), encoding="utf-8")
VariablesI22 = pd.read_csv(Path('In/info_home/2022/variables.csv'), encoding="utf-8")

DataI21 = pd.read_csv(Path('In/info_home/2021/data.csv'), encoding="utf-8")
ValueI21 = pd.read_csv(Path('In/info_home/2021/values.csv'), encoding="utf-8")
VariablesI21 = pd.read_csv(Path('In/info_home/2021/variables.csv'), encoding="utf-8")

DataI20 = pd.read_csv(Path('In/info_home/2020/data.csv'), encoding="utf-8")
ValueI20 = pd.read_csv(Path('In/info_home/2020/values.csv'), encoding="utf-8")
VariablesI20 = pd.read_csv(Path('In/info_home/2020/variables.csv'), encoding="utf-8")

DataR20 = pd.read_csv(Path('In/info_residents/2020/data.csv'), encoding="utf-8")
ValueR20 = pd.read_csv(Path('In/info_residents/2020/values.csv'), encoding="utf-8")
VariablesR20 = pd.read_csv(Path('In/info_residents/2020/variablesf.csv'), encoding="utf-8")

#concatenate VariablesI20 VariablesR20 = variablesC20

#%%clean names and format
ValueI20.rename(columns={'Unnamed: 1':'num'}, inplace=True)
ValueI20['Valor'] = ValueI20['Valor'].fillna(method='ffill')

ValueI21.rename(columns={'Unnamed: 1':'num'}, inplace=True)
ValueI21['Valor'] = ValueI21['Valor'].fillna(method='ffill')

ValueI22.rename(columns={'Unnamed: 1':'num'}, inplace=True)
ValueI22['Valor'] = ValueI22['Valor'].fillna(method='ffill')
# %%

#list unique values for visual inspection
VariablesI20[['Variable']].stack().unique().tolist()
VariablesI21[['Variable']].stack().unique().tolist()
VariablesI22[['Variable']].stack().unique().tolist()

VariablesR20[['Variable']].stack().unique().tolist()
#change all words t lower case
VariablesI20 = VariablesI20.applymap(lambda x: x.lower() if isinstance(x, str) else x)
VariablesI21 = VariablesI21.applymap(lambda x: x.lower() if isinstance(x, str) else x)
VariablesI22 = VariablesI22.applymap(lambda x: x.lower() if isinstance(x, str) else x)

# Merge the DataFrames
# track rows by adding a index

# Add index as a column in each DataFrame
VariablesI20['index_20'] = VariablesI20.index
VariablesI21['index_21'] = VariablesI21.index
VariablesI22['index_22'] = VariablesI22.index

#this doesnt work because ansanut changes the codes each year
merged_df =       VariablesI20[['Variable', 'index_20']].merge(VariablesI21[['Variable', 'index_21']], on='Variable', how='inner').merge(VariablesI22[['Variable', 'index_22']], on='Variable', how='inner')
merged_df_outer = VariablesI20[['Variable', 'index_20']].merge(VariablesI21[['Variable', 'index_21']], on='Variable', how='outer').merge(VariablesI22[['Variable', 'index_22']], on='Variable', how='outer')
# Filter out rows where values are present in all three original DataFrames
non_equal_df = merged_df_outer[merged_df_outer[['index_20', 'index_21', 'index_22']].isnull().any(axis=1)]
file_name = 'non_equal'
file_save = out_path_files / (file_name + ".csv")
non_equal_df.to_csv(file_save)

#we need to use the text of the questions to find similar questions across the years
merged_df_Etiqueta =       VariablesI20[['Etiqueta', 'index_20']].merge(VariablesI21[['Etiqueta', 'index_21']], on='Etiqueta', how='inner').merge(VariablesI22[['Etiqueta', 'index_22']], on='Etiqueta', how='inner')
merged_df_outer_Etiqueta = VariablesI20[['Etiqueta', 'index_20']].merge(VariablesI21[['Etiqueta', 'index_21']], on='Etiqueta', how='outer').merge(VariablesI22[['Etiqueta', 'index_22']], on='Etiqueta', how='outer')
# Filter out rows where values are present in all three original DataFrames
non_equal_df_Etiqueta  = merged_df_outer_Etiqueta[merged_df_outer_Etiqueta[['index_20', 'index_21', 'index_22']].isnull().any(axis=1)]
file_name = 'non_equal_Etiqueta'
file_save = out_path_files / (file_name + ".csv")
non_equal_df_Etiqueta.to_csv(file_save)



# Sample DataFrames
df1 = pd.DataFrame({
    'column_name': [1, 2, 3, 4],
    'other_data1': ['a', 'b', 'c', 'd']
})

df2 = pd.DataFrame({
    'column_name': [3, 1, 4, 6],
    'other_data2': ['e', 'f', 'g', 'h']
})

df3 = pd.DataFrame({
    'column_name': [1, 4, 7, 8],
    'other_data3': ['i', 'j', 'k', 'l']
})

# Merge the DataFrames
merged_df = df1[['column_name']].merge(df2[['column_name']], on='column_name', how='inner').merge(df3[['column_name']], on='column_name', how='inner')

print(merged_df)






speeds = pd.DataFrame([
        ("bird", "Falconiformes", 389.0),
        ("bird", "Psittaciformes", 24.0),
        ("mammal", "Carnivora", 80.2),
        ("mammal", "Primates", 0),
        ("mammal", "Carnivora", 58),
    ],
    index=["falcon", "parrot", "lion", "monkey", "leopard"],
    columns=("class", "order", "max_speed"),
)

speeds.groupby("class")['class'].count()

VariablesI22.groupby("Variable")['Variable'].count()