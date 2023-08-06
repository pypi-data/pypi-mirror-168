import unittest

import numpy as np
import pandas as pd

from feyn.metrics import get_pearson_correlations

from .. import quickmodels


class TestPearsonCorrelation(unittest.TestCase):

    def test_works_with_np_dict(self):
        model = quickmodels.get_fixed_model()
        data = {
            'z': np.random.random(5),
            'y': np.random.random(5),
            'x': np.random.random(5)
        }
        mutual = get_pearson_correlations(model, data)
        assert mutual is not None


    def test_works_with_pd_dataframe(self):
        model = quickmodels.get_fixed_model()
        data = pd.DataFrame({
            'z': np.random.random(5),
            'y': np.random.random(5),
            'x': np.random.random(5)
        })
        mutual = get_pearson_correlations(model, data)
        assert mutual is not None
