from typing import Any, Dict, List, cast

from pydantic import Field
from typing_extensions import Annotated, Literal

from rhino_health.lib.dataclass import RhinoBaseModel

# TODO: Actually finish dataclasses and make this usable
from rhino_health.lib.endpoints.endpoint import RESULT_DATACLASS_EXTRA
from rhino_health.lib.endpoints.user.user_dataclass import FutureUser, User


class ProjectCreateInput(RhinoBaseModel):
    """
    Input arguments for adding a new project.
    """

    name: str
    """@autoapi True The name of the Project"""
    description: str
    """@autoapi True The description of the Project"""
    type: Literal["Validation", "Refinement"]
    """@autoapi True The type of the Project"""
    primary_workgroup_uid: Annotated[str, Field(alias="primary_workgroup")]
    """@autoapi True The unique ID of the Project's Primary Workgroup"""


class Project(ProjectCreateInput, extra=RESULT_DATACLASS_EXTRA):
    """
    A Project that exists on the Rhino Health Platform
    """

    uid: str
    """@autoapi True The unique ID of the Project"""
    slack_channel: str
    """@autoapi True Slack Channel URL for communications for the Project"""
    collaborating_workgroups_uids: List[str]
    """@autoapi True A list of unique IDs of the Project's collaborating Workgroups"""
    users: List[User]
    """@autoapi True A list of users in the project"""
    status: Dict
    """@autoapi True The status of the Workgroup"""


class FutureProject(Project):
    """
    @objname Project
    DataClass representing a Project on the Rhino platform.
    """

    users: List[FutureUser]
    _collaborating_workgroups: Any = None

    def collaborating_workgroups(self):
        """
        Get the Collaborating Workgroup DataClass of this Project

        .. warning:: Be careful when calling this for newly created objects.
            The workgroups associated with the COLLABORATING_WORKGROUP_UIDS must already exist on the platform.

        .. warning:: The result of this function is cached.
            Be careful calling this function after making changes to the collaborating workgroups

        Returns
        -------
        collaborating_workgroups: List[Workgroup]
            A List of DataClasses representing the Collaborating Workgroups of the Project

        See Also
        --------
        rhino_health.lib.endpoints.workgroup.workgroup_dataclass : Workgroup Dataclass
        """
        if self._collaborating_workgroups:
            return self._collaborating_workgroups
        if self.collaborating_workgroups_uids:
            self._collaborating_workgroups = self.session.project.get_collaborating_workgroups(
                self.uid
            )
            return self._collaborating_workgroups
        else:
            return []

    def add_collaborator(self, collaborator_or_uid):
        """
        Adds COLLABORATOR_OR_UID as a collaborator to this project

        .. warning:: This feature is under development and the interface may change
        """
        from rhino_health.lib.endpoints.project.project_endpoints import ProjectFutureEndpoints

        from ..workgroup.workgroup_dataclass import Workgroup

        if isinstance(collaborator_or_uid, Workgroup):
            collaborator_or_uid = collaborator_or_uid.uid
        cast(self.session.project, ProjectFutureEndpoints).add_collaborator(
            self.uid, collaborator_or_uid
        )
        self._collaborating_workgroups = None

    def remove_collaborator(self, collaborator_or_uid):
        """
        Removes COLLABORATOR_OR_UID as a collaborator from this project

        .. warning:: This feature is under development and the interface may change
        """
        from rhino_health.lib.endpoints.project.project_endpoints import ProjectFutureEndpoints

        from ..workgroup.workgroup_dataclass import Workgroup

        if isinstance(collaborator_or_uid, Workgroup):
            collaborator_or_uid = collaborator_or_uid.uid
        cast(self.session.project, ProjectFutureEndpoints).remove_collaborator(
            self.uid, collaborator_or_uid
        )
        self._collaborating_workgroups = None

    # Add Schema
    # Local Schema from CSV
