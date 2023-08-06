import pandas as pd
from typing import List, Union


def groupby_choice(df: pd.DataFrame, by: Union[str, List], col_name: any, choice='max', inplace=True):
    """
    取分组后的某列最值,组成的新df. 默认inplace.

    Example::
     df = pd.DataFrame({'key' : ['A', 'A', 'B', 'B', 'C', 'C'],
                       'value' : ['v1', 'v2', 'v3', 'v4','v5', 'v6'],
                       'prob' : [1, 5, 50, 2, 5, 5]})
    >>> df
        key value  prob
    0   A    v1     1
    1   A    v2     5
    2   B    v3    50
    3   B    v4     2
    4   C    v5     5
    5   C    v6     5
    >>> groupby_choice(df, 'key', 'prob', 'max')
    >>>
        key value  prob
    1   A    v2     5
    2   B    v3    50
    4   C    v5     5
    """
    if not inplace:
        df = df.copy(deep=True)
    index_list = []
    for idx, item in df.groupby(by)[col_name]:
        if choice == "max":
            index_list.append(item.idxmax())
        elif choice == "min":
            index_list.append(item.idxmin())
        else:
            raise "Invalid `func` parameter."
    return df.iloc[index_list]


def group_df(df, col_name, interval=5, use_max_min_interval=False, closed='neither', dropna=True):
    """
    Parameters
    ----------
        col_name: 根据 `col_name` 进行分组
        interval: 合并采样间隔
        use_max_min_interval: True使用最大最小区间确定等距采样个数； False使用df的样本数目确定采样个数

    """
    if dropna:
        df = df.dropna(axis=0, how='any', inplace=False)
    df = df.sort_values(by=col_name, ascending=True)
    if use_max_min_interval:
        periods = (df[col_name].max() - df[col_name].min()) / interval
    else:
        periods = len(df) // interval

    bins = pd.interval_range(df[col_name].min(), df[col_name].max(),
                             periods=periods,
                             closed=closed)
    pd_cut = pd.cut(df[col_name], bins=bins)
    for idx, i in enumerate(df.groupby(pd_cut)):
        agg_res = i[1].agg('mean')
        if idx == 0:
            df_grouped = agg_res
        else:
            df_grouped = pd.concat([df_grouped, agg_res], axis=1)
    df_grouped = df_grouped.transpose()
    return df_grouped.dropna().reset_index(inplace=False).drop(['index'], axis=1)


def re_ord_df_col(df, col_name, ord_num=0):
    """Re-order df's column name."""
    tmp_list = df.columns.tolist()
    tmp_list.remove(col_name)
    tmp_list.insert(ord_num, col_name)
    df = df[tmp_list]
    return df
