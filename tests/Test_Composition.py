"""
Unit Tests for PlotEase Composition
This file verifies the relationship where PlotEase "has-a" component.
Run with: pytest test_composition.py -v
"""

import unittest
import pandas as pd
# Import the classes relevant to Composition testing
from plotease import (
    PlotEase, 
    DiagnosticPlotter, 
    SummaryGenerator,
    QuickPlotter
)


class TestComposition(unittest.TestCase):
    """Test composition - PlotEase contains other classes and delegates tasks."""
    
    def setUp(self):
        """Set up test data"""
        self.data = pd.DataFrame({
            'age': [25, 30, 35, 40, 45],
            'salary': [50000, 60000, 70000, 80000, 90000]
        })
    
    def test_plotease_contains_diagnostic_plotter(self):
        """Test that PlotEase contains DiagnosticPlotter (Composition)"""
        pe = PlotEase(self.data)
        # Check that the internal attribute exists and is the correct type
        self.assertIsInstance(pe._diagnostic, DiagnosticPlotter)
    
    def test_plotease_contains_summary_generator(self):
        """Test that PlotEase contains SummaryGenerator (Composition)"""
        pe = PlotEase(self.data)
        self.assertIsInstance(pe._summary, SummaryGenerator)
    
    def test_plotease_contains_quick_plotter(self):
        """Test that PlotEase contains QuickPlotter (Composition)"""
        pe = PlotEase(self.data)
        self.assertIsInstance(pe._plotter, QuickPlotter)
    
    def test_delegation_to_components(self):
        """
        Test that PlotEase delegates calls to its components.
        This verifies the Facade pattern's delegation mechanism.
        """
        pe = PlotEase(self.data)
        
        # Delegation to SummaryGenerator: tabular_summary
        summary = pe.tabular_summary(style='numeric')
        
        # Verify the delegated method ran and returned the expected type
        self.assertIsInstance(summary, pd.DataFrame)
        self.assertEqual(len(summary), 2)  # Should only return 'age' and 'salary'
        self.assertTrue('Mean' in summary.columns)

    # NOTE: In a real test, you would also ideally mock the autoplot/quick_plot
    # methods to ensure the delegation happens without relying on actual plot generation.


if __name__ == '__main__':
    # Running this file directly will execute only the composition tests
    unittest.main(verbosity=2)