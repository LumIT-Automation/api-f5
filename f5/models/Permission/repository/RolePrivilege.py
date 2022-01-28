from django.db import connection

from f5.helpers.Log import Log
from f5.helpers.Exception import CustomException
from f5.helpers.Database import Database as DBHelper


class RolePrivilege:

    # Table: role_privilege

    #   `id_role` int(11) NOT NULL,
    #   `id_privilege` int(11) NOT NULL KEY
    #
    #   PRIMARY KEY (`id_role`,`id_privilege`)
    #
    #   CONSTRAINT `rp_privilege` FOREIGN KEY (`id_privilege`) REFERENCES `privilege` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
    #   CONSTRAINT `rp_role` FOREIGN KEY (`id_role`) REFERENCES `role` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

    pass
