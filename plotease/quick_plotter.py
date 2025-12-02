import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import Optional, Dict
from .visualization import VisualizationBase 

class QuickPlotter(VisualizationBase):
    """Quick plotting with minimal syntax"""
    
    def __init__(self, data: pd.DataFrame, theme: str = 'default'):
        super().__init__(data, theme)
        self._style_config = {}
        self._apply_theme()
    
    def detect_plot_type(self, x: str, y: Optional[str]) -> str:
        """Automatically detect appropriate plot type"""
        if y is None:
            if self._data[x].dtype in [np.number]:
                return 'hist'
            else:
                return 'bar'
        else:
            if self._data[x].dtype in [np.number] and self._data[y].dtype in [np.number]:
                return 'scatter'
            else:
                return 'bar'
    
    def quick_plot(self, x: str, y: Optional[str] = None, 
                   kind: str = 'auto', 
                   color: str = 'steelblue',
                   title: Optional[str] = None,
                   figsize: tuple = (10, 6),
                   **kwargs):
        """Create plots with minimal syntax"""
        plt.figure(figsize=figsize)
        
        if kind == 'auto':
            kind = self.detect_plot_type(x, y)
        
        # Create plot based on type
        if kind == 'scatter' and y:
            plt.scatter(self._data[x], self._data[y], alpha=0.6, color=color, **kwargs)
            plt.xlabel(x, fontsize=12)
            plt.ylabel(y, fontsize=12)
            
        elif kind == 'hist':
            plt.hist(self._data[x], bins=30, color=color, edgecolor='black', alpha=0.7, **kwargs)
            plt.xlabel(x, fontsize=12)
            plt.ylabel('Frequency', fontsize=12)
        
        # Add title
        if title:
            plt.title(title, fontsize=16, fontweight='bold', pad=20)
        else:
            plt.title(f'{kind.capitalize()} Plot: {x}' + (f' vs {y}' if y else ''), 
                     fontsize=16, fontweight='bold', pad=20)
        
        plt.grid(alpha=0.3)
        plt.tight_layout()
        plt.show()
    
    def render(self):
        """Implementation of abstract method"""
        print("Use quick_plot() method to render specific plots")
    
    def __repr__(self):
        return f"QuickPlotter(rows={len(self._data)}, theme='{self._theme}')"
