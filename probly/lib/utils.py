from functools import partial, wraps

import matplotlib.pyplot as plt
import numpy as np

from ..core.random_variables import RandomVariable


def const(c):
    """
    Returns a constant random variable.

    :param c: constant value
    """

    if isinstance(c, RandomVariable):
        return c
    else:
        return RandomVariable(lambda _: c)


def hist(rv, num_samples, bins=None, density=True):
    """
    Plots a histogram from samples of a random variable.

    Parameters
    ----------
    rv : RandomVariable
        A random variable.
    num_samples : int
        The number of samples to draw from `rv`.
    bins : int or sequence, optional
        Specifies the bins in the histogram.
    density : bool, optional
        If True, the histogram is normalized to form a probability density.
    """

    samples = [rv() for _ in range(num_samples)]
    plt.hist(samples, bins=bins, density=density)
    plt.show()


def lift(f):
    """
    Lifts a function to the composition map between random variables.

    Can be used as a decorator.

    Example
    -------
    Construct a random variable given by the determinant of a Wigner matrix.

    >>> import probly as pr
    >>> import numpy as np
    >>> Det = pr.lift(np.linalg.det)
    >>> M = pr.Wigner(2, pr.Normal())
    >>> D = Det(M)
    """

    @wraps(f)
    def lifted(*args, **kwargs):
        if any((isinstance(arg, RandomVariable) for arg in args)):
            fkwargs = partial(f, **kwargs)
            return RandomVariable(fkwargs, *args)
        else:
            return f(*args, **kwargs)

    return lifted
