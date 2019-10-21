"""
Probly implements random variables and methods to aid in their construction.

The main objects of Probly are random variable classes. These inherit from the
core class ``RandomVariable``, which acts as a subclassing interface for a node
in a computational graph. Probly also provides methods to help in the formation
of new random variables.
"""


# Utilities
from .utils import array, hist, Lift, sum
from .utils import Wigner, Wishart

# Discrete random variables
from .distributions import DUnif
from .distributions import Multinomial, Bin, Ber
from .distributions import NegBin, Geom
from .distributions import HyperGeom, Pois

# Continuous random variables
from .distributions import Gamma, ChiSquared, Exp
from .distributions import Unif
from .distributions import Normal, LogNormal
from .distributions import Beta, PowerLaw
from .distributions import F, Student_t
from .distributions import Laplace, Logistic, VonMises

__all__ = []

# Constructors and helpers
__all__ += ['Lift', 'array', 'sum']
__all__ += ['hist', 'mean']

# Discrete random variables
__all__ += ['DUnif']
__all__ += ['Multinomial', 'Bin', 'Ber']
__all__ += ['NegBin', 'Geom']
__all__ += ['HyperGeom', 'Pois']

# Continuous random variables
__all__ += ['Gamma', 'ChiSquared', 'Exp']
__all__ += ['Unif']
__all__ += ['Normal', 'LogNormal']
__all__ += ['Beta', 'PowerLaw']
__all__ += ['F', 'Student_t']
__all__ += ['Laplace', 'Logistic', 'VonMises']

# Random matrices
__all__ += ['Wigner', 'Wishart']
