"""
Integration Tests for PlotEase Library
This file verifies that all components of the library work together seamlessly
in a typical data analysis workflow.
Run with: pytest test_integration.py -v
"""

import unittest
import pandas as pd
import numpy as np
# Import all relevant classes to test their interactions
from plotease import PlotEase


class TestIntegration(unittest.TestCase):
    """Integration tests - test the full workflow and class interactions."""
    
    def setUp(self):
        """Set up a large, diverse dataset for comprehensive testing."""
        np.random.seed(42)
        self.data = pd.DataFrame({
            'age': np.random.randint(20, 70, 100),
            'salary': np.random.randint(30000, 150000, 100),
            'experience': np.random.randint(0, 30, 100),
            'department': np.random.choice(['Sales', 'Engineering', 'Marketing'], 100),
            'target': np.random.choice([0, 1], 100) # Binary target variable
        })
    
    def test_full_workflow(self):
        """Test complete workflow using all features of PlotEase facade."""
        
        # 1. Initialize the Facade Class
        pe = PlotEase(self.data, theme='minimal')
        
        # Test all main methods
        try:
            # Feature 1: Summary (Delegation to SummaryGenerator)
            print("\n--- Testing Summary Delegation ---")
            summary = pe.tabular_summary(style='full')
            self.assertIsInstance(summary, pd.DataFrame)
            self.assertEqual(len(summary), 5) # All 5 columns summarized
            
            # Feature 2: Model Comparison (Delegation to ModelComparator)
            print("--- Testing Model Comparison Delegation ---")
            models = {
                'Model A': {'Accuracy': 0.85, 'Precision': 0.82},
                'Model B': {'Accuracy': 0.90, 'Precision': 0.87}
            }
            # This call should successfully initialize and run the comparator logic
            pe.compare_models(models)
            # Check that the internal comparator object was initialized
            self.assertIsNotNone(pe._comparator)

            # Feature 3: Quick Plot (Delegation to QuickPlotter)
            print("--- Testing Quick Plot Delegation ---")
            # This should call the underlying quick_plot logic without crashing
            pe.quick_plot('age', 'salary', kind='scatter')
            
            # Feature 4: AutoPlot (Delegation to DiagnosticPlotter)
            print("--- Testing Autoplot Delegation ---")
            # This should call the underlying diagnostic plotting logic
            pe.autoplot(target='target', max_plots=4)
            
            # Feature 5: Theme setting (Interacts with VisualizationBase and all plotters)
            print("--- Testing Theme Change ---")
            pe.set_theme('dark')
            self.assertEqual(pe._theme, 'dark')

            success = True
        except Exception as e:
            print(f"Integration test failed during workflow with error: {e}")
            success = False
        
        self.assertTrue(success, "The full PlotEase workflow failed to execute all components.")


if __name__ == '__main__':
    # Run with verbose output when executed directly
    unittest.main(verbosity=2)