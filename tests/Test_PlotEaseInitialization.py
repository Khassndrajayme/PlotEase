"""
Unit Tests for PlotEase Initialization and Data Validation
This file verifies the core functionality of the PlotEase constructor, including
data checks, theme setting, and basic encapsulation methods.
"""
import unittest
import pandas as pd
# Import the main class for testing
from plotease import PlotEase


def load_mtcars():
    """Load mtcars dataset for testing"""
    # NOTE: This data is copied locally to ensure the test is self-contained.
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
               2.465, 3.520, 3.435, 3.840, 3.845, 1.935, 2.140, 1.513, 3.170, 2.770, 3.570, 2.780]
    })
    return mtcars


class TestPlotEaseInitialization(unittest.TestCase):
    """Test PlotEase initialization, validation, and core property methods."""
    
    def setUp(self):
        """Set up test data - using mtcars."""
        self.mtcars = load_mtcars()
        
  
    # Initialization and Validation Tests
   
    def test_valid_initialization(self):
        """Test successful initialization with mtcars data."""
        # Using a theme ensures theme setting is handled correctly
        pe = PlotEase(self.mtcars, theme='minimal')
        self.assertIsNotNone(pe)
        self.assertEqual(pe._theme, 'minimal')
        self.assertEqual(len(pe), 32)  # mtcars has 32 rows
        
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

    
    # Encapsulation Tests (Getters/Setters inherited from Base)
   
    def test_get_data(self):
        """Test data getter method (encapsulation)."""
        pe = PlotEase(self.mtcars)
        retrieved_data = pe.get_data()
        self.assertTrue(retrieved_data.equals(self.mtcars))
        
    def test_set_theme(self):
        """Test theme setter method (encapsulation)."""
        pe = PlotEase(self.mtcars, theme='default')
        self.assertEqual(pe._theme, 'default')
        
        pe.set_theme('dark')
        self.assertEqual(pe._theme, 'dark')


if __name__ == '__main__':
    # Run with verbose output when executed directly
    unittest.main(verbosity=2)
