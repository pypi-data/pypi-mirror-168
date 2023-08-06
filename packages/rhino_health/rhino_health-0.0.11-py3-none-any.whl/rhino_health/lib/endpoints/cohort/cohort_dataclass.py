from typing import Any, Optional

from pydantic import Field
from typing_extensions import Annotated, Literal

from rhino_health.lib.dataclass import RhinoBaseModel
from rhino_health.lib.endpoints.endpoint import RESULT_DATACLASS_EXTRA


class BaseCohort(RhinoBaseModel):
    """
    @autoapi False
    Used for both creating a cohort as well as returning a cohort
    """

    name: str
    """
    @autoapi True The name of the Cohort
    """
    description: str
    """
    @autoapi True The description of the Cohort
    """
    base_version_uid: Optional[str]
    """
    @autoapi True The original Cohort this Cohort is a new version of, if applicable
    """
    project_uid: Annotated[str, Field(alias="project")]
    """
    @autoapi True The unique ID of the Project this Cohort belongs to.
    """
    _project: Any = None
    workgroup_uid: Annotated[str, Field(alias="workgroup")]
    """
    @autoapi True The unique ID of the Workgroup this Cohort belongs to
    """
    data_schema_uid: Annotated[str, Field(alias="data_schema")]
    """
    @autoapi True The unique ID of the DataSchema this Cohort follows
    """

    @property
    def project(self):
        """
        @autoapi True

        Get the project of this Cohort

        .. warning:: Be careful when calling this for newly created objects.
            The project associated with the PROJECT_UID must already exist on the platform.

        .. warning:: The result of this function is cached.
            Be careful calling this function after making changes to the project

        Returns
        -------
        project: Project
            A DataClass representing the Project of the user's primary workgroup

        See Also
        --------
        rhino_health.lib.endpoints.project.project_dataclass : Project Dataclass
        """
        if self._project:
            return self._project
        if self.project_uid:
            self._project = self.session.project.get_projects([self.project_uid])[0]
            return self._project
        else:
            return None

    def create_args(self):
        return self.dict(
            by_alias=True,
            include={
                "name",
                "description",
                "base_version_uid",
                "project_uid",
                "workgroup_uid",
                "data_schema_uid",
            },
        )


class CohortCreateInput(BaseCohort):
    """
    Input arguments for adding a new cohort
    """

    csv_filesystem_location: str
    """@autoapi True The location the cohort data is located on-prem. The file should be a CSV."""
    method: Literal["DICOM", "filesystem"]
    """@autoapi True What source are we importing imaging data from. Either a DICOM server, or the local file system"""
    is_data_deidentified: Optional[bool] = False
    """@autoapi True Is the data already deidentified?"""

    image_dicom_server: Optional[str]
    """@autoapi True The DICOM Server URL to import DICOM images from"""
    image_filesystem_location: Optional[str]
    """@autoapi True The on-prem Location to import DICOM images from"""

    file_base_path: Optional[str]
    """@autoapi True The location of non DICOM files listed in the cohort data CSV on-prem"""
    sync: Optional[bool] = True
    """@autoapi True Should we perform this import request synchronously."""

    def import_args(self):
        return self.dict(
            by_alias=True,
            include={
                "csv_filesystem_location",
                "method",
                "is_data_deidentified",
                "image_dicom_server",
                "image_filesystem_location",
                "file_base_path",
                "sync",
            },
        )


class Cohort(BaseCohort, extra=RESULT_DATACLASS_EXTRA):
    """
    @autoapi False
    """

    uid: str
    """
    @autoapi True The unique ID of the Cohort
    """
    version: Optional[int] = 0
    """
    @autoapi True Which revision this Cohort is
    """
    created_at: str
    """
    @autoapi True When this Cohort was added
    """
    num_cases: int
    """
    @autoapi True The number of cases in the cohort
    """
    cohort_info: Optional[dict]
    """
    @autoapi True Sanitized metadata information about the cohort.
    """
    import_status: str
    """
    @autoapi True The import status of the cohort
    """
    data_schema_info: dict
    """
    @autoapi True Metadata about the DataSchema for this cohort.
    """


class FutureCohort(Cohort):
    """
    @autoapi True
    @objname Cohort
    """

    _workgroup: Any = None
    _data_schema: Any = None

    def create(self):
        if self._persisted:
            raise RuntimeError("Cohort has already been created")
        created_cohort = self.session.cohort.create_cohort(self)
        return created_cohort

    def get_metric(self, metric_configuration):
        """
        Queries on-prem and returns the result based on the METRIC_CONFIGURATION for this cohort.

        See Also
        --------
        rhino_health.lib.endpoints.cohort.cohort_endpoints.CohortEndpoints.get_cohort_metric : Full documentation
        """
        """
        Then Cloud API use gRPC -> on-prem where the cohort raw data exists
        On on-prem we will run the sklearn metric function with the provided arguments on the raw cohort data
        on-prem will perform k-anonymization, and return data to Cloud API
        # TODO: How we support multiple instance
        # TODO: Way to exclude internal docs from autoapi
        """
        return self.session.cohort.get_cohort_metric(self.uid, metric_configuration)

    # TODO: No existing endpoint for this
    # @property
    # def workgroup(self):
    #     raise NotImplementedError
    #     if self._workgroup:
    #         return self._workgroup
    #     if self.workgroup_uid:
    #         self._workgroup = self.session.workgroup.get_workgroups([self.workgroup_uid])[0]
    #         return self._workgroup
    #     else:
    #         return None
