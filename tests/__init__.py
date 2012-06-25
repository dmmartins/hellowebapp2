import os
__all__ = [name for name, ext in [os.path.splitext(file) for file in os.listdir(os.path.dirname(__file__))] if name.startswith('test')]

