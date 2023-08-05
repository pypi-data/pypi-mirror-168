import functools

import numpy as np
import pandas as pd
from bumbag.core import flatten


def efficiency(values, dropna=True):
    """Compute efficiency (or normalized Shannon entropy) for discrete values.

    Let :math:`|\\mathcal{X}| = \\kappa` be the cardinality of the support
    :math:`\\mathcal{X} \\subseteq \\Omega` of a discrete random variable
    :math:`X`. In other words, :math:`\\kappa` is the number of distinct
    values of :math:`\\mathcal{X}`. It can be shown that entropy :math:`H(X)`
    is bounded by :math:`0 \\leq H(X) \\leq \\log_{2} \\kappa`. Hence,
    efficiency is defined as

    .. math::

        \\eta(X) \\triangleq \\frac{H(X)}{\\log_{2} \\kappa}
        = - \\frac{1}{\\log_{2} \\kappa}
        \\sum_{x \\in \\mathcal{X}} p(x) \\log_{2} p(x) \\in [0, 1].

    Parameters
    ----------
    values : array-like
        An input array for which efficiency is to be computed.
        It must be 1-dimensional.
    dropna : bool, default=True
        Specify if null values should be excluded from the computation.
        When input array consists of only null values, function returns NaN if
        ``dropna=True`` and 0.0 if ``dropna=False``.

    Returns
    -------
    float
        Normalized Shannon entropy with log to the base 2.
        Returns NaN if input array is empty.

    Examples
    --------
    >>> efficiency([])
    nan

    >>> efficiency(["a", "a"])
    0.0

    >>> efficiency(["a", "b"])
    1.0

    >>> efficiency(["a", "b", "c", "d"])
    1.0
    """
    if len(values) == 0:
        return float("nan")

    counts = (
        pd.Series(values)
        .value_counts(normalize=False, sort=False, dropna=dropna)
        .values
    )

    if len(counts) == 0:
        return float("nan")

    if len(counts) == 1:
        return 0.0

    total = counts.sum()

    h = (
        np.log2(total)
        if len(counts) == total
        else np.log2(total) - (counts * np.log2(counts)).sum() / total
    )

    return float(h / np.log2(len(counts)))


def entropy(values, dropna=True):
    """Compute the Shannon entropy for discrete values.

    The Shannon entropy of a discrete random variable :math:`X` with support
    :math:`\\mathcal{X} \\subseteq \\Omega` and probability mass function
    :math:`p(x) = \\Pr(X = x) \\in (0, 1]` is

    .. math::

        H(X) \\triangleq \\mathbb{E}[ -\\log_{2} p(X) ]
        = - \\sum_{x \\in \\mathcal{X}} p(x) \\log_{2} p(x) \\in [0, \\infty).

    Parameters
    ----------
    values : array-like
        An input array for which entropy is to be computed.
        It must be 1-dimensional.
    dropna : bool, default=True
        Specify if null values should be excluded from the computation.
        When input array consists of only null values, function returns NaN if
        ``dropna=True`` and 0.0 if ``dropna=False``.

    Returns
    -------
    float
        Shannon entropy with log to the base 2.
        Returns NaN if input array is empty.

    References
    ----------
    .. [1] C. E. Shannon, "A Mathematical Theory of Communication,"
           in The Bell System Technical Journal, vol. 27, no. 3, pp. 379-423,
           July 1948, doi: 10.1002/j.1538-7305.1948.tb01338.x.

    Examples
    --------
    >>> entropy([])
    nan

    >>> entropy(["a", "a"])
    0.0

    >>> entropy(["a", "b"])
    1.0

    >>> entropy(["a", "b", "c", "d"])
    2.0
    """
    if len(values) == 0:
        return float("nan")

    counts = (
        pd.Series(values)
        .value_counts(normalize=False, sort=False, dropna=dropna)
        .values
    )

    if len(counts) == 0:
        return float("nan")

    if len(counts) == 1:
        return 0.0

    total = counts.sum()

    return float(
        np.log2(total)
        if len(counts) == total
        else np.log2(total) - (counts * np.log2(counts)).sum() / total
    )


