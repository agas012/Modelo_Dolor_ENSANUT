#navigate folders 
from pathlib import Path
#dataframe
import pandas as pd
from datetime import date

#Math
import numpy as np
import math

#mi funciones
from module_stata import populationtest
from module_stata import ortest

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

DataR21 = pd.read_csv(Path('In/info_residents/2021/data.csv'), encoding="utf-8")
ValueR21 = pd.read_csv(Path('In/info_residents/2021/values.csv'), encoding="cp1252")
VariablesR21 = pd.read_csv(Path('In/info_residents/2021/variables.csv'),sep=';' ,encoding="cp1252")

DataR22 = pd.read_csv(Path('In/info_residents/2022/data.csv'),sep = ';' , encoding="utf-8")
ValueR22 = pd.read_csv(Path('In/info_residents/2022/values.csv'), encoding="cp1252")
VariablesR22 = pd.read_csv(Path('In/info_residents/2022/variables.csv'), encoding="cp1252")

DataHe21 = pd.read_csv(Path('In/info_health/2021/data.csv'), encoding="utf8")
ValueHe21 = pd.read_csv(Path('In/info_health/2021/values.csv'), encoding="utf8")
VariablesHe21 = pd.read_csv(Path('In/info_health/2021/variables.csv'), encoding="utf8")

DataHe22 = pd.read_csv(Path('In/info_health/2022/data.csv'), sep=';', encoding="utf8")
ValueHe22 = pd.read_csv(Path('In/info_health/2022/values.csv'), encoding="utf8")
VariablesHe22 = pd.read_csv(Path('In/info_health/2022/variables.csv'), encoding="utf8")
#change all column names to proper variable names
ValueH21.columns = ['Value', 'Num', 'Label']
ValueH22.columns = ['Value', 'Num', 'Label']
VariablesH21.columns = ['Variable', 'Position', 'Label', 'LevelMeasurement']
VariablesH22.columns = ['Variable', 'Position', 'Label', 'LevelMeasurement']

VariablesR21.columns = ['Variable', 'Position', 'Label', 'LevelMeasurement']
VariablesR22.columns = ['Variable', 'Position', 'Label', 'LevelMeasurement']
ValueR21.columns = ['Value', 'Num', 'Label']
ValueR22.columns = ['Value', 'Num', 'Label']

ValueHe21.columns = ['Value', 'Num', 'Label']
ValueHe22.columns = ['Value', 'Num', 'Label']
VariablesHe21.columns = ['Variable', 'Position', 'Label']
VariablesHe22.columns = ['Variable', 'Position', 'Label']
# %%
#change all words t lower case
VariablesH21 = VariablesH21.applymap(lambda x: x.lower() if isinstance(x, str) else x)
VariablesH22 = VariablesH22.applymap(lambda x: x.lower() if isinstance(x, str) else x)
VariablesR21 = VariablesR21.applymap(lambda x: x.lower() if isinstance(x, str) else x)
VariablesR22 = VariablesR22.applymap(lambda x: x.lower() if isinstance(x, str) else x)
VariablesHe21 = VariablesHe21.applymap(lambda x: x.lower() if isinstance(x, str) else x)
VariablesHe22 = VariablesHe22.applymap(lambda x: x.lower() if isinstance(x, str) else x)

#manual concatenation
H21array = np.r_[1,31,30,33,34,35,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,61,62,63,64,65,66,67,68,69,80,81,82,83,84,86,87,88,91,92,93,95,96,97,101,102,104,105,125,126,127,128,129,130,131,132,133,134,135,136]
H22array = np.r_[1,32,33,34,35,36,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,72,73,74,79,80,81,82,83,84,85,86,87,88,101,102,103,104,105,106,107,108,109,110,111,112]
H21array = H21array-1
H22array = H22array-1

R21array = np.r_[0,1,2,4,5,6,7,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,39,40,41,42,43,44,45,46,47,48,49,50,51,52,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,86,87,88,89,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,108,109,111,112,114,115,118,119,127,128,151,189,190,191,192,193,194,195,196,197,198,199,200,201,202,203,204,205,206,207,208,209,211,212,216,219,220,221,222,223,236,237,245,246,247,248,249,10]
R22array = np.r_[0,1,2,4,5,6,7,8,9,10,11,12,13,14,15,16,17,19,20,21,22,23,24,25,26,30,27,28,29,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,128,129,131,132,133,147,148,150,151,152,153,154,155]

