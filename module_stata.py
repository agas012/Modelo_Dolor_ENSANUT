from ast import Lambda
import numpy as np
import pandas as pd
import math
import scipy.stats as ss
from sklearn.model_selection import train_test_split
from statsmodels.formula.api import logit
from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype

def results_summary_to_dataframe(results):
    '''take the result of an statsmodel results table and transforms it into a dataframe'''
    pvals = results.pvalues
    coeff = results.params
    odds = np.exp(results.params)
    conf_lower = np.exp(results.conf_int(0.05)[0])
    conf_higher = np.exp(results.conf_int(0.05)[1])

    results_df = pd.DataFrame({"ODDs":odds,
                               "pvals":pvals,
                               "coeff":coeff,
                               "0.05":conf_lower,
                               "0.95":conf_higher
                                })
    #Reordering...
    results_df = results_df[["ODDs","coeff","pvals","0.05","0.95"]]
    return results_df

def is_categorical(array_like):
    """
    Test if the array is categorical.

    Parameters
    ----------
    array_like : pandas.arrays
        Input array to be tested
    """
    return array_like.dtype.name == 'category'

#data_in = data_I.copy()
#colgrouped = 'Outcome'
#valueslist = data_I['Outcome'].unique().tolist()
#outpath = outpath
#filename = 'diabetesTHOS'

