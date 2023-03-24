import json
from json.decoder import JSONDecodeError

from django.utils.html import strip_tags
from django.db import connection

from f5.helpers.Exception import CustomException
from f5.helpers.Database import Database as DBHelper
from f5.helpers.Log import Log


class Configuration:

    # Table: configuration

    #   `id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    #   `config_type` varchar(255) DEFAULT NULL,
    #   `configuration` text DEFAULT NULL



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def get(configType: str) -> dict:
        c = connection.cursor()

        try:
            c.execute("SELECT id, config_type, configuration FROM configuration WHERE config_type = %s", [
                configType
            ])

            o = DBHelper.asDict(c)[0]
            if "configuration" in o:
                try:
                    o["configuration"] = json.loads(o["configuration"])
                except JSONDecodeError:
                    o["configuration"] = []

            return o
        except IndexError:
            raise CustomException(status=400, payload={"database": "non existent configuration type"})
        except Exception as e:
            raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()



    @staticmethod
    def modify(id: int, configuration: dict) -> None:
        c = connection.cursor()

        if not configuration:
            configuration = []

        try:
            c.execute("UPDATE configuration SET configuration=%s WHERE id=%s", [
                strip_tags(
                    json.dumps(configuration)
                ),
                id
            ])
        except Exception as e:
            raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()