He21array = np.r_[1,2,47,50,51,52,53,54,55,56,57,58,59,60,61,62,72,65,66,67,68,69,70,71,77,78,80,83,81,82,84,85,88,91,92,93,94,95,97,98,100,99,102,101,103,105,106,107,108,109,100,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,134,135,136,137,138,139,140,141,142,143,146,148,147,150,152,151,153,156,158,159,160,161,162,175,176,177,185,186,187,196,197,198,199,200,201,202,204,205,206,223,218,213,224,219,214,225,220,215,226,221,216,212,230,231,232,233,234,235,236,247,237,238,239,240,241,242,243,244,245,246,248,249,250,251,252,265,253,254,255,256,257,258,259,260,261,262,263,264,266,267,268,269,270,271,274,275,272,273,278,276,277,280,281,283,284,285,286,287,288,289,290,291,292,293,294,295,296,297,298,299,300,302,303,304,308,309,310,311,312,313,314,315,316,317,318,319,321,322,327,328,329,331,333,335,337,338,341,342,345,346,349,350,353,354,357,358,361,362,365,366,369,370,373,374,380,381,379,378,387,388,386,385,394,395,393,392,399,400,401,403,404,405,406,407,409,410,413,414,417,418,421,422,426,429,430,433,434,437,438,444,445,443,442,451,452,450,449,458,459,457,456,463,472,481,490,508,517,526,535,544,464,465,473,474,482,483,491,492,509,510,518,519,527,528,536,537,545,546,466,475,484,493,511,520,529,538,547,467,476,485,494,512,521,530,539,548,468,477,486,495,513,522,531,540,459,469,478,487,496,514,523,532,541,550,470,471,479,480,488,489,497,498,515,516,524,525,533,534,542,543,551,552,563,564,565,566,567,568,581,582,583,584,585,586,589,590,591,592,593,601,594,595,596,597,598,599,600,612,613,614,616,617,618,619,620,621,622,623,624,625,626,627,630,631,632,633,634,635,636,637,638,639,640,641,642,644,645,647,648,649,650,651,652,653,654,42,41,651,695,32,34,38,31,699,698,40,694,7,13,19,25,29,5,11,17,23,693,6,12,18,24,28,4,10,16,22,33,462,562,587,588,628,629,643,646,43,63,64,75,76,144,145,183,184,210,211,228,229,325,326,330,377,441,448,455,384,391,696,697,30,9,15,21,27,39,692,8,14,20,26,37]
He22array = np.r_[1,2,45,46,47,48,49,50,51,52,53,54,55,56,57,58,68,61,62,63,64,65,66,67,71,72,73,76,74,75,77,78,81,84,85,86,87,88,89,93,95,94,97,96,98,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,129,130,131,132,133,134,135,136,137,138,141,143,142,144,147,146,148,153,155,156,157,158,159,171,172,173,177,178,179,180,181,182,183,184,185,186,188,189,190,203,199,195,204,200,196,205,201,197,206,202,198,194,209,210,211,212,213,214,215,226,216,217,218,219,220,221,222,223,224,225,227,228,229,230,231,244,232,233,234,235,236,237,238,239,240,241,242,243,245,246,247,248,249,250,253,254,251,252,257,255,256,259,260,262,263,264,265,266,267,268,269,270,271,272,273,274,275,276,277,278,279,281,282,283,285,286,287,288,289,290,291,292,293,294,295,296,298,299,302,303,304,306,308,310,312,313,314,315,316,317,318,319,320,321,322,323,324,325,326,327,328,329,330,331,335,336,334,333,340,341,339,338,345,346,344,343,358,359,360,362,363,364,365,366,368,369,370,371,372,373,374,375,377,378,379,380,381,382,383,387,388,386,385,392,393,391,390,397,398,396,395,410,419,428,437,446,455,464,473,482,411,412,420,421,429,430,438,439,447,448,456,457,465,466,474,475,483,484,413,422,431,440,449,458,467,476,485,414,423,432,441,450,459,468,477,486,415,424,433,442,451,460,469,478,487,416,425,434,443,452,461,470,479,488,417,418,426,427,435,436,444,445,453,454,462,463,471,472,480,481,489,490,492,493,494,495,496,497,498,499,500,501,502,503,506,507,508,509,510,518,511,512,513,514,515,516,517,520,521,522,523,524,525,526,527,528,529,530,531,532,533,534,537,538,539,540,541,542,543,544,545,546,547,548,549,551,552,554,555,556,557,558,559,560,561,43,42,562,566,34,36,38,33,570,569,40,565,10,16,22,28,32,8,14,20,26,564,9,15,21,27,31,7,13,19,25,35,409,491,504,505,535,536,550,553,44,59,60,69,70,139,140,175,176,192,193,207,208,300,301,305,332,384,389,394,337,342,567,568,572,12,18,24,30,39,563,11,17,23,29,571] 
He21array = He21array-1
He22array = He22array-1

DataH21_sub = DataH21.iloc[:,H21array]
DataH22_sub = DataH22.iloc[:,H22array]

DataR21_sub = DataR21.iloc[:,R21array]
DataR22_sub = DataR22.iloc[:,R22array]

