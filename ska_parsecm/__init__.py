# Licensed under a 3-clause BSD style license - see LICENSE.rst
import os
import warnings

message_warn = (
    "\n"
    "The ska_parsecm package is no longer supported and is replaced\n"
    "by parse_cm. Please update your code accordingly.\n"
)
message_error = (
    "\n"
    "To temporarily continue using this package set the environment variable\n"
    "SKA_ALLOW_DISCONTINUED_PACKAGES=1"
)

if os.environ.get("SKA_ALLOW_DISCONTINUED_PACKAGES") == "1":
    warnings.warn(message_warn, FutureWarning)
else:
    raise RuntimeError(message_warn + message_error)

import ska_helpers

from .ParseCM import *  # noqa

__version__ = ska_helpers.get_version("ska_parsecm")
