from __future__ import annotations
from typing import List

from f5.models.Permission.Privilege import Privilege

from f5.models.Permission.repository.Workflow import Workflow as Repository
from f5.models.Permission.repository.WorkflowPrivilege import WorkflowPrivilege as WorkflowPrivilegeRepository

from f5.helpers.Misc import Misc


class Workflow:
    def __init__(self, id: int = 0, workflow: str = "", *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.id: int = int(id)
        self.workflow: str = workflow
        self.description: str = ""

        self.privileges: List[Privilege] = []

        self.__load()



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def repr(self):
        return Misc.deepRepr(self)



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def list(selectWorkflow: list = None) -> List[Workflow]:
        selectWorkflow = selectWorkflow or []
        workflows = []

        try:
            for w in Repository.list(selectWorkflows=selectWorkflow):
                workflows.append(
                    Workflow(id=w["id"])
                )

            return workflows
        except Exception as e:
            raise e



    ####################################################################################################################
    # Private methods
    ####################################################################################################################

    def __load(self) -> None:
        try:
            info = Repository.get(id=self.id, workflow=self.workflow)

            for privilegeId in WorkflowPrivilegeRepository.workflowPrivileges(workflowId=self.id):
                self.privileges.append(
                    Privilege(privilegeId)
                )

            # Set attributes.
            for k, v in info.items():
                setattr(self, k, v)
        except Exception as e:
            raise e
