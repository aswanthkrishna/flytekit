"""
.. currentmodule:: flytekitplugins.mmcloud

This package contains things that are useful when extending Flytekit.

.. autosummary::
   :template: custom.rst
   :toctree: generated/

   MMCloudConfig
   MMCloudTask
   MMCloudAgent
"""

from .agent import SkyPilotAgent
from .task import MMCloudConfig, SkyPilotTask
