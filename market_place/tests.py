import unittest
from django.test import TestCase
import doctest
from . import mydoctests
# Create your tests here.


# def suite():
#     m_suite = unittest.TestSuite()
#     m_suite.addTest(doctest.DocFileSuite(mydoctests))
#     return m_suite

def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(mydoctests))
    return tests
