from flytekit import Resources, task, workflow, Secret
from flytekitplugins.skypilot import MMCloudConfig

@task
def testtask() -> str:
    return "running"

@task(
    task_config=MMCloudConfig(submit_extra="--migratePolicy [enable=true]"),
    requests=Resources(cpu="2", mem="1Gi"),
    limits=Resources(cpu="4", mem="16Gi"),
    secret_requests=[Secret(group='aws', key="AWS_ACCESS_KEY_ID"), Secret(group='aws', key="AWS_SECRET_ACCESS_KEY")]
)
def testSkyPilot(name: str) -> str:
    return f"Hello, {name}."
