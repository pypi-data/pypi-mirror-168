import os.path
__dir__ = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0]
data_location = os.path.join(__dir__, "system_verilog")
src = "https://github.com/openhwgroup/cv32e40x"

# Module version
version_str = "0.5.0.post170"
version_tuple = (0, 5, 0, 170)
try:
    from packaging.version import Version as V
    pversion = V("0.5.0.post170")
except ImportError:
    pass

# Data version info
data_version_str = "0.5.0.post28"
data_version_tuple = (0, 5, 0, 28)
try:
    from packaging.version import Version as V
    pdata_version = V("0.5.0.post28")
except ImportError:
    pass
data_git_hash = "a1ca4fc1b69eb9c4f3cd269d160203153d7d51f1"
data_git_describe = "0.5.0-28-ga1ca4fc1"
data_git_msg = """\
commit a1ca4fc1b69eb9c4f3cd269d160203153d7d51f1
Merge: 9acceb8d 1eb62f95
Author: silabs-oysteink <66771756+silabs-oysteink@users.noreply.github.com>
Date:   Thu Sep 22 11:58:21 2022 +0200

    Merge pull request #667 from silabs-oysteink/silabs-oysteink_wfi-wb_valid
    
    Keeping WFI in WB until SLEEP mode is exited

"""

# Tool version info
tool_version_str = "0.0.post142"
tool_version_tuple = (0, 0, 142)
try:
    from packaging.version import Version as V
    ptool_version = V("0.0.post142")
except ImportError:
    pass


def data_file(f):
    """Get absolute path for file inside pythondata_cpu_cv32e40x."""
    fn = os.path.join(data_location, f)
    fn = os.path.abspath(fn)
    if not os.path.exists(fn):
        raise IOError("File {f} doesn't exist in pythondata_cpu_cv32e40x".format(f))
    return fn