DataHe21_sub = DataHe21.iloc[:,He21array]
DataHe22_sub = DataHe22.iloc[:,He22array]
He21arrayfix=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,160,161,162,163,164,165,166,167,168,169,170,171,172,173,174,175,176,177,178,179,180,181,182,183,184,185,186,187,188,189,190,191,192,193,194,195,196,197,198,199,200,201,202,203,204,205,206,207,208,209,210,211,212,213,214,215,216,217,218,219,220,221,222,223,224,225,226,227,228,229,230,231,232,233,234,235,236,237,238,239,240,241,242,243,244,245,246,247,248,249,250,251,252,253,254,255,256,257,258,259,260,261,262,263,264,265,266,267,268,269,270,271,272,273,274,275,276,277,278,279,280,281,282,283,284,285,286,287,288,289,290,291,292,293,294,295,296,297,298,299,300,301,302,303,304,305,306,307,308,309,310,311,312,313,314,315,316,317,318,319,320,321,322,323,324,325,326,327,328,329,330,331,332,333,334,335,336,338,339,340,341,342,343,344,345,346,347,348,349,350,351,352,353,354,355,356,357,358,359,360,361,362,363,364,365,366,367,368,369,370,371,372,373,374,375,376,377,378,379,380,381,382,383,384,385,386,387,388,389,390,391,392,393,394,395,396,397,398,399,400,401,402,403,404,405,406,407,408,409,410,411,412,413,414,415,416,417,418,419,420,421,422,423,424,425,426,427,428,429,431,432,433,434,435,436,437,438,459,484,485,486,487,488,489,490,491,492,493,494,495,496,497]
DataHe21_sub = DataHe21_sub.iloc[:,He21arrayfix]
DataHe22_sub = DataHe22_sub.iloc[:,He21arrayfix]
DataHe22_sub.columns.tolist()

#nan fill
DataH21_sub.replace( ' ', np.nan, inplace=True)
DataH22_sub.replace( ' ', np.nan, inplace=True)
DataR21_sub.replace( ' ', np.nan, inplace=True)
DataR22_sub.replace( ' ', np.nan, inplace=True)
DataHe21_sub.replace( ' ', np.nan, inplace=True)
DataHe22_sub.replace( ' ', np.nan, inplace=True)


convert_dict = {
'region': 'category',
'entidad': 'category',
'desc_ent': 'category',
'municipio': 'category', #q
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
'h0812': 'category'
}
DataH21_sub = DataH21_sub.astype(convert_dict)
DataH22_sub = DataH22_sub.astype(convert_dict)

convert_dict = {
 'entidad1': 'category',
 'desc_ent1': 'category',
 'municipio1': 'category',
 'desc_mun1': 'category',
 'h0302': 'category',
 'h0303': 'category',
 'h0304': 'category',
 'h0304d': 'category',
 'h0304m': 'category',
 'h0304a': 'float64',
 'meses': 'category',
 'h0305': 'category',
 'h0305_es': 'category',
 'h0306': 'category',
 'h0306e': 'category',
 'h0306p': 'category',
 'h0307': 'category',
 'h0307q': 'category',
 'h0308': 'category',
 'h0308q': 'category',
 'h0309': 'category',
 'h0309e': 'category',
 'H0310A': 'category',
 'H0310B': 'category',
 'H0310C': 'category',
 'h0310e': 'category',
 'h0311': 'category',
 'h0312': 'category',
 'h0313': 'category',
 'h0314': 'category',
 'h0316': 'category',
 'h0316esp': 'category',
 'h0317a': 'category',
 'h0317g': 'category',
 'h0318': 'category',
 'intp3': 'category',
 'h0319': 'category',
 'h0320': 'category',
 'h0320q': 'category',
 'h0321': 'category',
 'h0322': 'category',
 'h0323': 'category',
 'h0324': 'category',
 'h0324esp': 'category',
 'h0401': 'category',
 'h0402': 'category',
 'h0402esp': 'category',
 'h0403': 'category',
 'h0404': 'category',
 'H0405A': 'category',
 'H0405B': 'category',
 'H0405C': 'category',
 'h0405esp': 'category',
 'h0406': 'category',
 'H0407A': 'category',
 'H0407B': 'category',
 'H0407C': 'category',
 'h0407esp': 'category',
 'h0408': 'category',
 'h0408esp': 'category',
 'H0409A': 'category',
 'H0409B': 'category',
 'H0409C': 'category',
 'h0601a': 'category',
 'h0603a': 'category',
 'h0601b': 'category',
 'h0603b': 'category',
 'h0601c': 'category',
 'h0603c': 'category',
 'h0601d': 'category',
 'h0603d': 'category',
 'h0601e': 'category',
 'h0603e': 'category',
 'h0601f': 'category',
 'h0603f': 'category',
 'h0601g': 'category',
 'h0603g': 'category',
 'h0601h': 'category',
 'h0603h': 'category',
 'h0601i': 'category',
 'h0603i': 'category',
 'h0601j': 'category',
 'h0603j': 'category',
 'h0601k': 'category',
 'h0603k': 'category',
 'h0601l': 'category',
 'h0603l': 'category',
 'h0601m': 'category',
 'h0603m': 'category',
 'h0601n': 'category',
 'h0603n': 'category',
 'h0604ba': 'category',
 'h0604bb': 'category',
 'h1205': 'category',
 'H1213A': 'category',
 'H1213B': 'category',
 'H1213C': 'category',
 'H1213D': 'category',
 'H1213E1': 'category',
 'H1213F': 'category',
 'H1213G': 'category',
 'H1213H': 'category',
 'H1213I': 'category',
 'H1213J': 'category',
 'H1213K': 'category',
 'H1213L': 'category',
 'H1213M': 'category',
 'H1213N': 'category',
 'H1213O': 'category',
 'H1213P': 'category',
 'H1213Q': 'category',
 'H1213R': 'category',
 'H1213S': 'category',
 'H1213T': 'category',
 'h1213e': 'category',
 'h1215': 'category',
 'h1216': 'category',
 'h1602': 'category',
 'h16041m': 'category',
 'h16041a': 'category',
 'h16042d': 'category',
 'h16042m': 'category',
 'h16042a': 'category',
 'h1607': 'category',
 'h1607e': 'category',
 'region': 'category',
 'entidad': 'category',
 'estrato': 'category',
 'est_sel': 'category'
}
DataR21_sub = DataR21_sub.astype(convert_dict)
DataR22_sub = DataR22_sub.astype(convert_dict)

