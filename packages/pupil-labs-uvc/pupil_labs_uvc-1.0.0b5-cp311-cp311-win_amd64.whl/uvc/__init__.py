

""""""# start delvewheel patch
def _delvewheel_init_patch_0_0_25():
    import os
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'pupil_labs_uvc.libs'))
    if sys.version_info[:2] >= (3, 8) and not os.path.exists(os.path.join(sys.base_prefix, 'conda-meta')) or sys.version_info[:2] >= (3, 10):
        os.add_dll_directory(libs_dir)
    else:
        from ctypes import WinDLL
        with open(os.path.join(libs_dir, '.load-order-pupil_labs_uvc-1.0.0b5')) as file:
            load_order = file.read().split()
        for lib in load_order:
            WinDLL(os.path.join(libs_dir, lib))


_delvewheel_init_patch_0_0_25()
del _delvewheel_init_patch_0_0_25
# end delvewheel patch

import logging

try:
    from importlib.metadata import PackageNotFoundError, version
except ImportError:
    from importlib_metadata import PackageNotFoundError, version

try:
    __version__ = version("pupil-labs-uvc")
except PackageNotFoundError:
    # package is not installed
    pass

__all__ = ["__version__"]

logger = logging.getLogger(__name__)

from .uvc_bindings import *
