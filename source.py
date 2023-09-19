#navigate folders 
from pathlib import Path
#dataframe
import pandas as pd


#%% get current directory
cwd = Path.cwd()
out_path_files = Path(cwd, "Out/")

#%% read the files
DataH22 = pd.read_csv(Path('In/info_home/2022/data.csv'), sep=';', encoding="utf8")
ValueH22 = pd.read_csv(Path('In/info_home/2022/values.csv'), encoding="utf8")
VariablesH22 = pd.read_csv(Path('In/info_home/2022/variables.csv'), encoding="utf8")

DataH21 = pd.read_csv(Path('In/info_home/2021/data.csv'), encoding="utf8")
ValueH21 = pd.read_csv(Path('In/info_home/2021/values.csv'), encoding="utf8")
VariablesH21 = pd.read_csv(Path('In/info_home/2021/variables.csv'), encoding="utf8")

DataH20 = pd.read_csv(Path('In/info_home/2020/data.csv'), encoding="utf8")
ValueH20 = pd.read_csv(Path('In/info_home/2020/values.csv'), encoding="utf8")
VariablesH20 = pd.read_csv(Path('In/info_home/2020/variables.csv'), encoding="utf8")

DataR20 = pd.read_csv(Path('In/info_residents/2020/data.csv'), encoding="utf8")
ValueR20 = pd.read_csv(Path('In/info_residents/2020/values.csv'), encoding="utf8")
VariablesR20 = pd.read_csv(Path('In/info_residents/2020/variables.csv'), encoding="cp1252")

#change all column names to proper variable names
ValueH22.columns = ['Value', 'Num', 'Label']
ValueH21.columns = ['Value', 'Num', 'Label']
ValueH20.columns = ['Value', 'Num', 'Label']

VariablesH22.columns = ['Variable', 'Position', 'Label', 'LevelMeasurement']
VariablesH21.columns = ['Variable', 'Position', 'Label', 'LevelMeasurement']
VariablesH20.columns = ['Variable', 'Position', 'Label', 'LevelMeasurement']

VariablesR20.columns = ['Variable', 'Position', 'Label', 'LevelMeasurement']

ValueR20.columns = ['Value', 'Num', 'Label']

#%%clean names and format
ValueH20['Value'] = ValueH20['Value'].fillna(method='ffill')
ValueH21['Value'] = ValueH21['Value'].fillna(method='ffill')
ValueH22['Value'] = ValueH22['Value'].fillna(method='ffill')

ValueR20['Value'] = ValueR20['Value'].fillna(method='ffill')
# %%

#list unique values for visual inspection
VariablesH20[['Variable']].stack().unique().tolist()
VariablesH21[['Variable']].stack().unique().tolist()
VariablesH22[['Variable']].stack().unique().tolist()

VariablesR20[['Variable']].stack().unique().tolist()
#change all words t lower case
VariablesH20 = VariablesH20.applymap(lambda x: x.lower() if isinstance(x, str) else x)
VariablesH21 = VariablesH21.applymap(lambda x: x.lower() if isinstance(x, str) else x)
VariablesH22 = VariablesH22.applymap(lambda x: x.lower() if isinstance(x, str) else x)

# Merge the DataFrames
# track rows by adding a index
# Add index as a column in each DataFrame
VariablesH20['index_20'] = VariablesH20.index
VariablesH21['index_21'] = VariablesH21.index
VariablesH22['index_22'] = VariablesH22.index

#delete code from label
#regular expressions '^h\d' find letter h and number at the beggining 
mask = VariablesH20['Label'].str.match(r'^h\d')
VariablesH20.loc[mask, 'Label'] = VariablesH20.loc[mask, 'Label'].str[4:]
# Split by space, remove the first word and then join back the string
VariablesH20.loc[mask, 'Label'] = VariablesH20.loc[mask, 'Label'].str.split().apply(lambda x: ' '.join(x[1:]) if len(x) > 1 else x[0])

mask = VariablesH21['Label'].str.match(r'^h\d')
VariablesH21.loc[mask, 'Label'] = VariablesH21.loc[mask, 'Label'].str[4:]
# Split by space, remove the first word and then join back the string
VariablesH21.loc[mask, 'Label'] = VariablesH21.loc[mask, 'Label'].str.split().apply(lambda x: ' '.join(x[1:]) if len(x) > 1 else x[0])

mask = VariablesH22['Label'].str.match(r'^h\d')
VariablesH22.loc[mask, 'Label'] = VariablesH22.loc[mask, 'Label'].str[4:]
# Split by space, remove the first word and then join back the string
VariablesH22.loc[mask, 'Label'] = VariablesH22.loc[mask, 'Label'].str.split().apply(lambda x: ' '.join(x[1:]) if len(x) > 1 else x[0])

#find the questions that are similar across all years we cant use codes since thet change over time 
merged_df_Etiqueta =       VariablesH20[['Label', 'index_20']].merge(VariablesH21[['Label', 'index_21']], on='Label', how='inner').merge(VariablesH22[['Label', 'index_22']], on='Label', how='inner')

# save the questions that are not equal for visual inspection
merged_df_outer_Etiqueta = VariablesH20[['Label', 'index_20']].merge(VariablesH21[['Label', 'index_21']], on='Label', how='outer').merge(VariablesH22[['Label', 'index_22']], on='Label', how='outer')
non_equal_df_Etiqueta  = merged_df_outer_Etiqueta[merged_df_outer_Etiqueta[['index_20', 'index_21', 'index_22']].isnull().any(axis=1)]
file_name = 'non_equal_Etiqueta'
file_save = out_path_files / (file_name + ".csv")
non_equal_df_Etiqueta.to_csv(file_save)


#final data table
DataHf2020 = DataH20.iloc[:,merged_df_Etiqueta['index_20']]
DataHf2020['year'] = 2020
DataHf2021 = DataH21.iloc[:,merged_df_Etiqueta['index_21']]
DataHf2021['year'] = 2021
DataHf2022 = DataH22.iloc[:,merged_df_Etiqueta['index_22']]
DataHf2022['year'] = 2022
DataHf2020.columns = DataHf2022.columns
DataHf2021.columns = DataHf2022.columns
frames = [DataHf2020, DataHf2021, DataHf2022]
DataH = pd.concat(frames)
file_name = 'DataH'
file_save = out_path_files / (file_name + ".csv")
DataH.to_csv(file_save)