convert_dict = {
 'a0104': 'category',
 'a0107': 'category',
 'a0108': 'category',
 'a0109': 'category',
 'A0110A': 'category',
 'A0110B': 'category',
 'A0110C': 'category',
 'A0110D': 'category',
 'A0110E': 'category',
 'A0110F': 'category',
 'A0110G': 'category',
 'A0110H': 'category',
 'A0110I': 'category',
 'a01esp': 'category',
 'a0202': 'category',
 'a0211': 'category',
 'a0212': 'category',
 'a0213': 'category',
 'a0214': 'category',
 'a0215': 'category',
 'a0216': 'category',
 'a0217': 'category',
 'a0301': 'category',
 'a0302': 'category',
 'a0303num': 'category',
 'a0304a': 'category',
 'a0304d': 'category',
 'a0304m': 'category',
 'a0305': 'category',
 'a0305esp': 'category',
 'a0306c': 'category',
 'a0306f': 'category',
 'a0306g': 'category',
 'a0306h': 'category',
 'a0306i': 'category',
 'a0306j': 'category',
 'a0306l': 'category',
 'a0307': 'category',
 'a0308a': 'category',
 'a0308m': 'category',
 'a0309a': 'category',
 'a0309m': 'category',
 'a0310': 'category',
 'A0312A': 'category',
 'A0312B': 'category',
 'A0312C': 'category',
 'A0312D': 'category',
 'a0313': 'category',
 'A0315A': 'category',
 'A0315B': 'category',
 'A0315C': 'category',
 'A0315D': 'category',
 'A0315E': 'category',
 'A0315F': 'category',
 'A0315G': 'category',
 'A0315H': 'category',
 'A0315I': 'category',
 'A0315J': 'category',
 'A0315K': 'category',
 'A0315L': 'category',
 'A0315M': 'category',
 'A0315N': 'category',
 'A0315O': 'category',
 'A0315P': 'category',
 'A0315Q': 'category',
 'A0315R': 'category',
 'A0315S': 'category',
 'A0315T': 'category',
 'A0315U': 'category',
 'A0315V': 'category',
 'a0316a': 'category',
 'a0316b': 'category',
 'a0316c': 'category',
 'a0316d': 'category',
 'a0316e': 'category',
 'a0316f': 'category',
 'a0316g': 'category',
 'a0316h': 'category',
 'a0316i': 'category',
 'a0316j': 'category',
 'a0401': 'category',
 'a0402a': 'category',
 'a0402m': 'category',
 'a0404': 'category',
 'a0405a': 'category',
 'a0405m': 'category',
 'a0406': 'category',
 'A0408A': 'category',
 'A0408C': 'category',
 'A0408D': 'category',
 'A0408E': 'category',
 'a0409': 'category',
 'a0409a': 'float64',
 'a0502a': 'category',
 'a0502b': 'category',
 'a0502c': 'category',
 'a0601a': 'category',
 'a0601b': 'category',
 'a0601c': 'category',
 'a0603': 'category',
 'a0604': 'category',
 'A0605A': 'category',
 'A0605B': 'category',
 'A0605C': 'category',
 'A0605D': 'category',
 'a0606': 'category',
 'A0607B': 'category',
 'A0607C': 'category',
 'A0607D': 'category',
 'a0701h': 'category',
 'a0701m': 'category',
 'a0701p': 'category',
 'a0702h': 'category',
 'a0702m': 'category',
 'a0702p': 'category',
 'a0703h': 'category',
 'a0703m': 'category',
 'a0703p': 'category',
 'a0704h': 'category',
 'a0704m': 'category',
 'a0704p': 'category',
 'a07her': 'category',
 'a0801': 'float64',
 'a0802': 'float64',
 'A0803A': 'category',
 'A0803B': 'category',
 'A0803C': 'category',
 'A0803D': 'category',
 'A0803E': 'category',
 'a0803esp': 'category',
 'A0803F': 'category',
 'A0803G': 'category',
 'A0803H': 'category',
 'A0803I': 'category',
 'A0803J': 'category',
 'A0803K': 'category',
 'A0803L': 'category',
 'A0803M': 'category',
 'A0803N': 'category',
 'A0803O': 'category',
 'A0804A': 'category',
 'A0804B': 'category',
 'A0804C': 'category',
 'A0804D': 'category',
 'A0804E': 'category',
 'a0804esp': 'category',
 'A0804F': 'category',
 'A0804G': 'category',
 'A0804H': 'category',
 'A0804I': 'category',
 'A0804J': 'category',
 'A0804K': 'category',
 'A0804L': 'category',
 'A0804M': 'category',
 'A0804N': 'category',
 'A0804O': 'category',
 'A0804P': 'category',
 'A0804Q': 'category',
 'a0805': 'category',
 'a0806': 'float64',
 'a0807': 'category',
 'a0808': 'category',
 'a0809': 'float64',
 'a0810a': 'float64',
 'a0810ad': 'float64',
 'a0810ae': 'float64',
 'a0810b': 'float64',
 'a0810c': 'float64',
 'a0811a': 'float64',
 'a0811d': 'float64',
 'a0811m': 'float64',
 'a0812': 'float64',
 'a0813': 'category',
 'a0814': 'float64',
 'a0815a': 'category',
 'a0815b': 'category',
 'a0815c': 'category',
 'a0815d': 'category',
 'a0815e': 'category',
 'a0815f': 'category',
 'a0815g': 'category',
 'a0815h': 'category',
 'a0815i': 'category',
 'a0815j': 'category',
 'a0815k': 'category',
 'a0815l': 'category',
 'a0815m': 'category',
 'a0815n': 'category',
 'a0815o': 'category',
 'a0815p': 'category',
 'a0816': 'category',
 'a0817': 'category',
 'a0818': 'category',
 'a0819k': 'float64',
 'a0821a': 'category',
 'a0821b': 'category',
 'a0821c': 'category',
 'a0821d': 'category',
 'a0821e': 'category',
 'a0821f': 'category',
 'a0821g': 'category',
 'a0821h': 'category',
 'a0821i': 'category',
 'a0821j': 'category',
 'a0822': 'category',
 'a0823': 'category',
 'a0824': 'category',
 'a0825': 'category',
 'a0901': 'category',
 'a0902': 'category',
 'a0903': 'category',
 'a0904': 'category',
 'a0906': 'category',
 'a0908': 'category',
 'a09091a': 'category',
 'a09092a': 'category',
 'a09093a': 'category',
 'a09101a': 'category',
 'a09102a': 'category',
 'a09103a': 'category',
 'a09104a': 'category',
 'a09111a': 'category',
 'a09121a': 'category',
 'a09122a': 'category',
 'a09131a': 'category',
 'a09131ed': 'category',
 'a09131nom': 'category',
 'a09132a': 'category',
 'a09132edad': 'category',
 'a09132nom': 'category',
 'a09133a': 'category',
 'a09133ed': 'category',
 'a09133nom': 'category',
 'a0914': 'category',
 'a0915': 'category',
 'a0916': 'category',
 'a0917': 'category',
 'a0918': 'category',
 'a0919': 'category',
 'a0920': 'category',
 'a0921': 'category',
 'a09221a': 'category',
 'a09222a': 'category',
 'a09223a': 'category',
 'a09231a': 'category',
 'a09233a': 'category',
 'a09234a': 'category',
 'a09241a': 'category',
 'a09251a': 'category',
 'a09251ed': 'category',
 'a09251nom': 'category',
 'a09252a': 'category',
 'a09252ed': 'category',
 'a09252nom': 'category',
 'a09253a': 'category',
 'a09253ed': 'category',
 'a09253nom': 'category',
 'a1001a': 'category',
 'a1001b': 'category',
 'a1001c': 'category',
 'a1001d': 'category',
 'a1001f': 'category',
 'a1001g': 'category',
 'a1001h': 'category',
 'a1001i': 'category',
 'a1001j': 'category',
 'a1002a': 'category',
 'a1002ae': 'category',
 'a1002b': 'category',
 'a1002be': 'category',
 'a1002c': 'category',
 'a1002ce': 'category',
 'a1002d': 'category',
 'a1002de': 'category',
 'a1002f': 'category',
 'a1002fe': 'category',
 'a1002g': 'category',
 'a1002ge': 'category',
 'a1002h': 'category',
 'a1002he': 'category',
 'a1002i': 'category',
 'a1002ie': 'category',
 'a1002j': 'category',
 'a1002je': 'category',
 'a1003a': 'category',
 'a1003b': 'category',
 'a1003c': 'category',
 'a1003d': 'category',
 'a1003f': 'category',
 'a1003g': 'category',
 'a1003h': 'category',
 'a1003i': 'category',
 'a1003j': 'category',
 'a1004a': 'category',
 'a1004b': 'category',
 'a1004c': 'category',
 'a1004d': 'category',
 'a1004f': 'category',
 'a1004g': 'category',
 'a1004h': 'category',
 'a1004i': 'category',
 'a1004j': 'category',
 'a1005a': 'category',
 'a1005b': 'category',
 'a1005c': 'category',
 'a1005d': 'category',
 'a1005f': 'category',
 'a1005g': 'category',
 'a1005h': 'category',
 'a1005i': 'category',
 'a1006a': 'category',
 'a1006b': 'category',
 'a1006c': 'category',
 'a1006d': 'category',
 'a1006f': 'category',
 'a1006g': 'category',
 'a1006h': 'category',
 'a1006i': 'category',
 'a1006j': 'category',
 'a1007a': 'category',
 'a1007ae': 'category',
 'a1007b': 'category',
 'a1007be': 'category',
 'a1007c': 'category',
 'a1007ce': 'category',
 'a1007d': 'category',
 'a1007de': 'category',
 'a1007f': 'category',
 'a1007fe': 'category',
 'a1007g': 'category',
 'a1007ge': 'category',
 'a1007h': 'category',
 'a1007he': 'category',
 'a1007i': 'category',
 'a1007ie': 'category',
 'a1007j': 'category',
 'a1007je': 'category',
 'a1101': 'category',
 'a1102': 'category',
 'a1103': 'category',
 'a1104': 'category',
 'a1105': 'category',
 'a1105e': 'category',
 'a1107': 'category',
 'a1107e': 'category',
 'a1108': 'category',
 'a1108e': 'category',
 'a1109': 'category',
 'a1109e': 'category',
 'a1201': 'category',
 'A1202A': 'category',
 'A1202B': 'category',
 'A1202C': 'category',
 'A1202D': 'category',
 'a1202e': 'category',
 'A1202E1': 'category',
 'A1202F': 'category',
 'A1202G': 'category',
 'A1202H': 'category',
 'A1202I': 'category',
 'A1202J': 'category',
 'A1202K': 'category',
 'a1203e': 'category',
 'a1204': 'category',
 'a1204e': 'category',
 'a1206': 'category',
 'a1206e': 'category',
 'a1207': 'category',
 'a1207e': 'category',
 'a1208': 'category',
 'a1208e': 'category',
 'a1209': 'category',
 'a1210': 'category',
 'a1211': 'category',
 'a1212': 'category',
 'a1213': 'category',
 'a1214': 'category',
 'a1301': 'category',
 'a1302': 'float64',
 'a1303': 'float64',
 'a1304': 'float64',
 'a1305': 'category',
 'a1306p': 'float64',
 'a1306t': 'float64',
 'a1307': 'category',
 'a1308': 'float64',
 'a1309': 'float64',
 'a1310': 'float64',
 'a1311': 'float64',
 'a1312': 'float64',
 'a1401': 'category',
 'a1402': 'category',
 'a1403a': 'category',
 'a1403b': 'category',
 'a1404a': 'category',
 'a1404b': 'category',
 'a1405': 'category',
 'a1406': 'category',
 'a1407': 'category',
 'a1408': 'category',
 'asexo': 'category',
 'completa': 'category',
 'desc_ent': 'category',
 'desc_mun': 'category',
 'entidad': 'category',
 'est_sel': 'category',
 'estrato': 'category',
 'municipio': 'category',
 'o_vac1': 'category',
 'o_vac11': 'category',
 'o_vac12': 'category',
 'o_vac13': 'category',
 'o_vac2': 'category',
 'o_vac3': 'category',
 'otroent': 'category',
 'ponde_f': 'category',
 'region': 'category',
 'resultado_1': 'category',
 'resultado_2': 'category',
 'resultado_3': 'category',
 'resultado_4': 'category',
 'sexo': 'category'
}
DataHe21_sub = DataHe21_sub.astype(convert_dict)
DataHe22_sub.a0819k = DataHe22_sub.a0819k.str.replace(',', '.')
DataHe22_sub = DataHe22_sub.astype(convert_dict)


