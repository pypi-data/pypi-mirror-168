# -------------------------------------------------------------------------
# Copyright (c) Switch Automation Pty Ltd. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
"""
Data Ingestion into the Switch Automation
=========================================

Complete package for ingestion data into the Switch Automation Platform.
"""
__all__ = [
    'models',
    'exceptions',
    'tasks',
    'utils',
    'exceptions',
    'SwitchGuideTask'
]

from . import models
from . import exceptions
from . import tasks
from . import exceptions
from . import utils
from .SwitchGuideTask import SwitchGuideTask

__version__ = "0.1.8"
