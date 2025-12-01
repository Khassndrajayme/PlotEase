import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import Optional, Dict
from .visualization import VisualizationBase 

class TestQuickPlotter(unittest.TestCase):
    """Test QuickPlotter functionality"""
    
    def setUp(self):
        """Set up test data - using mtcars"""
        self.mtcars = load_mtcars()
    
    def test_initialization(self):
        """Test QuickPlotter initialization"""
        qp = QuickPlotter(self.mtcars)
        self.assertIsNotNone(qp)
    
    def test_detect_plot_type_numeric(self):
        """Test automatic plot type detection for numeric data"""
        qp = QuickPlotter(self.mtcars)
        
        # Single numeric variable should be histogram
        plot_type = qp.detect_plot_type('mpg', None)
        self.assertEqual(plot_type, 'hist')
        
        # Two numeric variables should be scatter
        plot_type = qp.detect_plot_type('mpg', 'hp')
        self.assertEqual(plot_type, 'scatter')
    
    def test_inheritance_from_base(self):
        """Test that QuickPlotter inherits from VisualizationBase"""
        qp = QuickPlotter(self.mtcars)
        self.assertIsInstance(qp, VisualizationBase)
    
    def test_quick_plot_mtcars_variables(self):
        """Test quick_plot with mtcars variables"""
        qp = QuickPlotter(self.mtcars)
        
        # Test plotting different mtcars relationships
        try:
            qp.quick_plot('hp', 'mpg', kind='scatter')
            qp.quick_plot('wt', 'mpg', kind='scatter')
            qp.quick_plot('mpg', kind='hist')
            success = True
        except Exception:
            success = False
        
        self.assertTrue(success)
