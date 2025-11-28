"""
Integration Tests for PlotEase Library
This file verifies that all components of the library work together seamlessly
in a typical data analysis workflow using the mtcars dataset.
"""

import unittest
import pandas as pd
# Import all relevant classes to test their interactions
from plotease import PlotEase, DiagnosticPlotter, SummaryGenerator


def load_mtcars():
    """Load mtcars dataset for testing"""
    mtcars = pd.DataFrame({
        'mpg': [21.0, 21.0, 22.8, 21.4, 18.7, 18.1, 14.3, 24.4, 22.8, 19.2, 
                17.8, 16.4, 17.3, 15.2, 10.4, 10.4, 14.7, 32.4, 30.4, 33.9,
                21.5, 15.5, 15.2, 13.3, 19.2, 27.3, 26.0, 30.4, 15.8, 19.7, 15.0, 21.4],
        'cyl': [6, 6, 4, 6, 8, 6, 8, 4, 4, 6, 
                6, 8, 8, 8, 8, 8, 8, 4, 4, 4,
                4, 8, 8, 8, 8, 4, 4, 4, 8, 6, 8, 4],
        'hp': [110, 110, 93, 110, 175, 105, 245, 62, 95, 123,
               123, 180, 180, 180, 205, 215, 230, 66, 52, 65,
               97, 150, 150, 245, 175, 66, 91, 113, 264, 175, 335, 109],
        'wt': [2.620, 2.875, 2.320, 3.215, 3.440, 3.460, 3.570, 3.190, 3.150, 3.440,
               3.440, 4.070, 3.730, 3.780, 5.250, 5.424, 5.345, 2.200, 1.615, 1.835,
               2.465, 3.520, 3.435, 3.840, 3.845, 1.935, 2.140, 1.513, 3.170, 2.770, 3.570, 2.780],
        'am': [1, 1, 1, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 1, 1, 1,
               0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1]
    })
    return mtcars


class TestIntegration(unittest.TestCase):
    """Integration tests - test the full workflow and class interactions."""
    
    def setUp(self):
        """Set up the mtcars dataset for comprehensive testing."""
        self.mtcars = load_mtcars()
    
    def test_full_workflow(self):
        """Test complete workflow using all delegated features of PlotEase facade."""
        
        # 1. Initialize the Facade Class
        pe = PlotEase(self.mtcars, theme='minimal')
        
        # Test all main delegated methods
        try:
            # Feature 1: AutoPlot (Delegation to DiagnosticPlotter)
            pe.autoplot(target='mpg', max_plots=4)
            self.assertIsInstance(pe._diagnostic, DiagnosticPlotter)

            # Feature 2: Summary (Delegation to SummaryGenerator)
            summary = pe.tabular_summary(style='full')
            self.assertIsInstance(summary, pd.DataFrame)
            self.assertEqual(len(summary), 5) # 5 columns in this truncated mtcars data
            self.assertIsInstance(pe._summary, SummaryGenerator)

            # Feature 3: Model Comparison (Delegation to ModelComparator)
            models = {
                'Linear Reg': {'R²': 0.85, 'MAE': 3.2},
                'Random Forest': {'R²': 0.90, 'MAE': 2.3}
            }
            pe.compare_models(models)
            # Check that the internal comparator object was initialized
            self.assertIsNotNone(pe._comparator)

            # Feature 4: Quick Plot (Delegation to QuickPlotter)
            # This should call the underlying quick_plot logic without crashing
            pe.quick_plot('hp', 'mpg', kind='scatter')
            self.assertIsNotNone(pe._plotter)
            
            success = True
        except Exception as e:
            print(f"Integration test failed during workflow with error: {e}")
            success = False
        
        self.assertTrue(success, "The full PlotEase workflow failed to execute all components.")


if __name__ == '__main__':
    # Run with verbose output when executed directly
    unittest.main(verbosity=2)