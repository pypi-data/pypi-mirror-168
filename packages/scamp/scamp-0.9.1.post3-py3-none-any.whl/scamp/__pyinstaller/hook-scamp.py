from PyInstaller.utils.hooks import collect_dynamic_libs
from PyInstaller.compat import is_win, is_darwin

if is_win:
    scamp_libs = [lib_info for lib_info in collect_dynamic_libs("scamp")
                  if ".dll" in lib_info[0]]
elif is_darwin:
    scamp_libs = [lib_info for lib_info in collect_dynamic_libs("scamp")
                  if ".dylib" in lib_info[0]]
else:
    scamp_libs = []

binaries = scamp_libs
