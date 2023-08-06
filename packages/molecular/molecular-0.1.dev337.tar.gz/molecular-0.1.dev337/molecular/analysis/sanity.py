
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
    # Extract coordinates
    xyz = a.xyz.to_numpy().reshape(*a.shape)

    # Extract boxes and check that `a_box` and `b_box` are identical
    box = a.box.to_numpy()

    # Finally, we can compute the minimum distances
    return _minimum_cross_distances(xyz, box)


