import deeplake
import warnings

warnings.warn(
    "Hub is deprecated. Use Deep Lake instead:\n!pip install deelplake\nimport deeplake",
    DeprecationWarning,
    stacklevel=2,
)
globals().update(deeplake.__dict__)  # Forgive me
