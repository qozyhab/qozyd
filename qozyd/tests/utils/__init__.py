from types import ModuleType, FunctionType
from unittest import TestCase

from qozyd.utils import import_symbol

class ImportSymbolTest(TestCase):
    def test_import(self):
        self.assertIsInstance(import_symbol("qozyd.utils.import_symbol"), FunctionType)
        self.assertIsInstance(import_symbol("qozyd.utils"), ModuleType)
