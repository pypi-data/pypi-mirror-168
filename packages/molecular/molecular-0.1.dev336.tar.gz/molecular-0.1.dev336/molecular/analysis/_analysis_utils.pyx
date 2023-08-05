
#cython: language_level=3

from cython.parallel cimport prange
from scipy.spatial.distance import cdist
import numpy as np
cimport numpy as np


def _distances(a, b):
    return _cdef_distances(a.astype('float64'), b.astype('float64'))

cdef np.ndarray[np.float64_t, ndim=3] _cdef_distances(np.ndarray[np.float64_t, ndim=3] a, np.ndarray[
        np.float64_t, ndim=3] b):
    # Declarations
    cdef np.ndarray[np.float64_t, ndim=3] r
    cdef np.int32_t i

    r = np.zeros((a.shape[0], a.shape[1], b.shape[1]))

    for i in np.arange(a.shape[0]):
        # r[i, :, :] = cdist(a[i, :, :], b[i, :, :])
        r[i] = cdist(a[i], b[i])

    return r


# TODO convert this to cdef and combine with cdef minimum_cross_distances
def _minimum_distances(a, b, box):
    # Convert box to right format
    box = box[:, np.newaxis, :]

    # Put a and b in box
    a = a - box * np.round(a / box)
    b = b - box * np.round(b / box)

    # Find minimum distances
    min_r = np.ones((a.shape[0], a.shape[1], b.shape[1])) * np.inf
    for dx in np.arange(-1, 2):
        for dy in np.arange(-1, 2):
            for dz in np.arange(-1, 2):
                # Move b
                bm = b + box * [dx, dy, dz]

                # Update min_r?
                r = _distances(a, bm)
                is_closer = r < min_r
                if np.sum(is_closer) > 0:
                    min_r[is_closer] = r[is_closer]

    # Return
    return min_r

def _minimum_cross_distances(a, box):
    # Convert box to right format
    box = box[:, np.newaxis, :]

    # Move `a` to origin
    ac = np.mean(a, axis=1)[:, np.newaxis, :]  # center of `a`
    a0 = a - box * np.round(ac / box)

    # Compute
    return _cdef_minimum_cross_distances(a0.astype('float64'), box.astype('float64'))

cdef np.ndarray[np.float64_t, ndim=1] _cdef_minimum_cross_distances(np.ndarray[np.float64_t, ndim=3] a0, np.ndarray[
        np.float64_t, ndim=3] box):
    cdef np.ndarray[np.float64_t, ndim=3] am
    cdef np.ndarray[np.float64_t, ndim=1] min_r
    cdef np.float64_t r
    cdef np.int32_t dx, dy, dz, i

    # Find minimum distances
    min_r = np.ones(a0.shape[0]) * np.inf
    for dx in np.arange(-1, 2):  # I don't think these loops need to be here. It's the innermost loop that's slow.
        for dy in np.arange(-1, 2):
            for dz in np.arange(-1, 2):
                # Skip origin
                if dx == 0 and dy == 0 and dz == 0:
                    continue

                # Move `a` to image
                am = a0 + box * [dx, dy, dz]

                # Update min_r?
                for i in np.arange(a0.shape[0]):
                    r = np.min(cdist(a0[i], am[i]))
                    if r < min_r[i]:
                        min_r[i] = r

    # Return
    return min_r