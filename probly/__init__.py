"""probly.py: A python module for working with random variables."""

import copy
import networkx as nx
import numpy as np
import operator as op
from functools import wraps

from .programs import _programs
from .helpers import get_seed, _max_seed


def Lift(f):
    """Lifts a function to the composition map between random variables."""

    @wraps(f)
    def F(*args):
        """
        The lifted function

        Args:
            `rv`s and constants
        """

        return rv(f, *args)

    return F


class rv(object):
    """
    A random variable placeholder.

    Can be acted upon by arithmetical operations and functions compatible with
    `Lift`.
    """

    graph = nx.MultiDiGraph()

    def __init__(self, method=None, *args):
        # assert callable(method), '{} is not callable'.format(method)

        if len(args) == 0:
            args = [root]
        if method is None:
            # Seeding wrapper for `self.sampler`
            def sampler(seed=None):
                np.random.seed(seed)
                return self.sampler(seed)
            method = sampler

        edges = [(rv._cast(var), self, {'index': i})
                 for i, var in enumerate(args)]
        rv.graph.add_node(self, method=method)
        rv.graph.add_edges_from(edges)

    def __call__(self, seed=None):
        seed = get_seed(seed)
        parents = list(self.parents())

        # Create {index: parent} dictionary `arguments`
        # This could probably be made more clear
        data = [rv.graph.get_edge_data(p, self) for p in parents]
        arguments = {}
        for i in range(len(parents)):
            indices = [d.values() for d in data[i].values()]
            for j in range(len(indices)):
                arguments[data[i][j]['index']] = parents[i]

        # Sample elements of `parents` in order specified by `arguments`
        # and apply `method` to result
        samples = [arguments[i]((seed + id(self)) % _max_seed)
                   for i in range(len(arguments))]
        method = rv.graph.nodes[self]['method']
        return method(*samples)

    def __getitem__(self, key):
        assert hasattr(self(0), '__getitem__'),\
            'Scalar {} object not subscriptable'.format(self.__class__)
        return rv._getitem(self, key)

    # Define operators for emulating numeric types
    for p in _programs:
        exec(p)

    def parents(self):
        """Returns list of random variables from which `self` is defined"""
        if self in rv.graph:
            return list(rv.graph.predecessors(self))
        else:
            return []

    # Constructors
    @classmethod
    def _getitem(cls, obj, key):
        def get(arr):
            return arr[key]
        return Lift(get)(obj)

    @classmethod
    def _cast(cls, obj):
        """Cast constants to `rv` objects."""

        if isinstance(obj, cls):
            return obj
        elif hasattr(obj, '__getitem__'):
            return rv.array(obj)
        else:
            return cls(lambda seed=None: obj)

    @classmethod
    def copy(cls, obj):
        """Return a random variable with the same distribution as `self`"""

        # Shallow copy is ok as `rv` isn't mutable
        return copy.copy(obj)

    @classmethod
    def array(cls, arr):
        arr = np.array([rv._cast(var) for var in arr])

        def make_array(*args):
            return np.array(args)
        return Lift(make_array)(*arr)


class Root(rv):
    """The root of the dependency tree is the random number generator."""

    def __init__(self):
        rv.graph.add_node(self)

    def __call__(self, seed=None):
        return get_seed(seed)


root = Root()
