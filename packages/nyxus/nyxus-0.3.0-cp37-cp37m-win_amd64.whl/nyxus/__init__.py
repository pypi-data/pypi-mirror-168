

""""""# start delvewheel patch
def _delvewheel_init_patch_0_0_25():
    import os
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'nyxus.libs'))
    if sys.version_info[:2] >= (3, 8) and not os.path.exists(os.path.join(sys.base_prefix, 'conda-meta')) or sys.version_info[:2] >= (3, 10):
        os.add_dll_directory(libs_dir)
    else:
        from ctypes import WinDLL
        with open(os.path.join(libs_dir, '.load-order-nyxus-0.3.0')) as file:
            load_order = file.read().split()
        for lib in load_order:
            WinDLL(os.path.join(libs_dir, lib))


_delvewheel_init_patch_0_0_25()
del _delvewheel_init_patch_0_0_25
# end delvewheel patch

from .nyxus import Nyxus
from .nyxus import Nested
from .functions import gpu_is_available, get_gpu_properties

from . import _version
__version__ = _version.get_versions()['version']
