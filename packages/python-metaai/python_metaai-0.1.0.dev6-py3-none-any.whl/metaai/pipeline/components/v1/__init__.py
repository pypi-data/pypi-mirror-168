from typing import Any
from kfp.dsl import ContainerOp
from kfp.components.structures import TaskSpec
# from kfp

from kubernetes.client import V1EnvVar
from .. import constants


def set_required_env_in_op_from_workflow(op: Any):
    if isinstance(op, ContainerOp):
        op.container.add_env_variable(
            V1EnvVar(name="METAAI_USER_ID", value=constants.METAAI_USER_INFO_PLACEHOLDER)
        )
        op.container.add_env_variable(
            V1EnvVar(
                name="MLMODELS_ENDPOINT",
                value=constants.METAAI_MLMODELS_ENDPOINT_PLACEHOLDER,
            )
        )
        op.container.add_env_variable(
            V1EnvVar(
                name="DATASETS_ENDPOINT",
                value=constants.METAAI_MLDATASETS_ENDPOINT_PLACEHOLDER,
            )
        )
    elif isinstance(op, TaskSpec):
        env_mapping = {
            "METAAI_USER_ID": constants.METAAI_USER_INFO_PLACEHOLDER,
            "MLMODELS_ENDPOINT": constants.METAAI_MLMODELS_ENDPOINT_PLACEHOLDER,
            "DATASETS_ENDPOINT": constants.METAAI_MLDATASETS_ENDPOINT_PLACEHOLDER
        }
        op.component_ref.spec.implementation.container.env = env_mapping

    return op
