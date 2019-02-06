from qozyd.http import NotFoundException
from qozyd.http.utils import get_or_404
from unittest import TestCase


class UtilsTest(TestCase):
    def test_get_or_404(self):
        test_dict = {
            "key": "value"
        }

        with self.assertRaises(NotFoundException):
            get_or_404(test_dict, "missing_key")

        self.assertEqual(get_or_404(test_dict, "key"), "value")