#DataHe22_sub['a09091bd'] = pd.to_datetime(DataHe22_sub['a09091bd'], format='%Y%m%d') 


#merge
result_21 = DataHe21_sub.merge(DataR21_sub, on='FOLIO_I', how='left')
result_22 = DataHe22_sub.merge(DataR22_sub, on='FOLIO_I', how='left')

result_21 = result_21.merge(DataH21_sub, on='FOLIO_I', how='left')
result_22 = result_22.merge(DataH22_sub, on='FOLIO_I', how='left')

#creation of the dolor column using question h0402
frames = [result_21, result_22]
Data = pd.concat(frames,keys=["2021", "2022"])
Data['Dolor'] = 0
Data.loc[Data.h0402=='44','Dolor'] = 1
Data['Dolor']=Data['Dolor'].astype('category')
#defragmentation of data
Data = Data.copy()

nan_counts = Data.isna().sum()
# Set a limit for the number of NaN values allowed per column
nan_limit = len(Data)/2 #in statistics it should be 10%
# Drop columns where the number of NaN values exceeds the limit
#before the filtere we have 648
columns_to_drop = nan_counts[nan_counts > nan_limit].index
Data_sub = Data.copy()
Data_sub.drop(columns=columns_to_drop, inplace=True)
#after we only have 187

