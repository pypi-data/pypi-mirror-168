import unittest

import pandas as pd

from .. import quickmodels
from feyn.plots._model_response_2d import plot_model_response_2d


class TestPlotResponse2d(unittest.TestCase):

    def test_plot_function_runs(self):
        """Test that the function can be run without raising an error"""
        # Setup
        num_observations = 5
        model = quickmodels.get_simple_binary_model(["a", "b"], "output")
        assert model is not None
        test_df = pd.DataFrame({"a": list(range(num_observations)), 'b': list(range(num_observations)), "output": list(range(num_observations))})

        # Run plot function
        plot_model_response_2d(model, test_df)
