#navigate folders 
from pathlib import Path
#dataframe
import pandas as pd

#Math
import numpy as np
import math

#%% get current directory
cwd = Path.cwd()
out_path_files = Path(cwd, "Out/")

#%% read the files+
DataH21 = pd.read_csv(Path('In/info_home/2021/data.csv'), encoding="utf8")
ValueH21 = pd.read_csv(Path('In/info_home/2021/values.csv'), encoding="utf8")
VariablesH21 = pd.read_csv(Path('In/info_home/2021/variables.csv'), encoding="utf8")

DataH22 = pd.read_csv(Path('In/info_home/2022/data.csv'), sep=';', encoding="utf8")
ValueH22 = pd.read_csv(Path('In/info_home/2022/values.csv'), encoding="utf8")
VariablesH22 = pd.read_csv(Path('In/info_home/2022/variables.csv'), encoding="utf8")

#change all column names to proper variable names
ValueH21.columns = ['Value', 'Num', 'Label']
ValueH22.columns = ['Value', 'Num', 'Label']
VariablesH21.columns = ['Variable', 'Position', 'Label', 'LevelMeasurement']
VariablesH22.columns = ['Variable', 'Position', 'Label', 'LevelMeasurement']

# %%
#change all words t lower case
VariablesH21 = VariablesH21.applymap(lambda x: x.lower() if isinstance(x, str) else x)
VariablesH22 = VariablesH22.applymap(lambda x: x.lower() if isinstance(x, str) else x)

#list unique values for visual inspection
# VariablesH21[['Variable']].stack().unique().tolist()
# VariablesH22[['Variable']].stack().unique().tolist()

# VariablesH21[['Label']].stack().unique().tolist()
# VariablesH22[['Label']].stack().unique().tolist()

#manual concatenation
H21array = np.r_[1,31,30,33,34,35,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,61,62,63,64,65,66,67,68,69,80,81,82,83,84,86,87,88,91,92,93,95,96,97,101,102,104,105,125,126,127,128,129,130,131,132,133,134,135,136]
H22array = np.r_[1,32,33,34,35,36,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,72,73,74,79,80,81,82,83,84,85,86,87,88,101,102,103,104,105,106,107,108,109,110,111,112]
H21array = H21array-1
H22array = H22array-1

DataH21_sub = DataH21.iloc[:,H21array]
DataH22_sub = DataH22.iloc[:,H22array]
DataH21_sub['year'] = 2021
DataH22_sub['year'] = 2022

DataH21_sub.columns.tolist()
DataH22_sub.columns.tolist()

frames = [DataH21_sub, DataH22_sub]
DataH = pd.concat(frames)
convert_dict = {
'region': 'category',
'entidad': 'category',
'desc_ent': 'category',
'municipio': 'category',
'desc_mun': 'category',
'nota1a': 'category',
'h0101': 'category',
'h0102': 'category',
'h0103': 'category',
'h0104': 'category',
'h0105': 'category',
'h0106': 'category',
'h0107': 'category',
'h0108': 'category',
'h0109': 'category',
'h0110': 'category',
'h0111': 'category',
'h0112': 'category',
'h0113': 'category',
'h0114': 'category',
'h0118': 'category',
'h0119': 'category',
'h0120': 'category',
'h0121': 'category',
'h0122': 'category',
'h0123': 'category',
'h0124': 'category',
'h0125': 'category',
'nota2': 'category',
'h0201': 'category',
'h0202': 'category',
'h0203': 'category',
'h0204': 'category',
'h305t': 'category',
'h305i': 'category',
'h0327': 'category',
'h0501a': 'category',
'h0501b': 'category',
'h0501c': 'category',
'h0501e': 'category',
'h0501f': 'category',
'h0501g': 'category',
'h0501k': 'category',
'h0501l': 'category',
'h0501n': 'category',
'h0501o': 'category',
'h0801': 'category',
'h0802': 'category',
'h0803': 'category',
'h0804': 'category',
'h0805': 'category',
'h0806': 'category',
'h0807': 'category',
'h0808': 'category',
'h0809': 'category',
'h0810': 'category',
'h0811': 'category',
'h0812': 'category',
'year': 'int64'
}
DataH = DataH.astype(convert_dict)

file_name = 'DataH'
file_save = out_path_files / (file_name + ".csv")
DataH.to_csv(file_save)


