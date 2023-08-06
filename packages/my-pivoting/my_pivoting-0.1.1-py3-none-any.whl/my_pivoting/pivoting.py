from functools import reduce

import pandas as pd


def unpivot(
    df:str,
    ids:str,
    cols:dict
):
    '''
    unpivot from wide to long

    groups={
    'share':["Q1'22", "Q2'22"],
    'base':["Base_Q1'22", "Base_Q2'22"]
    }
    
    ids = ['Name', 'Operator', 'Reason','Category', 'Region', 'num1', 'num2', 'Extra']
    '''

    dfs = []
    for key, value in cols.items():
        melted = pd.melt(
            df, 
            id_vars=ids,
            var_name='Quarter',
            value_name=key,
            value_vars=value
            )
        dfs.append(melted)
    
    final_df = reduce(lambda  left,right: pd.merge(left, right, on=ids,
                                            how='outer'), dfs)
    return final_df
