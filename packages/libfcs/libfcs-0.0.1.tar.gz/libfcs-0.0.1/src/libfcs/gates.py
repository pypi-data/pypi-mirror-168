"""
Convenience gate functions
"""
import numpy as np

import _libfcs_ext

def polygon_gate(events: np.ndarray, polygon: np.ndarray) -> np.ndarray:
    return _libfcs_ext.polygon_gate(events, polygon)