def freq(values, dropna=True):
    """Compute value frequencies.

    Given an input array, calculate for each distinct value:
     - the frequency (``n``),
     - the cumulative frequency (``N``),
     - the relative frequency (``r``), and
     - the cumulative relative frequency (``R``).

    Parameters
    ----------
    values : array-like
        An input array of values to compute the frequencies of its members.
        It must be 1-dimensional.
    dropna : bool, default=True
        Specify if null values should be excluded from the computation.

    Returns
    -------
    pandas.DataFrame
        Frequencies of distinct values.

    Examples
    --------
    >>> x = ["a", "c", "b", "g", "h", "a", "g", "a"]
    >>> frequency = freq(x)
    >>> isinstance(frequency, pd.DataFrame)
    True
    >>> frequency
       n  N      r      R
    a  3  3  0.375  0.375
    g  2  5  0.250  0.625
    c  1  6  0.125  0.750
    b  1  7  0.125  0.875
    h  1  8  0.125  1.000
    """
    return pd.DataFrame(
        data=pd.Series(values).value_counts(
            sort=True,
            ascending=False,
            bins=None,
            dropna=dropna,
        ),
        columns=["n"],
    ).assign(
        N=lambda df: df["n"].cumsum(),
        r=lambda df: df["n"] / df["n"].sum(),
        R=lambda df: df["r"].cumsum(),
    )


def join_dataframes_by_index(*dataframes):
    """Join multiple data frames by their index.

    Parameters
    ----------
    dataframes : sequence of pandas.DataFrame and pandas.Series
        Data frames to join. Being a variadic function, it can handle in one
        call both cases when data frames are given individually and when they
        are given in a sequence. The function also accepts pandas series.
        If an object is of type pandas.Series, it is converted to a data frame.

    Returns
    -------
    pandas.DataFrame
        A new data frame with all columns.

    Examples
    --------
    >>> df1 = pd.DataFrame([[1, 2], [3, 4]], columns=["a", "b"])
    >>> df2 = pd.DataFrame([[5, 6], [7, 8]], columns=["c", "d"])
    >>> df = join_dataframes_by_index(df1, df2)
    >>> isinstance(df, pd.DataFrame)
    True
    >>> df
       a  b  c  d
    0  1  2  5  6
    1  3  4  7  8

    >>> df1 = pd.DataFrame([[1, 2], [3, 4]], index=[0, 1], columns=["a", "b"])
    >>> df2 = pd.DataFrame([[5, 6], [7, 8]], index=[0, 2], columns=["c", "d"])
    >>> df = join_dataframes_by_index([df1, df2])
    >>> isinstance(df, pd.DataFrame)
    True
    >>> df
         a    b    c    d
    0  1.0  2.0  5.0  6.0
    1  3.0  4.0  NaN  NaN
    2  NaN  NaN  7.0  8.0

    >>> df1 = pd.DataFrame([[1, 2], [3, 4]], columns=["a", "b"])
    >>> s1 = pd.Series([5, 6], name="c")
    >>> df = join_dataframes_by_index(df1, s1)
    >>> isinstance(df, pd.DataFrame)
    True
    >>> df
       a  b  c
    0  1  2  5
    1  3  4  6

    >>> s1 = pd.Series([1, 2])
    >>> s2 = pd.Series([3, 4])
    >>> s3 = pd.Series([5, 6])
    >>> df = join_dataframes_by_index([s1, s2], s3)
    >>> isinstance(df, pd.DataFrame)
    True
    >>> df
       0  0  0
    0  1  3  5
    1  2  4  6

    >>> s1 = pd.Series([1, 2], index=[0, 1], name="a")
    >>> s2 = pd.Series([3, 4], index=[1, 2], name="b")
    >>> s3 = pd.Series([5, 6], index=[2, 3], name="c")
    >>> df = join_dataframes_by_index(s1, s2, s3)
    >>> isinstance(df, pd.DataFrame)
    True
    >>> df
         a    b    c
    0  1.0  NaN  NaN
    1  2.0  3.0  NaN
    2  NaN  4.0  5.0
    3  NaN  NaN  6.0
    """
    return pd.concat(map(pd.DataFrame, flatten(dataframes)), axis=1)


