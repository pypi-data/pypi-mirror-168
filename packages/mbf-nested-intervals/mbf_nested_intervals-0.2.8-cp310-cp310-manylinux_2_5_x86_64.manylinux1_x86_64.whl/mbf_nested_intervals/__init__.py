from .mbf_nested_intervals import *  # noqa:F401
from mbf_nested_intervals import IntervalSet
import pandas as pd
import itertools

__version__ = '0.2.8'


def _df_to_tup(df):
    joined = []
    for ii, (chr, start, stop, strand) in enumerate(
        zip(df["chr"], df["start"], df["stop"], df["strand"])
    ):
        joined.append(((chr, strand), start, stop, ii))
    joined.sort(key=lambda tup: tup[0])
    return joined


def _df_to_tup_no_strand(df):
    joined = []
    for ii, (chr, start, stop) in enumerate(zip(df["chr"], df["start"], df["stop"])):
        joined.append((chr, start, stop, ii))
    joined.sort(key=lambda tup: tup[0])
    return joined


def merge_df_intervals(df, iv_func=lambda iv: iv.merge_hull()):
    """take a DataFrame {chr, start, end, *} and merge overlapping intervals.
    * is from the last entry.


    """
    if not "strand" in df.columns:
        df = df.assign(strand=1)
        strand_added = True
    else:
        strand_added = False
    joined = _df_to_tup(df)

    out = []
    for chr_strand, sub_group in itertools.groupby(joined, lambda tup: tup[0]):
        args = [x[1:] for x in sub_group]
        iv = IntervalSet.from_tuples_with_id(args)
        new_order = iv_func(iv).to_tuples_last_id()
        new_df = df.iloc[[x[2] for x in new_order]].copy()
        new_df.loc[:, "start"] = [x[0] for x in new_order]
        new_df.loc[:, "stop"] = [x[1] for x in new_order]
        out.append(new_df)
    res = pd.concat(out)
    if strand_added:
        res = res.drop("strand", axis=1)
    return res.sort_values(["chr", "start"])


def merge_df_intervals_with_callback(df, callback):
    """take a {chr, start, end, *} dataframe and merge overlapping intervals, calling callback for group larger than one.."""
    if not "strand" in df:
        df = df.assign(strand=1)
        strand_added = True
    else:
        strand_added = False
    joined = _df_to_tup(df)
    result = []
    for chr, sub_group in itertools.groupby(joined, lambda tup: tup[0]):
        args = [x[1:] for x in sub_group]
        iv = IntervalSet.from_tuples_with_id(args)
        subsets = iv.merge_hull().to_tuples_with_id()
        for s in subsets:
            sub_df = df.iloc[list(s[2])].copy()
            sub_df.at[:, "start"] = s[0]
            sub_df.at[:, "stop"] = s[1]
            row_data = callback(sub_df)
            if not isinstance(
                row_data, dict
            ):  # and not (isinstance(row_data, pd.core.series.Series) and len(row_data.shape) == 1):
                print("type", type(row_data))
                # print 'len(shape)', len(row_data.shape)
                print(callback)
                raise ValueError(
                    "Merge_function returned something other than dict (writing to the pandas series directly is very slow, call to_dict() on it, then modify it.)"
                )
            if set(row_data.keys()) != set(df.columns):
                raise ValueError(
                    "Merge_function return wrong columns. Expected %s, was %s"
                    % (df.columns, list(row_data.keys()))
                )
            row_data["start"] = s[0]
            row_data["stop"] = s[1]

            result.append(row_data)
    res = pd.DataFrame(result).sort_values(["chr", "start"])
    if strand_added:
        res = res.drop("strand", axis=1)
    return res
