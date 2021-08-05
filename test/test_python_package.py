from python_package import greet, greeting
import unittest
from contextlib import redirect_stdout
from io import StringIO


# TODO replace the simple class below with actual tests for your code in python_package
class TestPythonPackage(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_version_defined(self):
        try:
            from python_package import __version__
        except ImportError:
            self.fail('__version__ not in package')

    def test_greeting(self):
        self.assertEqual('Hello', greeting(), 'greeting is Hello')

    def test_greet(self):
        f = StringIO()
        with redirect_stdout(f):
            greet('world')
            self.assertEqual('Hello world\n', f.getvalue())
