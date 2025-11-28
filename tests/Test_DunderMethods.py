"""
Unit Tests for Dunder Methods (__methods__)
This file verifies the Pythonic integration of PlotEase through operator overloading.
Run with: pytest test_dundermethods.py -v
"""

import unittest
import pandas as pd
# Import the main class that implements/overrides the dunder methods
from plotease import PlotEase


class TestDunderMethods(unittest.TestCase):
    """Test dunder methods (magic methods) defined in VisualizationBase and PlotEase."""
    
    def setUp(self):
        """Set up test data with different sizes for comparison tests."""
        self.data1 = pd.DataFrame({
            'x': [1, 2, 3, 4, 5], # 5 rows
            'y': [10, 20, 30, 40, 50]
        })
        self.data2 = pd.DataFrame({
            'x': [1, 2, 3], # 3 rows
            'y': [10, 20, 30]
        })
    
    def test_repr(self):
        """Test __repr__ method for correct developer-friendly string representation."""
        pe = PlotEase(self.data1, theme='colorful')
        repr_str = repr(pe)
        # Check for class name, row count, column count, and theme
        self.assertIn('PlotEase', repr_str)
        self.assertIn('rows=5', repr_str)
        self.assertIn('cols=2', repr_str)
        self.assertIn("theme='colorful'", repr_str)
    
    def test_len(self):
        """Test __len__ method, allowing len(pe) to return the row count."""
        pe = PlotEase(self.data1)  # 5 rows
        self.assertEqual(len(pe), 5)
        
        pe2 = PlotEase(self.data2) # 3 rows
        self.assertEqual(len(pe2), 3)
    
    def test_eq(self):
        """Test __eq__ method (==) for object equality based on data and theme."""
        # Case 1: Identical data and theme
        pe1 = PlotEase(self.data1, theme='minimal')
        pe2 = PlotEase(self.data1, theme='minimal')
        self.assertEqual(pe1, pe2)
        
        # Case 2: Different data (should be False)
        pe3 = PlotEase(self.data2, theme='minimal')
        self.assertNotEqual(pe1, pe3)
        
        # Case 3: Different theme, same data (should be False)
        pe4 = PlotEase(self.data1, theme='dark')
        self.assertNotEqual(pe1, pe4)
    
    def test_lt(self):
        """Test __lt__ method (<) for comparison based on data size (row count)."""
        pe1 = PlotEase(self.data1)  # 5 rows
        pe2 = PlotEase(self.data2)  # 3 rows
        
        self.assertFalse(pe1 < pe2)  # 5 < 3 = False
        self.assertTrue(pe2 < pe1)   # 3 < 5 = True
        self.assertFalse(pe1 < pe1)  # 5 < 5 = False


if __name__ == '__main__':
    # Run with verbose output when executed directly
    unittest.main(verbosity=2)