"""

note: all the functions that end with "0" in this document are worse versions of the ones that don't end in "0".
"""

from molecular.analysis._analysis_utils import _minimum_cross_distances

from molecular.analysis import contacts, distances
from molecular.simulations import generate_images

import numpy as np


def has_cross_interactions0(a, cutoff=4.5):
    # Move `a` to the unit cell
    a0 = a.to_image(0, 0, 0, inplace=False)

    # Go through all images and find cross interactions
    is_crossed = np.zeros(a.n_structures, dtype='bool')
    for image in generate_images(exclude_origin=True):
        am = a.to_image(*image, inplace=False)  # use `a` directly to avoid creating a copy
        is_crossed = is_crossed | np.max(contacts(a0, am, cutoff=cutoff, include_images=False), axis=(1, 2))

    # Return
    return is_crossed


def has_cross_interactions(a, cutoff=4.5):
    return minimum_cross_distances(a) <= cutoff


def has_mediated_cross_interactions0(a, b, cutoff=4.5):  # a protein, b ligand
    a0 = a.to_image(0, 0, 0, inplace=False)
    b0 = b.to_image(0, 0, 0, inplace=False)
    is_crossed = np.zeros(a.n_structures, dtype='bool')
    for image0 in generate_images(exclude_origin=False):
        bm = b0.to_image(*image0, inplace=False)
        contact0 = np.max(contacts(a0, bm, cutoff=cutoff, include_images=False), axis=(1, 2))
        for image1_ in generate_images(exclude_origin=False):
            image1 = tuple(np.array(image0) + np.array(image1_))
            if image1 == (0, 0, 0):
                break
            am = a0.to_image(*image1, inplace=False)
            contact1 = np.max(contacts(am, bm, cutoff=cutoff, include_images=False), axis=(1, 2))
            is_crossed = is_crossed | (contact0 & contact1)
    return is_crossed


def has_mediated_cross_interactions(a, b, cutoff=4.5):  # a protein, b ligand
    """
    Check if `a` is able to interact with another image of itself where both images are bound to the same instance of
    `b`.

    Parameters
    ----------
    a : Trajectory
    b : Trajectory
    cutoff : float

    Returns
    -------
        numpy.ndarray Boolean array indicating if `a` has mediated cross-interactions with `b`. The size of the array is
        the number of structures in `a`.
    """

    # Check `a` and `b` have the same parent
    if a.parent.designator != b.parent.designator:
        raise AttributeError('`a` and `b` must have same parent')

    # Move `a` and `b` to unit cell
    a0 = a.to_image(0, 0, 0, inplace=False)
    b0 = b.to_image(0, 0, 0, inplace=False)

    # Extract boxes and check that `a_box` and `b_box` are identical
    # TODO package this into a utility function
    a_box = a.box.to_numpy()
    b_box = b.box.to_numpy()
    if np.allclose(a_box, b_box) is not True:
        raise AttributeError('`a` and `b` have different dimensions')

    # Compute
    n_bound_images = np.zeros(a.n_structures, dtype='int')
    for image in generate_images(exclude_origin=False):
        bm = b0.to_image(*image, inplace=False)
        n_bound_images = n_bound_images + np.max(contacts(a0, bm, cutoff=cutoff, include_images=False), axis=(1, 2))

    # Return
    return n_bound_images > 1


def minimum_cross_distances0(a):
    # Move `a` to the unit cell
    a0 = a.to_image(0, 0, 0, inplace=False)

    # Go through all images and find cross interactions
    distances = np.ones(a.n_structures) * np.inf
    for image in generate_images(exclude_origin=True):
        am = a.to_image(*image, inplace=False)  # use `a` directly to avoid creating a copy
        r = np.min(distances(a0, am, include_images=False), axis=(1, 2))
        mask = r < distances
        if np.sum(mask) > 0:
            distances[mask] = r[mask]

    # Return
    return distances


def minimum_cross_distances(a):
    """
    The minimum cross distance is the minimum atomic distance between two images of the same molecule `a`.

    Parameters
    ----------
    a : Trajectory

    Returns
    -------
    numpy.ndarray
        The minimum cross distance for each structure in `a`.
    """

    # Extract coordinates
    xyz = a.xyz.to_numpy().reshape(*a.shape)

    # Extract boxes and check that `a_box` and `b_box` are identical
    box = a.box.to_numpy()

    # Finally, we can compute the minimum distances
    return _minimum_cross_distances(xyz, box)
