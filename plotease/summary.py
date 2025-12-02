import pandas as pd
import numpy as np
# Assuming VisualizationBase is in a file like 'visualization.py'
from .visualization import VisualizationBase
from typing import Optional, List, Dict

class SummaryGenerator(VisualizationBase):
    """
    Generates tabular data summaries (mean, median, missing, etc.).
    Inherits from VisualizationBase.
    
    The 'render' method is implemented here to satisfy the
    Abstract Base Class requirement from VisualizationBase.
    """
    
    def __init__(self, data: pd.DataFrame, theme: str = 'default'): 
        """
        Initializes the SummaryGenerator.
        """
        super().__init__(data, theme) 
    
    # === FIX: Implementation of the required abstract method 'render' ===
    def render(self, style: str = 'full') -> pd.DataFrame:
        """
        Implements the abstract 'render' method from VisualizationBase.
        For SummaryGenerator, this method returns the comprehensive
        tabular summary.
        """
        # Call the primary method of this class
        return self.tabular_summary(style=style)
    # ===================================================================

    def tabular_summary(self, style: str = 'full') -> pd.DataFrame:
        """
        Generates a comprehensive statistical summary of the data.
        """
        df = self._data
        
        # Helper function to get summary stats for numeric columns
        def get_numeric_summary(data: pd.DataFrame) -> pd.DataFrame:
            stats = data.describe(include=[np.number], numeric_only=True).T 
            stats['missing'] = data.isnull().sum()
            stats['% missing'] = (stats['missing'] / len(data)) * 100
            stats['skew'] = data.skew(numeric_only=True)
            stats['kurtosis'] = data.kurtosis(numeric_only=True)
            return stats[['count', 'missing', '% missing', 'mean', 'std', 'min', 'max', 'skew', 'kurtosis']]

        # Helper function to get summary stats for categorical columns
        def get_categorical_summary(data: pd.DataFrame) -> pd.DataFrame:
            data_non_numeric = data.select_dtypes(exclude=[np.number, 'datetime'])
            stats = pd.DataFrame(data_non_numeric.dtypes, columns=['DType'])
            stats['count'] = data_non_numeric.count()
            stats['missing'] = data_non_numeric.isnull().sum()
            stats['% missing'] = (stats['missing'] / len(data)) * 100
            stats['unique'] = data_non_numeric.nunique()
            
            if not data_non_numeric.empty:
                stats['top_value'] = data_non_numeric.mode().iloc[0]
                # Safely get the max frequency (mode count)
                stats['top_freq'] = data_non_numeric.apply(lambda x: x.value_counts().max() if not x.empty else 0)
            else:
                stats['top_value'] = np.nan
                stats['top_freq'] = 0

            return stats
        
        # Combine the summaries based on the 'style'
        numeric_df = get_numeric_summary(df)
        categorical_df = get_categorical_summary(df)

        if style == 'full':
            # Align columns for concatenation
            # Add missing columns to categorical summary with NaNs so they can be concatenated
            for col in numeric_df.columns:
                if col not in categorical_df.columns:
                    categorical_df[col] = np.nan
            
            # Reorder columns to match numeric_df before concatenation
            categorical_df = categorical_df.reindex(columns=numeric_df.columns.insert(0, 'DType'), fill_value=np.nan)
            
            # Concatenate and return the combined summary
            full_summary = pd.concat([numeric_df.reset_index(names=['Feature']), 
                                      categorical_df.reset_index(names=['Feature'])], 
                                     ignore_index=True)
            return full_summary.set_index('Feature')

        elif style == 'numeric':
            return numeric_df
        elif style == 'categorical':
            return categorical_df
        else:
            raise ValueError("Style must be 'full', 'numeric', or 'categorical'.")

    # The remaining methods (e.g., __len__) should also be implemented if they are abstract
    # ...