file_name = 'Data_sub'
file_save = out_path_files / (file_name + ".csv")
Data_sub.to_csv(file_save)

# Filter and select only the numeric columns
numeric_columns = Data_sub.select_dtypes(include=['number'])
# Group the DataFrame by 'Category' and calculate statistics for numeric columns
grouped = numeric_columns.groupby(Data_sub['Dolor'])
summary_numeric = grouped.agg(['mean', 'std', lambda x: x.mode().iloc[0]])
# Iterate over the first level of the multi-index and combine 'sum' and 'mean' for each index
for index_name in summary_numeric.columns.levels[0]:
    summary_numeric[f'{index_name}_Value'] = summary_numeric[index_name]['mean'].apply(lambda x: f'{x:.2f}').astype(str) + '(' + summary_numeric[index_name]['std'].apply(lambda x: f'{x:.2f}').astype(str) + ')'
    summary_numeric.drop([(index_name, 'mean'), (index_name, 'std'), (index_name,'<lambda_0>')], axis=1, inplace=True)
# Reset the index to make 'Category' a regular column
summary_numeric = summary_numeric.reset_index()
summary_numeric = summary_numeric.droplevel(level=1, axis=1)

# Group the DataFrame by 'Category' and calculate statistics for categorical columns
categorical_columns = Data_sub.select_dtypes(include=['category']).columns.tolist()
# Create an empty DataFrame to store the frequency counts
summary_categorical = pd.DataFrame(columns=['Dolor'])
# Loop through each categorical column and calculate frequencies
for col in categorical_columns:
    grouped_categorical = Data_sub[col].groupby(Data_sub['Dolor'])
    col_summary = grouped_categorical.value_counts().unstack(fill_value=0)
    col_summary.columns = [f'{col}_Frequency_{c}' for c in col_summary.columns]
    col_summary.reset_index(inplace=True)
    summary_categorical = pd.merge(summary_categorical, col_summary, on='Dolor', how='outer')

