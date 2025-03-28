import os
import importlib.util
import warnings
from pathlib import Path

def _load_driver(name):
    """Load driver from either .py or .amatak file"""
    # Try Python version first
    py_path = Path(__file__).parent / f'{name}.py'
    if py_path.exists():
        try:
            spec = importlib.util.spec_from_file_location(
                f'amatak.database.drivers.{name}',
                str(py_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
        except Exception as e:
            warnings.warn(f"Failed to load Python driver {name}: {e}", RuntimeWarning)
    
    # Fall back to Amatak version if Python version not found
    amatak_path = Path(__file__).parent / f'{name}.amatak'
    if amatak_path.exists():
        try:
            from ...loader import load_amatak_module
            return load_amatak_module(str(amatak_path))
        except Exception as e:
            warnings.warn(f"Failed to load Amatak driver {name}: {e}", RuntimeWarning)
    
    return None

# Load drivers
BaseDriver = _load_driver('base_driver') or _load_driver('base_drive')  # Handle typo
SQLiteDriver = _load_driver('sqlite')
PostgresDriver = _load_driver('postgres')

__all__ = []
if BaseDriver is not None:
    __all__.append('BaseDriver')
if SQLiteDriver is not None:
    __all__.append('SQLiteDriver')
if PostgresDriver is not None:
    __all__.append('PostgresDriver')