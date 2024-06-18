from __future__ import annotations
from typing import List

from f5.models.Permission.Privilege import Privilege

from f5.models.Permission.repository.Workflow import Workflow as Repository
from f5.models.Permission.repository.WorkflowPrivilege import WorkflowPrivilege as WorkflowPrivilegeRepository

from f5.helpers.Misc import Misc


class Workflow:
    def __init__(self, id: int = 0, workflow: str = "", loadPrivilege: bool = True, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.id: int = int(id)
        self.workflow: str = workflow
        self.description: str = ""

        self.privileges: List[Privilege] = []

        self.__load(loadPrivilege=loadPrivilege)



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def repr(self):
        return Misc.deepRepr(self)



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def list(loadPrivilege: bool = True) -> List[Workflow]:
        roles = []

        try:
            for role in Repository.list():
                roles.append(
                    Workflow(id=role["id"], loadPrivilege=loadPrivilege)
                )

            return roles
        except Exception as e:
            raise e



    ####################################################################################################################
    # Private methods
    ####################################################################################################################

    def __load(self, loadPrivilege: bool = True) -> None:
        try:
            info = Repository.get(id=self.id, workflow=self.workflow)

            if loadPrivilege:
                for privilegeId in WorkflowPrivilegeRepository.workflowPrivileges(workflowId=self.id):
                    self.privileges.append(
                        Privilege(privilegeId)
                    )
            else:
                del self.privileges

            # Set attributes.
            for k, v in info.items():
                setattr(self, k, v)
        except Exception as e:
            raise e
