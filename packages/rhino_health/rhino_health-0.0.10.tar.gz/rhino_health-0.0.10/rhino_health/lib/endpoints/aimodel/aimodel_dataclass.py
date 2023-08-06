import json
from enum import Enum
from typing import Any, List, Optional

from pydantic import Field, root_validator
from typing_extensions import Annotated

from rhino_health.lib.dataclass import RhinoBaseModel
from rhino_health.lib.endpoints.endpoint import RESULT_DATACLASS_EXTRA


class ModelTypes(str, Enum):
    CLARA_TRAIN = "Clara Train"
    GENERALIZED_COMPUTE = "Generalized Compute"
    NVIDIA_FLARE = "NVIDIA FLARE"


class AIModelCreateInput(RhinoBaseModel):
    """
    @autoapi False
    """

    def __init__(self, *args, **kwargs):
        container_image_uri = kwargs.pop("container_image_uri", None)
        super().__init__(*args, **kwargs)
        if container_image_uri:
            self.container_image_uri = container_image_uri

    name: str
    """@autoapi True The name of the AIModel"""
    description: str
    """@autoapi True The description of the AIModel"""
    version: int
    """@autoapi True The version of the AIModel"""
    base_version_uid: Optional[str] = ""
    """@autoapi True The first version of the AIModel"""
    config: Optional[dict] = None
    _project: Any = None
    input_data_schema: str
    """@autoapi True The schema pre-run of the input cohorts"""
    output_data_schema: str
    """@autoapi True The schema post-run of the output cohorts"""
    project_uid: Annotated[str, Field(alias="project")]
    """@autoapi True The AIModel project"""
    model_type: Annotated[str, Field(alias="type")]
    """@autoapi Aimodel types use the ModelTypes enum"""

    @property
    def container_image_uri(self):
        return self.config.get("container_image_uri", None)

    @container_image_uri.setter
    def container_image_uri(self, new_value):
        self.config["container_image_uri"] = new_value

    @property
    def project(self):
        if self._project:
            return self._project
        if self.project_uid:
            self._project = self.session.project.get_projects([self.project_uid])[0]
            return self._project
        else:
            return None


class AIModel(AIModelCreateInput, extra=RESULT_DATACLASS_EXTRA):
    """
    @autoapi True
    """

    uid: str
    """@autoapi True The unique ID of the AIModel"""
    created_at: str
    """@autoapi True When this AIModel was added"""


class AIModelRunInput(RhinoBaseModel):
    """
    @autoapi True
    """

    def __init__(self, *args, **kwargs):
        run_params = kwargs.get("run_params", None)
        if isinstance(run_params, dict):
            kwargs["run_params"] = json.dumps(run_params)
        super().__init__(*args, **kwargs)

    aimodel_uid: str
    """@autoapi True The unique ID of the AIModel"""
    input_cohort_uids: List[str]
    """@autoapi True A list of the input cohort uids"""
    output_cohort_names_suffix: str
    """@autoapi True The suffix given to all output cohorts"""
    run_params: Optional[str] = "{}"
    """@autoapi True The run params code you want to run on the cohorts"""
    timeout_seconds: Optional[int] = 600
    """@autoapi True The time before a timeout is declared for the run"""
    secret_run_params: Optional[str]
    """The secrets for the AI model"""
    sync: Optional[bool] = True
    """@autoapi True If True wait for run to end if False let it run in the background"""

    @root_validator
    def passwords_match(cls, values):
        if values.get("sync", True) and values.get("timeout_seconds", 600) > 600:
            raise ValueError(
                "Timeout seconds cannot be greater than 600 when run in synchronous mode"
            )
        return values


class AIModelTrainInput(RhinoBaseModel):
    """
    @autoapi True
    """

    aimodel_uid: str
    """The unique ID of the AIModel"""
    input_cohort_uids: List[str]
    """A list of the input cohort uids"""
    validation_cohort_uids: List[str]
    """A list of the cohort uids for validation"""
    validation_cohorts_inference_suffix: str
    """The suffix given to all output cohorts"""
    config_fed_server: str
    """The config for the federated server"""
    config_fed_client: str
    """The config for the federated client"""
    secrets_fed_server: Optional[str]
    """The secrets for the federated server"""
    secrets_fed_client: Optional[str]
    """The secrets for the federated client"""
    timeout_seconds: int
    """The time before a timeout is declared for the run"""