def mode(values, dropna=True):
    """Compute the most frequent value.

    Parameters
    ----------
    values : array-like
        An input array for which mode is to be computed.
        It must be 1-dimensional.
    dropna : bool, default=True
        Specify if null values should be excluded from the computation.
        When input array consists of only null values, function returns NaN if
        ``dropna=True`` and mode of null values if ``dropna=False``.

    Returns
    -------
    tuple
        Mode and its frequency. Returns NaN if input array is empty.

    Examples
    --------
    >>> mode([])
    nan

    >>> mode([None, None])
    nan

    >>> mode([None, None], dropna=False)
    (None, 2)

    >>> mode([1, None, 1, 1, None, 2, None, None])
    (1.0, 3)

    >>> mode([1, None, 1, 1, None, 2, None, None], dropna=False)
    (nan, 4)
    """
    if len(values) == 0:
        return float("nan")

    counts = pd.Series(values).value_counts(dropna=dropna)

    if len(counts) == 0:
        return float("nan")

    return counts.index[0], counts.iloc[0]


def profile(dataframe, dropna=True):
    """Profile data frame by compute summary measures of its columns.

    Parameters
    ----------
    dataframe : pandas.DataFrame
        An input data frame to profile.
    dropna : bool, default=True
        Specify if null values should be excluded from the computation.

    Returns
    -------
    pandas.DataFrame
        A new data frame with column summary measures.
    """

    def compute_mode(values, drop_na, index):
        try:
            return mode(values, drop_na)[index]
        except (IndexError, TypeError):
            return float("nan")

    mode_value = functools.partial(compute_mode, drop_na=dropna, index=0)
    mode_freq = functools.partial(compute_mode, drop_na=dropna, index=1)
    eff = functools.partial(efficiency, dropna=dropna)

    return join_dataframes_by_index(
        dataframe.dtypes.apply(str).to_frame("type"),
        dataframe.count().to_frame("count"),
        dataframe.isnull().sum().to_frame("isnull"),
        dataframe.nunique().to_frame("unique"),
        dataframe.apply(mode_value).to_frame("top"),
        dataframe.apply(mode_freq).to_frame("freq"),
        dataframe.mean(numeric_only=True).to_frame("mean"),
        dataframe.std(numeric_only=True, ddof=1).to_frame("std"),
        dataframe.min(numeric_only=True).to_frame("min"),
        dataframe.quantile(0.05, numeric_only=True).to_frame("5%"),
        dataframe.quantile(0.25, numeric_only=True).to_frame("25%"),
        dataframe.quantile(0.50, numeric_only=True).to_frame("50%"),
        dataframe.quantile(0.75, numeric_only=True).to_frame("75%"),
        dataframe.quantile(0.95, numeric_only=True).to_frame("95%"),
        dataframe.max(numeric_only=True).to_frame("max"),
        dataframe.skew(numeric_only=True).to_frame("skewness"),
        dataframe.kurt(numeric_only=True).to_frame("kurtosis"),
        dataframe.apply(eff).to_frame("efficiency"),
    ).assign(
        pct_isnull=lambda df: df["isnull"] / dataframe.shape[0],
        pct_unique=lambda df: df["unique"] / dataframe.shape[0],
        pct_freq=lambda df: df["freq"] / dataframe.shape[0],
    )


