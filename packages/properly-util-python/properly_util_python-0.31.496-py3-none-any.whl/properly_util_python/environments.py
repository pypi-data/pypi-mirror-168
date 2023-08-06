import os

# Stages that consistently exist for all services, with optional inclusion of local
# for callers that want to use a local override in automated tests
CONSISTENT_STAGES = {"staging", "prod"}
CONSISTENT_STAGES_WITH_LOCAL = {"staging", "prod", "local"}


def get_properly_stage_for_resource(
    default_stage: str = "staging", ignore_custom_stages: bool = True, use_local_for_tests: bool = False
) -> str:
    """
    Gets the PROPERLY_STAGE environment variable with configuration for handling different needs.
    With custom stages, some of our resources are deployed with a new instance for the custom stage,
    but many legacy or third party resources continue to only have prod and staging versions.
    In a service that supports custom domains but needs to access an outside managed resource, use default_stage="prod".
    https://prop.atlassian.net/wiki/spaces/TECH/pages/2299953165/HOWTO+Setup+a+BE+service+to+deploy+to+custom+stages#Use-of-PROPERLY_STAGE-setup-to-handle-custom-stages
    default_stage: 
        Set to prod for read only resources.
        Fallback if we cannot get the stage from the environment
    ignore_custom_stages: 
        Should be False for resources that are self managed in the serverless.yml for a service and deployed in each stage.
        When this is true, the only stages that are used are either staging, prod, or local.
    use_local_for_tests: 
        Set to True for resources mocked by moto in automated tests
    """
    env_stage = os.environ.get("PROPERLY_STAGE", default_stage)

    if ignore_custom_stages and use_local_for_tests:
        return env_stage if env_stage in CONSISTENT_STAGES_WITH_LOCAL else default_stage
    elif ignore_custom_stages:
        return env_stage if env_stage in CONSISTENT_STAGES else default_stage
    elif use_local_for_tests:
        return env_stage
    else:
        return env_stage if env_stage != "local" else default_stage
