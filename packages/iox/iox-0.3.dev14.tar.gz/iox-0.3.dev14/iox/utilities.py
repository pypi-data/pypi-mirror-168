
import numpy as np
import pandas as pd
from sparse import COO


def bucket(a, width, right=True):
    """

    Parameters
    ----------
    a : array-like
    width : float
    right : bool

    Returns
    -------
    numpy.ndarray
    """

    # Define bins
    a_min = np.min(np.floor(a)) - 2. * width  # really we only need 1 * width TODO test this out
    a_max = np.max(np.ceil(a)) + 2. * width
    bins = np.arange(a_min, a_max, width)

    # Perform cut
    return bins[pd.cut(a, bins=bins, right=right, labels=False, include_lowest=True)]


def numpy_aggregate(a, axes, index_names=None, value_name='value', aggfunc='mean', as_frame=True):
    """
    Aggregate numpy array with an arbitrary number of axes.

    Parameters
    ----------
    a : numpy.ndarray
    axes : list-like
        New axis values for axes of `a`. Must be one for each axis. If set to None, axis will be ignored.
    index_names : list-like
        Axes names.
    value_name : str
        Value column name.
    aggfunc : str
        How to pivot the data. Follows the pandas convention.
    as_frame : bool

    Returns
    -------
    pandas.DataFrame or numpy.ndarray
    """

    # Make sure `a` is a numpy array
    if not isinstance(a, np.ndarray):
        raise AttributeError('`a` must be a numpy array')

    # Set index_names
    if index_names is None:
        index_names = [f'axis{i}' for i in range(len(axes))]

    # Make sure index_names and axes are same length
    if len(axes) != len(index_names):
        raise AttributeError('`axes` and `index_names` must be same length')

    # Is `a` boolean?
    # This eliminates the benefit of COO. COO here just exists to collect the data. Maybe there's a better solution.
    is_boolean = False
    if a.dtype == 'bool':
        is_boolean = True
        a = a + 1  # To make this not a boolean. COO below might remove some indices otherwise.

    # Get sparse representation of `a`
    a_sparse = COO(a)

    # Update axis IDs if necessary
    for i, axis in enumerate(axes):
        if axis is not None:
            a_sparse.coords[i] = pd.Series(dict(zip(range(a.shape[i]), axis)))[a_sparse.coords[i]].to_numpy()

    # Create DataFrame
    data = dict(zip(index_names, a_sparse.coords))  # axes
    data.update({value_name: a_sparse.data})  # add value
    df = pd.DataFrame(data)

    # If `a` is boolean, change data back to boolean
    if is_boolean:
        df[value_name] = df[value_name] == 2  # because we added 1 to True before

    # Aggregate
    df_agg = df.pivot_table(index=index_names, values=value_name, aggfunc=aggfunc)

    # What to return?
    if as_frame:
        return df_agg
    else:
        return df_agg.to_numpy().reshape(*[len(np.unique(axis)) for axis in axes])  # noqa


# Unpack
def unpack(a):
    """
    Unpack a higher dimensional structure into a few variables. For instance, a dataframe with an index and a single
    column could be unpacked into the variable "x" for the index and "y" for the first column.

    Parameters
    ----------
    a : pd.DataFrame

    Returns
    -------
    np.ndarray
        Unpacked data
    """
    if isinstance(a, pd.DataFrame):
        return a.reset_index().T.to_numpy()
    else:
        raise AttributeError


def collapse_to_vector(df, index, where, columns=None):
    """
    Collapse a pandas DataFrame to an index and turn all columns into a vector of their values. This is something
    akin to a pivot table.

    Returns
    -------

    """

    df = (
        df
        .reset_index()  # reset the index in case we have a MultiIndex
        .set_index(index)  # set the index to what we expect it to be
    )

    if columns is None:
        columns = df.columns
    elif isinstance(columns, str):
        columns = [columns]

    df_filtered = df.query(where)

    # Construct result
    results = pd.DataFrame({index: np.unique(df.index.to_numpy())}).set_index(index)
    for column in columns:
        results[column] = df_filtered.groupby(index)[column].agg(lambda x: list(x.unique()))

    # Return
    return results


def wherein(a, b):
    return pd.Series(np.arange(len(b)), index=b)[a].to_numpy()


# Convenience zfill function
def zfill(a, width=None):
    if width is None:
        return a
    elif hasattr(a, '__getitem__'):
        return np.char.zfill(list(map(str, a)), width)
    else:
        return str(a).zfill(width)


# Convenience zfill range function
def zfillr(n, width=None):
    return zfill(range(n), width)


if __name__ == '__main__':
    a = np.random.rand(3, 6, 100)
    x = [0, 0, 1]
    y = [0, 1, 2, 0, 1, 2]
    ap = numpy_aggregate(a, axes=[x, y])

