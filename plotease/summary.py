import pandas as pd
import numpy as np
# Assuming VisualizationBase is correctly imported from .visualization
from .visualization import VisualizationBase 
from typing import Optional, List, Dict 

class SummaryGenerator(VisualizationBase):
    """
    Generates tabular data summaries (mean, median, missing, etc.).
    Inherits from VisualizationBase.
    """
    
    # FIX: Add 'theme' to the __init__ method signature.
    def __init__(self, data: pd.DataFrame, theme: str = 'default'): 
        """
        Initializes the SummaryGenerator.
        
        Args:
            data: The pandas DataFrame.
            theme: The visual theme string (passed to the base class).
        """
        # FIX: Pass both data and theme to the parent (VisualizationBase) constructor.
        # This correctly handles the three arguments (self, data, theme).
        super().__init__(data, theme) 
    
    def tabular_summary(self, style: str = 'full') -> pd.DataFrame:
        """
        Generates a comprehensive statistical summary of the data.
        """
        df = self._data
        
        # Helper function to get summary stats for numeric columns
        def get_numeric_summary(data: pd.DataFrame) -> pd.DataFrame:
            stats = data.describe(include=[np.number]).T
            stats['missing'] = data.isnull().sum()
            stats['% missing'] = (stats['missing'] / len(data)) * 100
            stats['skew'] = data.skew(numeric_only=True)
            stats['kurtosis'] = data.kurtosis(numeric_only=True)
            return stats[['count', 'missing', '% missing', 'mean', 'std', 'min', 'max', 'skew', 'kurtosis']]

        # Helper function to get summary stats for categorical columns
        def get_categorical_summary(data: pd.DataFrame) -> pd.DataFrame:
            stats = pd.DataFrame(data.dtypes, columns=['DType'])
            stats['count'] = data.count()
            stats['missing'] = data.isnull().sum()
            stats['% missing'] = (stats['missing'] / len(data)) * 100
            stats['unique'] = data.nunique()
            stats['top_value'] = data.mode().iloc[0]
            stats['top_freq'] = data.apply(lambda x: x.value_counts().max())
            return stats[stats['DType'].astype(str).isin(['object', 'category'])]

        if style == 'numeric':
            return get_numeric_summary(df)
        elif style == 'categorical':
            return get_categorical_summary(df)
        elif style == 'full':
            numeric_df = get_numeric_summary(df)
            categorical_df = get_categorical_summary(df)
            
            # Use 'outer' join to keep all columns, filling NaNs where necessary
            full_summary = pd.concat([numeric_df, categorical_df], axis=0, sort=True)
            return full_summary.sort_index()
        else:
            raise ValueError(f"Unknown style '{style}'. Choose from 'full', 'numeric', or 'categorical'.")

    # Implementation of the abstract method (Polymorphism)
    def render(self):
        """
        Implementation of the abstract method from VisualizationBase.
        Renders the full tabular summary (prints it to the console).
        """
        print("\n📊 Comprehensive Data Summary:")
        print("=" * 30)
        # Delegate the actual work to the tabular_summary method
        summary_df = self.tabular_summary(style='full')
        print(summary_df.to_string())
        print("=" * 30)
