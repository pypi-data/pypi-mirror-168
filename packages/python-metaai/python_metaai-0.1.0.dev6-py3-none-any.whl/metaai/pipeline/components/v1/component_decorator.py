from typing import *
import functools

from kfp.components import create_component_from_func
# NOTE: use kfp builtin func instead of this
# from metaai.pipeline.components.hack import create_component_from_func
from ..settings import KFP_DISABLE_CACHE_ANNOTATIONS, DEFAULT_BASE_PYTHON_IMAGE


# from kfp.v2.components.component_decorator import component
# see kfp.v2.components.component_decorator component
def component(
        func: Optional[Callable] = None,
        *,
        enable_cache: Optional[bool] = True,
        output_component_file: Optional[str] = None,
        base_image: Optional[str] = DEFAULT_BASE_PYTHON_IMAGE,
        packages_to_install: List[str] = None,
        # image_pull_policy: Optional[str] = None,
        annotations: Optional[Mapping[str, str]] = None,
):
    if not annotations:
        annotations = {}

    if not enable_cache:
        annotations.update(KFP_DISABLE_CACHE_ANNOTATIONS)

    if func is None:
        return functools.partial(
            component,
            # enable_cache=enable_cache,
            base_image=base_image,
            packages_to_install=packages_to_install,
            output_component_file=output_component_file,
            # image_pull_policy=image_pull_policy,
            annotations=annotations,
        )

    return create_component_from_func(
        func,
        # enable_cache=enable_cache,
        output_component_file=output_component_file,
        base_image=base_image,
        packages_to_install=packages_to_install,
        # image_pull_policy=image_pull_policy,
        annotations=annotations,
    )
