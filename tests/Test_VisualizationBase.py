"""
Unit Tests for VisualizationBase (Abstract Base Class)
This file verifies the abstract nature, inheritance, and core non-abstract
methods of the VisualizationBase class.
"""
import unittest
import pandas as pd
from abc import ABC
# Import the class being tested and a concrete class for instantiation checks
from plotease import VisualizationBase, PlotEase, DiagnosticPlotter 


class TestVisualizationBase(unittest.TestCase):
    """Test the abstract base class"""
    def load_mtcars():
    """Load mtcars dataset for testing"""
    # Using a simplified version for the base class test
    return pd.DataFrame({
        'A': [1, 2, 3],
        'B': [10, 20, 30]
    })
    
    def setUp(self):
        """Set up test data - using mtcars"""
        self.mtcars = load_mtcars()
    
    def test_cannot_instantiate_abstract_class(self):
        """Test that abstract class cannot be instantiated directly"""
        with self.assertRaises(TypeError):
            VisualizationBase(self.mtcars)
    
    def test_inheritance(self):
        """Test that subclasses inherit from base"""
        pe = PlotEase(self.mtcars)
        self.assertIsInstance(pe, VisualizationBase)
        
        dp = DiagnosticPlotter(self.mtcars)
        self.assertIsInstance(dp, VisualizationBase)


if __name__ == '__main__':
    # Run with verbose output when executed directly
    unittest.main(verbosity=2)
