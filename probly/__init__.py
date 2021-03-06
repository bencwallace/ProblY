"""
Probly implements random variables and methods to aid in their manipulation and construction.
"""


from .core import *
from .distr import *
from .lib import *

__all__ = []

__all__ += ['seed']

__all__ += ['array']
__all__ += ['const', 'hist', 'lift', 'iid']
__all__ += ['mean', 'variance', 'cdf']

# Discrete random variables
__all__ == ['Distribution', 'model']
__all__ += ['RandInt']
__all__ += ['Multinomial', 'Bin', 'Ber']
__all__ += ['NegBin', 'Geom']
__all__ += ['HyperGeom', 'Pois']

# Continuous random variables
__all__ += ['Gamma', 'ChiSquared', 'Exp']
__all__ += ['Unif']
__all__ += ['Normal']
__all__ += ['Beta', 'PowerLaw']
__all__ += ['F', 'StudentT']
__all__ += ['Laplace', 'Logistic', 'VonMises']

# Random matrices
__all__ += ['Wigner', 'Wishart']
