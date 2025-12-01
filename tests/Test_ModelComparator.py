"""
Unit Tests for ModelComparator Component
This file verifies the logic for managing and comparing machine learning model performance metrics.
"""
import unittest
import pandas as pd
# Import the class specific to this component's tests
from plotease import ModelComparator


class TestModelComparator(unittest.TestCase):
    """Test ModelComparator functionality"""
    
    def setUp(self):
        """Set up test data - models predicting mpg"""
        self.models = {
            'Linear Regression': {'R²': 0.85, 'MAE': 2.5, 'RMSE': 3.2},
            'Random Forest': {'R²': 0.92, 'MAE': 1.8, 'RMSE': 2.3},
            'XGBoost': {'R²': 0.94, 'MAE': 1.5, 'RMSE': 2.0}
        }
    
    def test_initialization(self):
        """Test ModelComparator initialization"""
        mc = ModelComparator(self.models)
        self.assertIsNotNone(mc)
    
    def test_get_best_model(self):
        """Test getting best model by metric"""
        mc = ModelComparator(self.models)
        
        best_r2 = mc.get_best_model('R²')
        self.assertEqual(best_r2, 'XGBoost')
        
        # For MAE and RMSE, lower is better, but our method finds max
        # So we test with metrics where higher is better
        models_accuracy = {
            'Model A': {'Accuracy': 0.85, 'Precision': 0.82},
            'Model B': {'Accuracy': 0.92, 'Precision': 0.90}
        }
        mc2 = ModelComparator(models_accuracy)
        best_acc = mc2.get_best_model('Accuracy')
        self.assertEqual(best_acc, 'Model B')
    
    def test_get_best_model_invalid_metric(self):
        """Test ValueError for invalid metric"""
        mc = ModelComparator(self.models)
        
        with self.assertRaises(ValueError):
            mc.get_best_model('InvalidMetric')
    
    def test_eq_dunder(self):
        """Test __eq__ method"""
        mc1 = ModelComparator(self.models)
        mc2 = ModelComparator(self.models)
        
        self.assertEqual(mc1, mc2)
    
    def test_gt_dunder(self):
        """Test __gt__ method (greater than)"""
        models_good = {
            'Model A': {'Accuracy': 0.95, 'Precision': 0.93}
        }
        models_poor = {
            'Model B': {'Accuracy': 0.75, 'Precision': 0.73}
        }
        
        mc_good = ModelComparator(models_good)
        mc_poor = ModelComparator(models_poor)
        
        self.assertTrue(mc_good > mc_poor)
        self.assertFalse(mc_poor > mc_good)


if __name__ == '__main__':
    # Run with verbose output when executed directly
    unittest.main(verbosity=2)
