
from .replica_exchange import *

__all__ = [
    'ExchangeHistory',
    'generate_images',
    'get_pme_size',
    'temperature_schedule',
    'tempsch'
]


def generate_images(n=1, exclude_origin=False):
    from itertools import product
    import numpy as np
    results = list(product(np.arange(-n, n+1, dtype='int'), repeat=3) )
    if exclude_origin:
        results = [result for result in results if result != (0, 0, 0)]
    return results


# TODO move this to a better location
# TODO does this actually belong in the package namdtools?
def get_pme_size(a):
    """
    Given a box length, figure out the grid size for PME. We are looking for the PME size that's ~1 grid spacing, while
    with only small prime factors 2, 3, and 5.

    Parameters
    ----------
    a : numeric
        Size of box length.

    Returns
    -------
    int
        Size of PME grid length.
    """

    # To reduce runtime, import this here
    # TODO can this be replaced with a numpy or scipy package?
    from sympy.ntheory import factorint

    # If a is a decimal, round up
    a = int(np.ceil(a))

    # We want to find larger number that has only factors 2, 3, and 5
    # noinspection PyShadowingNames
    def _has_only_factors(a):
        factors = np.array(list(factorint(a).keys()))
        for factor in [2, 3, 5]:
            factors = np.delete(factors, np.where(factors == factor))
        return len(factors) == 0

    # Keep on increasing a until we find the right number
    while not _has_only_factors(a):
        a += 1

    # Return
    return a


# TODO when n_waters is used, why doesn't this agree with autoionize from VMD?
def salt_concentration(n_ions, box=None, n_waters=None):
    import numpy as np
    from scipy.constants import Avogadro

    moles = n_ions / Avogadro
    if n_waters is not None:
        volume = n_waters * 3e-26  # L per 1 water
    elif box is not None:
        volume = np.product(box) * 1e-27  # L per A^3
    else:
        raise AttributeError

    return moles / volume


if __name__ == '__main__':
    print(salt_concentration(24, n_waters=8394))