# Merge the summary dataframes on 'Category'
summary = pd.merge(summary_numeric, summary_categorical, on='Dolor')
file_name = 'summary'
file_save = out_path_files / (file_name + ".csv")
summary.T.to_csv(file_save)


Data_test = Data_sub.copy()
Data_test.drop(['FOLIO_I'], axis=1, inplace=True)
Data_test.drop(['FOLIO_INT_x'], axis=1, inplace=True)
Data_test.drop(['desc_ent_x'], axis=1, inplace=True)
Data_test.drop(['desc_mun_x'], axis=1, inplace=True)
Data_test.drop(['ponde_f_x'], axis=1, inplace=True)
Data_test.drop(['FOLIO_INT_y'], axis=1, inplace=True)
Data_test.drop(['desc_ent1'], axis=1, inplace=True)
Data_test.drop(['desc_mun1'], axis=1, inplace=True)
Data_test.drop(['ponde_f_y'], axis=1, inplace=True)
Data_test.drop(['upm_x'], axis=1, inplace=True)
Data_test.drop(['upm_y'], axis=1, inplace=True)
Data_test.drop(['desc_ent_y'], axis=1, inplace=True)
Data_test.drop(['desc_mun_y'], axis=1, inplace=True)
Data_test.drop(['resultado_1'], axis=1, inplace=True)
Data_test.drop(['resultado_2'], axis=1, inplace=True)
Data_test.drop(['resultado_3'], axis=1, inplace=True)
Data_test.drop(['resultado_4'], axis=1, inplace=True)


array=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,68,70,71,72,73,74,75,76,77,79,80,81,82,83,84,85,86,87,88,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,160,161,162,163,164,165,166,167,168,169]
Data_test = Data_test.iloc[:,array]
Data_test.drop(Data_test.columns[80], axis=1, inplace=True)

stats_p = populationtest(Data_test, 'Dolor', Data_test['Dolor'].unique().tolist(), out_path_files, 'Dolor')
#or_test(data_I, 'TipoPoblacion',np.r_[5:10,18,19:27],out_path_files, 'OR')



Data_sample_np = Data.loc[Data.Dolor==0,:]
Data_sample_p = Data.loc[Data.Dolor==1,:]
Data_sample_np = Data_sample_np.sample(len(Data_sample_p)*3)
frames = [Data_sample_p, Data_sample_np]
Data_sample = pd.concat(frames)

