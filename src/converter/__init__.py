# import os

# __all__ = []
# dirname = os.path.dirname(os.path.abspath(__file__))

# for f in os.listdir(dirname):
#     if f != "__init__.py" and os.path.isfile("%s/%s" % (dirname, f)) and f[-3:] == ".py":
#         __all__.append(f[:-3])
#         globals().update(vars(f))


import os
import importlib

package_path = os.path.dirname(__file__)

__all__ = []
for module_file in os.listdir(package_path):
    if module_file.endswith('.py') and module_file != '__init__.py':
        module_name = module_file[:-3]
        module = importlib.import_module('.' + module_name, package=__name__)

        symbols = [name for name in module.__dict__ if not name.startswith('_')]
        globals().update({name: getattr(module, name) for name in symbols})

        if hasattr(module, '__all__'):
            symbols = module.__all__
        else:
            symbols = [name for name in module.__dict__ if not name.startswith('_')]

        __all__ += symbols