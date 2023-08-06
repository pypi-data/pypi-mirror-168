import unittest

import numpy as np

from feyn.metrics import get_mutual_information, calculate_mi
from .. import quickmodels

class TestGetMI(unittest.TestCase):

    def test_works_with_np_dict(self):
        model = quickmodels.get_identity_model()

        x = np.random.randint(0,10,10)

        data = {"x": x, "y": x}

        test_mi = get_mutual_information(model, data)

        # This relies on knowing the steps in indentity_model
        actual_mi_0 = calculate_mi([x, x*.5-.5])
        actual_mi_1 = calculate_mi([x, x])

        self.assertTrue(np.allclose(test_mi, [actual_mi_1, actual_mi_0]))