def union_dataframes_by_name(*dataframes):
    """Union multiple data frames by their name.

    Parameters
    ----------
    dataframes : sequence of pandas.DataFrame and pandas.Series
        Data frames to union. Being a variadic function, it can handle in one
        call both cases when data frames are given individually and when they
        are given in a sequence. The function also accepts pandas series.
        If an object is of type pandas.Series, it is converted to a data frame.

    Returns
    -------
    pandas.DataFrame
        A new data frame with all rows.

    Notes
    -----
    - Inspired by the unionByName method of a Spark DataFrame.
    - Deduplication is not performed on the returned data frame.

    Examples
    --------
    >>> df1 = pd.DataFrame([[1, 2], [3, 4]])
    >>> df2 = pd.DataFrame([[5, 6], [7, 8]])
    >>> df = union_dataframes_by_name(df1, df2)
    >>> isinstance(df, pd.DataFrame)
    True
    >>> df
       0  1
    0  1  2
    1  3  4
    0  5  6
    1  7  8

    >>> df1 = pd.DataFrame([[1, 1], [1, 1]])
    >>> df2 = pd.DataFrame([[1, 1], [1, 1]])
    >>> df = union_dataframes_by_name(df1, df2)
    >>> isinstance(df, pd.DataFrame)
    True
    >>> df
       0  1
    0  1  1
    1  1  1
    0  1  1
    1  1  1

    >>> df1 = pd.DataFrame([[1, 2], [3, 4]], index=[0, 1])
    >>> df2 = pd.DataFrame([[5, 6], [7, 8]], index=[0, 2])
    >>> df = union_dataframes_by_name([df1, df2])
    >>> isinstance(df, pd.DataFrame)
    True
    >>> df
       0  1
    0  1  2
    1  3  4
    0  5  6
    2  7  8

    >>> df1 = pd.DataFrame([[1, 2], [3, 4]], index=[0, 1], columns=["a", "b"])
    >>> df2 = pd.DataFrame([[5, 6], [7, 8]], index=[0, 2], columns=["c", "d"])
    >>> df = union_dataframes_by_name([df1, df2])
    >>> isinstance(df, pd.DataFrame)
    True
    >>> df
         a    b    c    d
    0  1.0  2.0  NaN  NaN
    1  3.0  4.0  NaN  NaN
    0  NaN  NaN  5.0  6.0
    2  NaN  NaN  7.0  8.0

    >>> df1 = pd.DataFrame([[1, 2], [3, 4]])
    >>> s1 = pd.Series([5, 6])
    >>> df = union_dataframes_by_name(df1, s1)
    >>> isinstance(df, pd.DataFrame)
    True
    >>> df
       0    1
    0  1  2.0
    1  3  4.0
    0  5  NaN
    1  6  NaN

    >>> s1 = pd.Series([1, 2])
    >>> s2 = pd.Series([3, 4])
    >>> s3 = pd.Series([5, 6])
    >>> df = union_dataframes_by_name([s1, s2], s3)
    >>> isinstance(df, pd.DataFrame)
    True
    >>> df
       0
    0  1
    1  2
    0  3
    1  4
    0  5
    1  6

    >>> s1 = pd.Series([1, 2], index=[0, 1], name="a")
    >>> s2 = pd.Series([3, 4], index=[1, 2], name="b")
    >>> s3 = pd.Series([5, 6], index=[2, 3], name="c")
    >>> df = union_dataframes_by_name(s1, s2, s3)
    >>> isinstance(df, pd.DataFrame)
    True
    >>> df
         a    b    c
    0  1.0  NaN  NaN
    1  2.0  NaN  NaN
    1  NaN  3.0  NaN
    2  NaN  4.0  NaN
    2  NaN  NaN  5.0
    3  NaN  NaN  6.0
    """
    return pd.concat(map(pd.DataFrame, flatten(dataframes)), axis=0)
