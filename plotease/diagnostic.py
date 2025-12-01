import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 
from typing import Optional, List 
from abc import ABC, abstractmethod
from .visualization import VisualizationBase 

class DiagnosticPlotter(VisualizationBase):
    """
    Handles automatic diagnostic plot generation
    Demonstrates: Inheritance from VisualizationBase
    """
    
    def __init__(self, data: pd.DataFrame, theme: str = 'default'):
        super().__init__(data, theme)
        self._apply_theme()
    
    def create_distributions(self, ax, numeric_cols: List[str]):
        for col in numeric_cols[:3]:
            self._data[col].hist(alpha=0.5, label=col, bins=30, ax=ax, edgecolor='black') 
        ax.set_title('Distribution of Numeric Variables', fontsize=14, fontweight='bold')
        ax.set_xlabel('Value')
        ax.set_ylabel('Frequency')
        ax.legend()
        ax.grid(alpha=0.3)
    
    def create_correlations(self, ax, numeric_cols: List[str]):
        corr = self._data[numeric_cols].corr()
        sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', 
                    center=0, ax=ax, cbar_kws={'shrink': 0.8})
        ax.set_title('Correlation Matrix', fontsize=14, fontweight='bold')
    
    def create_missing_data(self, ax):
        missing = self._data.isnull().sum()
        missing = missing[missing > 0].sort_values(ascending=False)
        
        if len(missing) > 0:
            missing.plot(kind='barh', ax=ax, color='coral')
            ax.set_title('Missing Values by Column', fontsize=14, fontweight='bold')
            ax.set_xlabel('Count')
            ax.set_ylabel('Column')
        else:
            ax.text(0.5, 0.5, 'No Missing Values', ha='center', va='center', fontsize=16)
            ax.set_title('Missing Values Check', fontsize=14, fontweight='bold')
            ax.axis('off')
    
    def create_outliers(self, ax, numeric_cols: List[str]):
        self._data[numeric_cols[:4]].boxplot(ax=ax)
        ax.set_title('Outlier Detection (Boxplots)', fontsize=14, fontweight='bold')
        ax.set_ylabel('Value')
        if len(numeric_cols[:4]) > 0:
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
    
    def autoplot(self, target: Optional[str] = None, max_plots: int = 6):
        numeric_cols = self._data.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = self._data.select_dtypes(include=['object', 'category']).columns.tolist()
        
        plots_created = 0
        n_rows = min(3, (max_plots + 1) // 2)
        fig = plt.figure(figsize=(15, 5 * n_rows))
        
        if numeric_cols and plots_created < max_plots:
            plots_created += 1
            ax = plt.subplot(n_rows, 2, plots_created)
            self.create_distributions(ax, numeric_cols)

        if len(numeric_cols) > 1 and plots_created < max_plots:
            plots_created += 1
            ax = plt.subplot(n_rows, 2, plots_created)
            self.create_correlations(ax, numeric_cols)

        if plots_created < max_plots:
            plots_created += 1
            ax = plt.subplot(n_rows, 2, plots_created)
            self.create_missing_data(ax)

        if target and target in self._data.columns and plots_created < max_plots:
            plots_created += 1
            ax = plt.subplot(n_rows, 2, plots_created)

            if pd.api.types.is_numeric_dtype(self._data[target].dtype):
                self._data[target].hist(bins=30, ax=ax, color='steelblue', edgecolor='black')
                ax.set_xlabel(target)
                ax.set_ylabel('Frequency')
            else:
                self._data[target].value_counts().head(10).plot(
                    kind='bar', ax=ax, color='steelblue'
                )
                ax.set_xlabel(target)
                ax.set_ylabel('Count')
                plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)

            ax.set_title(f'Target Distribution: {target}', fontsize=14, fontweight='bold')

    def render(self):
        """Implements required abstract method from VisualizationBase."""
        print("Rendering diagnostic plots...")
        self.autoplot()
        plt.tight_layout()
        plt.show()
