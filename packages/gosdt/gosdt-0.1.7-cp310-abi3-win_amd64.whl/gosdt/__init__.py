

""""""# start delvewheel patch
def _delvewheel_init_patch_0_0_25():
    import os
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'gosdt.libs'))
    if sys.version_info[:2] >= (3, 8) and not os.path.exists(os.path.join(sys.base_prefix, 'conda-meta')) or sys.version_info[:2] >= (3, 10):
        os.add_dll_directory(libs_dir)
    else:
        from ctypes import WinDLL
        with open(os.path.join(libs_dir, '.load-order-gosdt-0.1.7')) as file:
            load_order = file.read().split()
        for lib in load_order:
            WinDLL(os.path.join(libs_dir, lib))


_delvewheel_init_patch_0_0_25()
del _delvewheel_init_patch_0_0_25
# end delvewheel patch

# We're just going to bring these to the front
# This is Tynan guessing what
from gosdt.model.gosdt import GOSDT
from gosdt.model.threshold_guess import get_thresholds