from __future__ import annotations
from typing import List

from f5.models.Permission.repository.IdentityGroup import IdentityGroup as Repository

from f5.helpers.Misc import Misc


class IdentityGroup:
    def __init__(self, id: int = 0, identityGroupIdentifier: str = "", *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.id: int = int(id)
        self.name: str = ""
        self.identity_group_identifier: str = identityGroupIdentifier

        self.__load()



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def repr(self):
        return vars(self)



    def modify(self, data: dict) -> None:
        try:
            Repository.modify(self.id, data)

            for k, v in Misc.toDict(data).items():
                setattr(self, k, v)
        except Exception as e:
            raise e



    def delete(self) -> None:
        try:
            Repository.delete(self.id)
            del self
        except Exception as e:
            raise e



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def list() -> List[IdentityGroup]:
        identityGroups = []

        try:
            for ig in Repository.list():
                identityGroups.append(
                    IdentityGroup(id=ig["id"])
                )

            return identityGroups
        except Exception as e:
            raise e



    @staticmethod
    def add(data: dict) -> None:
        try:
            Repository.add(data)
        except Exception as e:
            raise e



    ####################################################################################################################
    # Private methods
    ####################################################################################################################

    def __load(self) -> None:
        try:
            info = Repository.get(self.id, self.identity_group_identifier)

            # Set attributes.
            for k, v in info.items():
                setattr(self, k, v)
        except Exception as e:
            raise e
