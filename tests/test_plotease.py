"""
Unit Tests for PlotEase Core Functionality
This file verifies the Abstract Base Class (ABC) contract,
PlotEase initialization, and basic encapsulation methods.
Run with: pytest test_plotease.py -v
"""

import unittest
import pandas as pd
# Import the core classes for testing
from plotease import PlotEase, VisualizationBase


class TestVisualizationBaseContract(unittest.TestCase):
    """
    Test the Abstract Base Class (ABC) to ensure it enforces the contract
    (i.e., cannot be instantiated directly and requires concrete implementation).
    """
    
    def setUp(self):
        """Set up valid test data for subclasses."""
        self.valid_data = pd.DataFrame({
            'age': [25, 30, 35, 40, 45],
            'salary': [50000, 60000, 70000, 80000, 90000]
        })
    
    def test_cannot_instantiate_abstract_class(self):
        """Test that VisualizationBase cannot be instantiated directly."""
        with self.assertRaises(TypeError) as cm:
            # Attempting to instantiate an ABC should raise a TypeError
            VisualizationBase(self.valid_data)
        
        # Verify the error message relates to the abstract method 'render'
        self.assertIn("Can't instantiate abstract class", str(cm.exception))

    def test_inheritance(self):
        """Test that PlotEase correctly inherits from VisualizationBase (Inheritance)."""
        pe = PlotEase(self.valid_data)
        self.assertIsInstance(pe, VisualizationBase)


class TestPlotEaseCore(unittest.TestCase):
    """Test PlotEase initialization, data validation, and encapsulation."""
    
    def setUp(self):
        """Set up standard test data."""
        self.valid_data = pd.DataFrame({
            'age': [25, 30, 35, 40, 45],
            'salary': [50000, 60000, 70000, 80000, 90000],
            'department': ['Sales', 'HR', 'IT', 'Sales', 'HR']
        })
    
    # --- Initialization and Validation Tests ---

    def test_valid_initialization(self):
        """Test successful initialization with valid data and a custom theme."""
        pe = PlotEase(self.valid_data, theme='minimal')
        self.assertIsNotNone(pe)
        self.assertEqual(pe._theme, 'minimal')
    
    def test_invalid_data_type(self):
        """Test TypeError when passing non-DataFrame data."""
        with self.assertRaises(TypeError):
            PlotEase([1, 2, 3])
        
        with self.assertRaises(TypeError):
            PlotEase(None)
    
    def test_empty_dataframe(self):
        """Test ValueError when passing an empty DataFrame."""
        with self.assertRaises(ValueError):
            PlotEase(pd.DataFrame())
    
    # --- Encapsulation Tests ---

    def test_get_data(self):
        """Test data getter method (get_data) to check Encapsulation."""
        pe = PlotEase(self.valid_data)
        retrieved_data = pe.get_data()
        self.assertTrue(retrieved_data.equals(self.valid_data))
    
    def test_set_theme(self):
        """Test theme setter method (set_theme) to check Encapsulation."""
        pe = PlotEase(self.valid_data, theme='default')
        self.assertEqual(pe._theme, 'default')

        pe.set_theme('dark')
        self.assertEqual(pe._theme, 'dark')


if __name__ == '__main__':
    # Run with verbose output when executed directly
    unittest.main(verbosity=2)