def populationtest(data_in, colgrouped, valueslist, outpath, filename):
    """
    Test of indepence between populations. 

    Parameters
    __________
    data_in : Dataframe
        Input dataframe with the data to be tested
    colgrouped : pandas.column
        column
    collist : list of str
        list of columns to be tested
    """
    #list of significance
    data_sig = pd.DataFrame(data = {'Name': data_in.columns, 'statistic': np.zeros(data_in.shape[1]), 'p': np.zeros(data_in.shape[1])})

    #check of type of variabel per column check for categorical
    data_in.loc[:, data_in.dtypes == 'object'] =\
        data_in.select_dtypes(['object']).apply(lambda x: x.astype('category'))
    data_in.loc[:, data_in.isin([0,1]).all()] = data_in.loc[:, data_in.isin([0,1]).all()].apply(lambda x: x.astype('category'))

    #columns test
    colnames = data_in.columns
    colnames = np.delete(colnames, [np.r_[colnames.get_loc(colgrouped)]], 0)

    valueslistconst = valueslist.copy()
    valueslistconst.extend(['Totales', 'p'])
    CQ = pd.DataFrame(columns = valueslistconst)
    temp_totales = data_in[colgrouped].value_counts()
    CQ.loc['Totales', 'Totales'] = 0
    for coltitle in valueslist:
        CQ.loc['Totales', coltitle] = temp_totales[coltitle]
        CQ.loc['Totales', 'Totales'] = CQ.loc['Totales', 'Totales'] + temp_totales[coltitle]
    for coltitle in valueslist:
        d={'per' : [(CQ.loc['Totales', coltitle]/CQ.loc['Totales', 'Totales'])*100.00]}
        valn = pd.DataFrame(d)
        valn = valn.applymap(lambda x: "({:.2f})".format(x))
        CQ.loc['Totales', coltitle] = CQ.loc['Totales', coltitle].astype(str)
        strval = CQ.loc['Totales', coltitle] + valn
        CQ.loc['Totales', coltitle] = strval.iloc[0,0]
    coltitle ='Totales'
    d = {'per': [(CQ.loc['Totales',coltitle]/CQ.loc['Totales','Totales'])*100.00]}
    valn = pd.DataFrame(d)
    valn = valn.applymap(lambda x: " ({:.2f})".format(x))
    CQ.loc['Totales',coltitle] = CQ.loc['Totales',coltitle].astype(str)
    strval = CQ.loc['Totales',coltitle] + valn
    CQ.loc['Totales',coltitle] = strval.iloc[0,0]

    for cols in colnames:
        if(not is_numeric_dtype(data_in[cols])):
            ctableT = pd.crosstab(pd.to_numeric(data_in[cols]),data_in[colgrouped],margins=True)
            ctableT = ctableT.drop('All')
            if(ctableT.shape[0]>1):
                ctablen = pd.crosstab(pd.to_numeric(data_in[cols]),data_in[colgrouped], normalize='columns',margins=True)*100.00
                ctablen = ctablen.applymap(lambda x: " ({:.2f})".format(x))
                stat, pvalue, dof, expected = ss.chi2_contingency(ctableT.loc[:,valueslist])
                ctableT = ctableT.astype(str)
                ctableT = ctableT + ctablen
                ctableT.rename(columns={'All':'Totales'}, inplace = True)
                data_sig.loc[data_sig.Name==cols,'p'] = pvalue
                data_sig.loc[data_sig.Name==cols,'statistic'] = stat
                if((ctableT.index == 0).any()):
                    ctableT = ctableT.drop(0)
                    ctableT.rename({1:cols}, inplace = True) 
                # if(pvalue < 0.001):
                #     ctableT.loc[ctableT.index[0], 'p'] = '<0.001'
                # elif(pvalue < 0.01):
                #     ctableT.loc[ctableT.index[0], 'p'] = '<0.01'
                # else:
                ctableT.loc[ctableT.index[0], 'p'] = "{:.6f}".format(pvalue) 
                ctableT = ctableT.dropna()
            else:
                ctableT.rename(columns={'All':'Totales'}, inplace = True) 
                ctableT.rename(index={ ctableT.index[0]: cols }, inplace = True)
                data_sig.loc[data_sig.Name==cols,'p'] = math.nan
                data_sig.loc[data_sig.Name==cols,'statistic'] = math.nan
                for col in ctableT.columns:
                    ctableT[col].values[:] = 0
                ctableT.loc[ctableT.index[0], 'p'] = 'NaN'
        else:
            x=[]
            dataset_numeric = pd.concat([data_in[cols], data_in[colgrouped]], axis=1)
            for coltitle in valueslist:
                x.append(dataset_numeric.loc[dataset_numeric[colgrouped] == coltitle,cols])
            correlation, pvalue = ss.kruskal(*x)
            ctableT = dataset_numeric.groupby(colgrouped).mean().T
            ctableT.columns = ctableT.columns.tolist()
            ctableT['Totales'] = dataset_numeric[cols].mean()
            ctableT = ctableT.applymap(lambda x: "{:.2f}".format(x))
            ctabled = dataset_numeric.groupby(colgrouped).std().T
            ctabled.columns = ctabled.columns.tolist()
            ctabled['Totales'] = dataset_numeric[cols].std()
            ctabled = ctabled.applymap(lambda x: " ({:.2f})".format(x))
            ctableT = ctableT + ctabled
            data_sig.loc[data_sig.Name==cols,'p'] = pvalue
            data_sig.loc[data_sig.Name==cols,'statistic'] = correlation
            # if(pvalue < 0.001):
            #     ctableT.loc[ctableT.index[0], 'p'] = '<0.001'
            # elif(pvalue < 0.01):
            #     ctableT.loc[ctableT.index[0], 'p'] = '<0.01'
            # else:
            ctableT.loc[ctableT.index[0], 'p'] = "{:.6f}".format(pvalue)
        CQ  =  pd.concat([CQ, ctableT])
    CQ = CQ.replace(np.nan,'',regex = True)
    if(outpath.is_dir()):
        file_save = outpath / (filename + ".xlsx")
        CQ.to_excel(file_save) 
    else:
        outpath.mkdir(parents=True, exist_ok=True)
        file_save = outpath / (filename + ".xlsx")
        CQ.to_excel(file_save)  
    return data_sig

