## Notes:

#### Using the `hid` & `hidapi` modules in Windows (Python)

If you try and run the script `hid-test.py` and you get import errors such as the following:
```sh
ImportError: Unable to load any of the following

libraries:libhidapi-hidraw.so libhidapi-hidraw.so.0
libhidapi-libusb.so libhidapi-libusb.so.0
libhidapi-iohidmanager.so libhidapi-iohidmanager.so.0
libhidapi.dylib hidapi.dll libhidapi-0.dll
```

Here are some steps that can help fix the issue. 
1. Install `hid` version `1.0.4` instead of the latest:
    1. `pip uninstall hid`
    2. `pip install hid==1.0.4`
    This may help since the latest version of `hid` (as of when I'm writing this) was having issues with communicating with older shared object files.
2. Install `hidapi` (a dependency of `hid`):
    1. Download `hidapi-win.zip` from https://github.com/libusb/hidapi/releases
    2. Depending on your architecture (x86 or x64), place the corresponding files into your Python install path.

For example, on my system (x64), I downloaded & unzipped `hidapi-win.zip`, copied the following files from the `hidapi-win/x64/` directory:
- `hidapi.dll`
- `hidapi.lib`
And pasted them at `C:\Users\...\AppData\Local\Programs\Python\Python39\`.

(It's important to note that placing them in the `Python39\Scripts\` subdirectory did not solve the problem for me.)

You should now be able to run `python` and `import hid` without any issues, meaning `python hidtest.py` should correctly work.

Also, if anyone has managed to properly build the `hid` and `hidapi` library for `C/C++` using `CMake` on Windows, please let me know. I want to make this in C rather than Python -_-