"""
distance.py

language: python
version: 3.x
author: C. Lockhart <chris@lockhartlab.org>
"""

from molecular.analysis._analysis_utils import _distances, _minimum_distances

from iox import collapse_to_vector, numpy_aggregate
import numpy as np
import pandas as pd
from sparse import COO  # has numba dependency I'm not thrilled about


# These functions well better the smaller the number of atoms in a or b is. In the future, maybe wrap this so that
# only ~100 atoms considered at a time? Or ~1000? If we have 1M atoms, this could get onerous though.

def contacts(a, b, cutoff=4.5, aggregate_by=None, include_images=False, vectorize=False):
    """
    Compute atomic contacts.

    Parameters
    ----------
    a, b : Trajectory
    cutoff : float
    aggregate_by : str
        Aggregate atomic contacts to a different resolution, e.g., residue or segment.
    include_images : bool
        Include neighboring images in this calculation (Default: False).
    vectorize : bool

    Returns
    -------
    numpy.ndarray
    """

    # Actually compute the contacts
    results = distances(a, b, include_images=include_images) <= cutoff

    # Aggregate the contacts?
    if aggregate_by is not None:
        results = _format_results(results, a, b, value_name='contact', by=aggregate_by, aggfunc='max')

    # Vectorize?
    if vectorize:
        results = collapse_to_vector(results, index='structure_id', where='contact == True').drop(columns='contact')

    # Return
    return results


def contacts_to_vector(contacts, axis1=None, axis2=None):
    """
    Convert contacts array to contact vector. With `axis1` and `axis2`, `contacts` can be changed such that indices
    besides the atom IDs are used.

    Parameters
    ----------
    contacts : numpy.ndarray
    axis1 : list-like
        (Optional) New indices for axis 1 of `contacts`
    axis2 : list-like
        (Optional) New indices for axis 2 of `contacts`

    Returns
    -------
    numpy.ndarray
    """

    # Get sparse representation of contacts
    contacts_sparse = COO(contacts)

    # Update axis IDs if necessary
    def _update_id(i, x):
        contacts_sparse.coords[i] = \
            pd.Series(dict(zip(range(contacts.shape[i]), x)))[contacts_sparse.coords[i]].to_numpy()

    if axis1 is not None:
        _update_id(1, axis1)
    if axis2 is not None:
        _update_id(2, axis2)

    # Create DataFrame
    df = pd.DataFrame({
        'structure_id': contacts_sparse.coords[0],
        f'i': contacts_sparse.coords[1],
        f'j': contacts_sparse.coords[2],
    })

    # Aggregate to series
    sr = (
        df
        .drop_duplicates()
        .sort_values(['structure_id', 'j'])
        .groupby('structure_id')['j']
        .agg(list)
    )

    # Make a correction for missing structure IDs (if there were no contacts they'll be absent)
    is_empty = ~np.max(contacts, axis=(1, 2))
    if np.sum(is_empty) > 0:
        for i in np.argwhere(is_empty).ravel():
            sr.loc[i] = []

        sr.sort_index(inplace=True)

    # Return as numpy array
    return sr.to_numpy()


# Compute the distance between two Trajectories
# TODO should this always return a DataFrame?
def distances(a, b, aggregate_by=None, include_images=False):
    """
    Compute the distance between two Trajectory instances.

    Parameters
    ----------
    a, b : Trajectory
        Two trajectories. Must have same dimensions.
    aggregate_by : str
        Takes the minimum distance among a group: atom, residue, or segment.
    include_images : bool
        Consider all images in this computation. (Default: False)

    Returns
    -------
    numpy.ndarray or pandas.DataFrame
        Distance between every frame in the trajectory.
    """

    # Extract coordinates
    a_xyz = a.xyz.to_numpy().reshape(*a.shape)
    b_xyz = b.xyz.to_numpy().reshape(*b.shape)

    # If we're not going to consider images, we can run with just coordinates
    if not include_images:
        results = _distances(a_xyz, b_xyz)

    # Otherwise, we need to do some extra checks and extract the box
    else:
        # Make sure that `a` and `b` come from the same parent Trajectory
        if a.parent.designator != b.parent.designator:
            raise AttributeError('`a` and `b` must have same parent')

        # Extract boxes and check that `a_box` and `b_box` are identical
        a_box = a.box.to_numpy()
        b_box = b.box.to_numpy()
        if np.allclose(a_box, b_box) is not True:
            raise AttributeError('`a` and `b` have different dimensions')

        # Finally, we can compute the minimum distances
        results = _minimum_distances(a_xyz, b_xyz, a_box)

    # Aggregate?
    if aggregate_by is not None:
        results = _format_results(results, a, b, value_name='distance', by=aggregate_by, aggfunc='min')

    # Return
    return results


#
# # Compute the distance between two Trajectories
# def distance(a, b):
#     """
#     Compute the distance between two Trajectory instances.
#
#     Parameters
#     ----------
#     a, b : Trajectory
#         Two trajectories. Must have same dimensions.
#
#     Returns
#     -------
#     numpy.ndarray
#         Distance between every frame in the trajectory.
#     """
#
#     # TODO there must be a better way
#     a_xyz = a.xyz.to_numpy().reshape(*a.shape)
#     b_xyz = b.xyz.to_numpy().reshape(*b.shape)
#
#     return np.sqrt(np.sum(np.square(a_xyz - b_xyz), axis=(1, 2)))
#
# # Compute pairwise distance between two Trajectories (or within a Trajectory?)
# def pairwise_distance(a, b):
#     pass

def r1N(a):
    """
    End-to-end distance. This is a metric commonly computed in our lab.

    Parameters
    ----------
    a : Trajectory

    Returns
    -------
    """

    import warnings
    warnings.warn('experimental!')

    # Break up `a` into sub-selections for the first and last residue
    residue_ids = a.residue_ids
    a_first = a.select(residue_id=residue_ids[0])
    a_last = a.select(residue_id=residue_ids[-1])

    # Return distances
    return distances(a_first, a_last)



# Helper function to format results of `contacts` or `distances` functions
def _format_results(results, a, b, value_name, aggfunc='min', by='residue'):
    """

    Parameters
    ----------
    results : numpy.ndarray
    a : Trajectory
    b : Trajectory
    value_name : str
    aggfunc : str
    by : str

    Returns
    -------

    """

    # Make sure the dimensions make sense
    if (not all(a.structure_ids == b.structure_ids) or  # noqa
            not results.shape == (a.n_structures, a.n_atoms, b.n_atoms)):
        raise AttributeError(f'{results.shape}, {(a.n_structures, a.n_atoms, b.n_atoms)}')

    # Construct axes
    axes = (
        a.structure_ids,  # Should I check again that a.structures == b.structure_ids?
        a[f'{by}_id'],
        b[f'{by}_id']
    )

    # Set index names
    index_names = (
        'structure_id',
        f'{by}_id0',
        f'{by}_id1'
    )

    # Aggregate and return results
    return numpy_aggregate(
        results,  # noqa
        axes=axes,
        index_names=index_names,
        value_name=value_name,
        aggfunc=aggfunc,
        as_frame=True
    )