def ortest(data_in, ColGrouped, list_independent, out_path_files, file_name):
    """
    Test for odds ratio using a logistical regression for binary dependent variable.
   
    Parameters
    ----------
    data_in : DataFrame
        Input Dataframe with the data to be tested
    ColGrouped : pandas.Column
        Column with the dependent data
    list_independent : list of int
        List of the different independent values to be used in the regression
    out_path_files : str
        Output directory
    file_name : file_name
        Output file name
    """
    #check if dependent variable is binary
    dataset_dependent = data_in.loc[:,ColGrouped]
    if(dataset_dependent.isin([0,1]).all()):
        #check the type of variable per column
        data_in.loc[:, data_in.dtypes == 'object'] =\
                data_in.select_dtypes(['object'])\
                .apply(lambda x: x.astype('category'))
        data_in.loc[:, data_in.isin([0,1]).all()] = data_in.loc[:, data_in.isin([0,1]).all()].apply(lambda x: x.astype('category'))
        #select the column for the OR model
        ColNames = data_in.columns
        ColNames = np.delete(ColNames, [np.r_[ColNames.get_loc(ColGrouped)]], 0)
        #ColNames = np.delete(ColNames, [list_independent], 0)
        #OR
        dataset_results_final = pd.DataFrame()
        dataset_independent= data_in.loc[:,ColNames]
        dataset_dependent = dataset_dependent.astype("int")
        dataset_model = pd.concat([dataset_dependent, dataset_independent], axis=1)
        train_data, test_data = train_test_split(dataset_model, test_size=0.20, random_state= 42)
        #generate string model
        ColNamesstr = np.delete(ColNames, [np.r_[0]], 0)
        formula_str = ColGrouped + ' ~ ' + ColNames[0]
        for cols in ColNamesstr:
            formula_str = formula_str + ' + ' + cols
        model = logit(formula = formula_str, data = train_data).fit()
        dataset_results = results_summary_to_dataframe(model)
        dataset_results_final['OR (95% CI two-sided)'] = dataset_results['ODDs'].apply('{:.2f}'.format).astype(str) + ' (' + dataset_results['0.05'].apply('{:.2f}'.format).astype(str) + ' - ' + dataset_results['0.95'].apply('{:.2f}'.format).astype(str) +  ' )'
        dataset_results['ps'] = ''
        dataset_results.loc[dataset_results['pvals']< 0.05,'ps'] = '< 0.05' 
        dataset_results.loc[dataset_results['pvals']>= 0.05,'ps'] = dataset_results.loc[dataset_results['pvals']>= 0.05,'pvals'].apply('{:.3f}'.format).astype(str)
        dataset_results_final['p'] = dataset_results['ps']
        if(out_path_files.is_dir()):
            file_save = out_path_files / (file_name + ".xlsx")
            dataset_results_final.to_excel(file_save) 
        else:
            out_path_files.mkdir(parents=True, exist_ok=True)
            file_save = out_path_files / (file_name + ".xlsx")
            dataset_results_final.to_excel(file_save) 
    else:
        if(pd.get_dummies(dataset_dependent).shape[1]==2):
            dataset_dependent = pd.get_dummies(dataset_dependent).iloc[:,0]
            #check the type of variable per column
            data_in.loc[:, data_in.dtypes == 'object'] =\
                    data_in.select_dtypes(['object'])\
                    .apply(lambda x: x.astype('   '))
            data_in.loc[:, data_in.isin([0,1]).all()] = data_in.loc[:, data_in.isin([0,1]).all()].apply(lambda x: x.astype('category'))
            #select the column for the OR model
            ColNames = data_in.columns
            ColNames = np.delete(ColNames, [np.r_[ColNames.get_loc(ColGrouped)]], 0)
            #ColNames = np.delete(ColNames, [list_independent], 0)
            ColGrouped = dataset_dependent.name
            #OR
            dataset_results_final = pd.DataFrame()
            dataset_independent= data_in.loc[:,ColNames]
            dataset_dependent = dataset_dependent.astype("int")
            dataset_model = pd.concat([dataset_dependent, dataset_independent], axis=1)
            train_data, test_data = train_test_split(dataset_model, test_size=0.20, random_state= 42)
            #generate string model
            ColNamesstr = np.delete(ColNames, [np.r_[0]], 0)
            formula_str = ColGrouped + ' ~ ' + ColNames[0]
            for cols in ColNamesstr:
                formula_str = formula_str + ' + ' + cols
            try:
                model = logit(formula = formula_str, data = train_data).fit()
            except:
                print("An exception occurred")
                return
            dataset_results = results_summary_to_dataframe(model)
            dataset_results_final['OR (95% CI two-sided)'] = dataset_results['ODDs'].apply('{:.2f}'.format).astype(str) + ' (' + dataset_results['0.05'].apply('{:.2f}'.format).astype(str) + ' - ' + dataset_results['0.95'].apply('{:.2f}'.format).astype(str) +  ' )'
            dataset_results['ps'] = ''
            dataset_results.loc[dataset_results['pvals']< 0.05,'ps'] = '< 0.05' 
            dataset_results.loc[dataset_results['pvals']>= 0.05,'ps'] = dataset_results.loc[dataset_results['pvals']>= 0.05,'pvals'].apply('{:.3f}'.format).astype(str)
            dataset_results_final['p'] = dataset_results['ps']
            if(out_path_files.is_dir()):
                file_save = out_path_files / (file_name + ".xlsx")
                dataset_results_final.to_excel(file_save) 
            else:
                out_path_files.mkdir(parents=True, exist_ok=True)
                file_save = out_path_files / (file_name + ".xlsx")
                dataset_results_final.to_excel(file_save) 
