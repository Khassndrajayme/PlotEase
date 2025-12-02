import pandas as pd
import numpy as np
from .visualization import VisualizationBase
from typing import Optional, List, Dict

class SummaryGenerator(VisualizationBase):
    """
    Generates tabular data summaries (mean, median, missing, etc.).
    Inherits from VisualizationBase.
    """

    def __init__(self, data: pd.DataFrame, theme: str = 'default'):
        """
        Initializes the SummaryGenerator.
        
        Args:
            data: The pandas DataFrame.
            theme: The visual theme string (passed to the base class).
        """
        super().__init__(data, theme)

    def render(self, style: str = 'full') -> pd.DataFrame:
        """
        Implements the abstract 'render' method from VisualizationBase.
        For SummaryGenerator, this method returns the comprehensive
        tabular summary.
        """
        # Call the primary method of this class
        return self.tabular_summary(style=style)
    
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
            
            # Handle empty DataFrame case for mode/top_value
            if not data_non_numeric.empty:
                stats['top_value'] = data_non_numeric.mode().iloc[0]
                # Safely get the max frequency (mode count)
                stats['top_freq'] = data_non_numeric.apply(lambda x: x.value_counts().max() if not x.empty else 0)
            else:
                stats['top_value'] = np.nan
                stats['top_freq'] = 0

            return stats
        
        # === Missing Logic: Combine and Return the Summaries ===
        
        if style == 'numeric':
            return get_numeric_summary(df)
        
        if style == 'categorical':
            return get_categorical_summary(df)
        
        if style == 'full':
            numeric_df = get_numeric_summary(df)
            categorical_df = get_categorical_summary(df)

            # Prepare categorical_df for concatenation by aligning columns
            # DType is only present in categorical summary, so we add the numeric features as NaN
            for col in numeric_df.columns:
                if col not in categorical_df.columns:
                    categorical_df[col] = np.nan
            
            # Reset index to treat feature names as a column for concatenation
            numeric_df = numeric_df.reset_index(names=['Feature'])
            categorical_df = categorical_df.reset_index(names=['Feature'])

            # Concatenate and re-set 'Feature' as the index
            full_summary = pd.concat([numeric_df, categorical_df], ignore_index=True)
            
            # Remove duplicate 'DType' column if it was inadvertently created in numeric_df
            if 'DType' in full_summary.columns and full_summary['DType'].isnull().all():
                 full_summary = full_summary.drop(columns=['DType'])
            
            return full_summary.set_index('Feature')

        raise ValueError("Style must be 'full', 'numeric', or 'categorical'.")
