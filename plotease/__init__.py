# 1. Import all primary classes from their new modules 
# The classes are imported relative to the current package ('.')

from .visualization import VisualizationBase
from .plotease import PlotEase
from .diagnostic import DiagnosticPlotter
from .summary import SummaryGenerator
from .model_comp import ModelComparator
from .quick_plotter import QuickPlotter

# The main user-facing facade class
from .plotease import PlotEase              # From plotease.py 

# 2. Define __all__ 
# This explicitly lists all public objects to expose when someone runs 'from plotease import *'
__all__ = [
    "PlotEase",
    "VisualizationBase",
    "SummaryGenerator",
    "DiagnosticPlotter",
    "QuickPlotter",
    "ModelComparator",
]

# 3. Package Version 
__version__ = "0.1.0"
