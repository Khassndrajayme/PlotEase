"""
Unit Tests for DiagnosticPlotter Component
This file verifies the functionality of diagnostic data visualization.
Run with: pytest test_diagnostic_plotter.py -v
"""

import unittest
import pandas as pd
import numpy as np
# Import classes specific to this component's tests
from plotease import DiagnosticPlotter, VisualizationBase


class TestDiagnosticPlotter(unittest.TestCase):
    """Test DiagnosticPlotter functionality, focusing on data inspection plots."""
    
    def setUp(self):
        """Set up test data for plotting simulations."""
        np.random.seed(42)
        # Create a realistic DataFrame with numeric and categorical data
        self.data = pd.DataFrame({
            'age': np.random.randint(20, 70, 50),
            'salary': np.random.randint(30000, 150000, 50),
            'experience': np.random.randint(0, 30, 50),
            'department': np.random.choice(['Sales', 'Engineering', 'Marketing'], 50)
        })
    
    def test_initialization(self):
        """Test DiagnosticPlotter initialization."""
        dp = DiagnosticPlotter(self.data)
        self.assertIsNotNone(dp)
        self.assertIsInstance(dp, DiagnosticPlotter)
    
    def test_inheritance_from_base(self):
        """Test that DiagnosticPlotter inherits from VisualizationBase (Inheritance)."""
        dp = DiagnosticPlotter(self.data)
        self.assertIsInstance(dp, VisualizationBase)
        
    def test_autoplot_runs_without_error(self):
        """
        Test that autoplot executes without raising exceptions.
        In a production environment, you would use mocking (e.g., mock.patch('matplotlib.pyplot.show')) 
        to prevent plots from actually appearing and to verify the correct plotting functions are called.
        """
        dp = DiagnosticPlotter(self.data)
        try:
            # Test a run with a target variable
            dp.autoplot(target='salary', max_plots=4)
            # Test a run without a target variable
            dp.autoplot(max_plots=2) 
            success = True
        except Exception as e:
            # Fail the test if any exception occurs during plotting setup
            print(f"Autoplot failed with error: {e}")
            success = False
        
        self.assertTrue(success, "DiagnosticPlotter's autoplot method raised an exception.")


if __name__ == '__main__':
    # Run with verbose output when executed directly
    unittest.main(verbosity=2)