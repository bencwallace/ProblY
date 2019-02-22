"""probly.py: A python module for working with random variables."""

import math
import networkx as nx
import numpy as np
import operator as op

import random

from os import urandom

# Numpy max seed
_max_seed = 2 ** 32 - 1

# Exec programs for automating repetitive operator definitions
_num_ops_lift = ['add', 'sub', 'mul', 'matmul',
                 'truediv', 'floordiv', 'mod', 'divmod', 'pow']
_num_ops_right = ['add', 'sub', 'mul', 'matmul', 'truediv', 'floordiv', 'mod',
                  'divmod', 'pow']
_num_ops_unary = ['neg', 'pos', 'abs', 'complex', 'int', 'float', 'round',
                  'trunc', 'floor', 'ceil']

_programs_lift = [
    (
        'def __{:s}__(self, x):\n'
        '    return Lift(op.{:s})(self, x)'
    ).format(fcn, fcn) for fcn in _num_ops_lift]

_programs_right = [
    (
        'def __r{:s}__(self, x):\n'
        '   X = rvar.convert(x)\n'
        '   return X.__{:s}__(self)'
    ).format(fcn, fcn) for fcn in _num_ops_right]

_programs_unary = [
    (
        'def __{:s}__(self):\n'
        '   return Lift(op.{:s})(self)'
    ).format(fcn, fcn) for fcn in _num_ops_unary]
_programs = _programs_lift + _programs_right + _programs_unary


def Lift(f):
    """Lifts a function to the composition map between random variables."""

    def F(*args):
        """
        The lifted function

        Args:
            `rvar`s and constants
        """

        return rvar.compose(f, *args)

    return F


def get_seed(seed=None):
    """
    Generate a random seed. If a seed is provided, returns it unchanged.

    Based on the Python implementation. A consistent approach to generating
    re-usable random seeds is needed in order to implement dependency.
    """

    if seed is not None:
        return seed

    try:
        max_bytes = math.ceil(np.log2(_max_seed) / 8)
        seed = int.from_bytes(urandom(max_bytes), 'big')
    except NotImplementedError:
        raise

    return seed


class rvar(object):
    """
    A random variable placeholder.

    Can be acted upon by arithmetical operations and functions compatible with
    `Lift`.
    """

    graph = nx.DiGraph()

    def __init__(self, sampler=None, f=None, *args):
        self.sampler = sampler
        if self.sampler is not None:
            assert callable(sampler), '`sampler` is not callable'

        if f is not None:
            rvar.graph.add_node(self, method=f)
            edges = [(rvar.convert(var), self, {'index': i})
                     for i, var in enumerate(args)]
            rvar.graph.add_edges_from(edges)

    def __call__(self, seed=None):
        seed = get_seed(seed)
        parents = list(self.parents())

        if len(parents) == 0:
            # Seed as follows for independence of `rvar`s with same `sampler`
            return self.sampler((seed + id(self)) % _max_seed)
        else:
            # Re-order parents according to edge index
            data = [rvar.graph.get_edge_data(p, self) for p in parents]
            indices = [d['index'] for d in data]
            parents = [parents[i] for i in indices]

            # Sample from parents and evaluate method on samples
            samples = [p(seed) for p in parents]
            method = rvar.graph.nodes[self]['method']
            return method(*samples)

    def __getitem__(self, key):
        return rvar.getitem(self, key)

    # Define operators for emulating numeric types
    for p in _programs:
        exec(p)

    def parents(self):
        """Returns list of random variables from which `self` is defined"""
        if self in rvar.graph:
            return list(rvar.graph.predecessors(self))
        else:
            return []

    @classmethod
    def convert(cls, obj):
        """Converts constants to `rvar` objects."""

        if isinstance(obj, cls):
            return obj
        else:
            return cls(lambda seed=None: obj)

    @classmethod
    def define(cls, sampler):
        return cls(sampler)

    @classmethod
    def from_random(cls, random_sampler):
        def seeded_sampler(seed=None):
            random.seed(seed)
            return random_sampler()
        return cls(seeded_sampler)

    @classmethod
    def from_numpy(cls, numpy_sampler):
        def seeded_sampler(seed=None):
            np.random.seed(seed)
            return numpy_sampler()
        return cls(seeded_sampler)

    @classmethod
    def from_scipy(cls, scipy_rv):
        return cls(lambda seed=None: scipy_rv.rvs(random_state=seed))

    @classmethod
    def compose(cls, f, *args):
        return cls(None, f, *args)

    @classmethod
    def array(cls, arr):
        def make_array(*args):
            return np.array(args)
        return cls.compose(make_array, *arr)

    @classmethod
    def getitem(cls, obj, key):
        def get(arr):
            return arr[key]
        return cls.compose(get, obj)
