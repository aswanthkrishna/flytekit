import asyncio
import subprocess
from collections import OrderedDict
from shutil import which
from unittest.mock import MagicMock

import grpc
import pytest
from flyteidl.admin.agent_pb2 import PERMANENT_FAILURE, RUNNING, SUCCEEDED
from flytekitplugins.skypilot import MMCloudConfig, SkyPilotTask
from flytekitplugins.skypilot.utils import async_check_output, flyte_to_mmcloud_resources

from flytekit import Resources, task, workflow
from flytekit.configuration import DefaultImages, ImageConfig, SerializationSettings
from flytekit.extend import get_serializable
from flytekit.extend.backend.base_agent import AgentRegistry

float_missing = which("float") is None


task_config = MMCloudConfig(submit_extra="--migratePolicy [enable=true]")
requests = Resources(cpu="2", mem="4Gi")
limits = Resources(cpu="4")
container_image = DefaultImages.default_image()
environment = {"KEY": "value"}

@task(
    task_config=task_config,
    requests=requests,
    limits=limits,
    container_image=container_image,
    environment=environment,
)
def say_hello(name: str) -> str:
    return f"Hello, {name}."

assert say_hello.task_config == task_config
assert say_hello.task_type == "skypilot_task"
assert isinstance(say_hello, SkyPilotTask)

serialization_settings = SerializationSettings(image_config=ImageConfig())
task_spec = get_serializable(OrderedDict(), serialization_settings, say_hello)
template = task_spec.template
container = template.container

assert template.custom == {"submit_extra": "--migratePolicy [enable=true]", "resources": ["2", "4", "4", None]}
assert container.image == container_image
assert container.env == environment

@workflow
def wf():
    print(say_hello(name="Alice"))

if __name__ == "__main__":
    wf()