Data_sample.drop(columns=columns_to_drop, inplace=True)
#after we only have 187

file_name = 'Data_sample'
file_save = out_path_files / (file_name + ".csv")
Data_sample.to_csv(file_save)

# Filter and select only the numeric columns
numeric_columns = Data_sample.select_dtypes(include=['number'])
# Group the DataFrame by 'Category' and calculate statistics for numeric columns
grouped = numeric_columns.groupby(Data_sample['Dolor'])
summary_numeric = grouped.agg(['mean', 'std', lambda x: x.mode().iloc[0]])
# Iterate over the first level of the multi-index and combine 'sum' and 'mean' for each index
for index_name in summary_numeric.columns.levels[0]:
    summary_numeric[f'{index_name}_Value'] = summary_numeric[index_name]['mean'].apply(lambda x: f'{x:.2f}').astype(str) + '(' + summary_numeric[index_name]['std'].apply(lambda x: f'{x:.2f}').astype(str) + ')'
    summary_numeric.drop([(index_name, 'mean'), (index_name, 'std'), (index_name,'<lambda_0>')], axis=1, inplace=True)
# Reset the index to make 'Category' a regular column
summary_numeric = summary_numeric.reset_index()
summary_numeric = summary_numeric.droplevel(level=1, axis=1)

# Group the DataFrame by 'Category' and calculate statistics for categorical columns
categorical_columns = Data_sample.select_dtypes(include=['category']).columns.tolist()
# Create an empty DataFrame to store the frequency counts
summary_categorical = pd.DataFrame(columns=['Dolor'])
# Loop through each categorical column and calculate frequencies
for col in categorical_columns:
    grouped_categorical = Data_sample[col].groupby(Data_sample['Dolor'])
    col_summary = grouped_categorical.value_counts().unstack(fill_value=0)
    col_summary.columns = [f'{col}_Frequency_{c}' for c in col_summary.columns]
    col_summary.reset_index(inplace=True)
    summary_categorical = pd.merge(summary_categorical, col_summary, on='Dolor', how='outer')

# Merge the summary dataframes on 'Category'
summary = pd.merge(summary_numeric, summary_categorical, on='Dolor')
file_name = 'summary_Data_sample'
file_save = out_path_files / (file_name + ".csv")
summary.T.to_csv(file_save)


Data_test = Data_sample.copy()
Data_test.drop(['FOLIO_I'], axis=1, inplace=True)
Data_test.drop(['FOLIO_INT_x'], axis=1, inplace=True)
Data_test.drop(['desc_ent_x'], axis=1, inplace=True)
Data_test.drop(['desc_mun_x'], axis=1, inplace=True)
Data_test.drop(['ponde_f_x'], axis=1, inplace=True)
Data_test.drop(['FOLIO_INT_y'], axis=1, inplace=True)
Data_test.drop(['desc_ent1'], axis=1, inplace=True)
Data_test.drop(['desc_mun1'], axis=1, inplace=True)
Data_test.drop(['ponde_f_y'], axis=1, inplace=True)
Data_test.drop(['upm_x'], axis=1, inplace=True)
Data_test.drop(['upm_y'], axis=1, inplace=True)
Data_test.drop(['desc_ent_y'], axis=1, inplace=True)
Data_test.drop(['desc_mun_y'], axis=1, inplace=True)
Data_test.drop(['resultado_1'], axis=1, inplace=True)
Data_test.drop(['resultado_2'], axis=1, inplace=True)
Data_test.drop(['resultado_3'], axis=1, inplace=True)
Data_test.drop(['resultado_4'], axis=1, inplace=True)


array=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,68,70,71,72,73,74,75,76,77,79,80,81,82,83,84,85,86,87,88,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,160,161,162,163,164,165,166,167,168,169]
Data_test = Data_test.iloc[:,array]
#for all the individuals in the sample
Data_test.drop(Data_test.columns[80], axis=1, inplace=True)

Data_test.drop('h0304d',axis=1, inplace=True)
Data_test.drop('h0304m',axis=1, inplace=True)
Data_test.drop('h0304a',axis=1, inplace=True)
Data_test.drop('meses',axis=1, inplace=True)

stats_p = populationtest(Data_test, 'Dolor', Data_test['Dolor'].unique().tolist(), out_path_files, 'Dolor_sample')
#or_test(data_I, 'TipoPoblacion',np.r_[5:10,18,19:27],out_path_files, 'OR')


df_reset = Data_test.reset_index()
df_reset = df_reset.drop('level_1', axis=1)
filtered_df = df_reset[df_reset['Dolor'] == 1]
filtered_df = filtered_df.rename(columns={'level_0': 'Ano'})
#filtered is only for people with pain
stats_p = populationtest(filtered_df, 'Ano', filtered_df['Ano'].unique().tolist(), out_path_files, 'Dolor_sample_year')
