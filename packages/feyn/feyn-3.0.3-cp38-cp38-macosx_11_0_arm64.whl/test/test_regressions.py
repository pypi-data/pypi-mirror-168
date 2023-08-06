"""
This file contains regression errors observed in production. Some of these tests may
be a bit gnarly formulated, they may be a bit more fragile, and they probably do not
smell like a requirement specification for the feyn.

The idea is, that these can be deleted whenever they become too annoying.
"""


import numpy as np
import pandas as pd

import feyn
import _qepler
from . import quickmodels

import unittest


class TestMiscRegressions(unittest.TestCase):
    def test_filter_works_with_numpy_int(self):
        inputs, output = list('abc'), 'output'

        models = [
            quickmodels.get_unary_model(inputs, output), # Complexity 2
            quickmodels.get_simple_binary_model(inputs, output) # Complexity 3
        ]

        n2 = sum(map(lambda m: m.edge_count == 2, models))
        complexity_filter = feyn.filters.Complexity(np.int64(2))

        filtered_models = list(filter(complexity_filter, models))
        self.assertEqual(n2, len(filtered_models))
