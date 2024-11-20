from typing import List, Dict
import json
from json.decoder import JSONDecodeError

from django.utils.html import strip_tags
from django.db import connection
from django.db import transaction

from f5.helpers.Exception import CustomException
from f5.helpers.Database import Database as DBHelper


class Configuration:

    # Table: configuration



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def get(id: int) -> dict:
        c = connection.cursor()

        try:
            c.execute("SELECT id, config_type, value FROM configuration WHERE id = %s", [
                id
            ])

            o = DBHelper.asDict(c)[0]
            if "value" in o:
                try:
                    o["value"] = json.loads(o["value"])
                except JSONDecodeError:
                    o["value"] = []

            return o
        except IndexError:
            raise CustomException(status=400, payload={"database": "Non existent configuration"})
        except Exception as e:
            raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()



    @staticmethod
    def delete(id: int) -> None:
        c = connection.cursor()

        try:
            c.execute("DELETE FROM configuration WHERE id = %s", [id]) # foreign keys' on cascade rules will clean the linked items on db.
        except Exception as e:
            raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()



    @staticmethod
    def modify(id: int, config_type: str, value: str) -> None:
        c = connection.cursor()

        try:
            with transaction.atomic():
                c.execute("UPDATE configuration SET config_type=%s, value=%s WHERE id = %s", [
                    config_type,
                    strip_tags(
                        json.dumps(value)
                    ),
                    id
                ])
                return c.lastrowid

        except Exception as e:
            raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()



    @staticmethod
    def list(configType: list = None) -> List[Dict]:
        configType = configType or []
        query = "SELECT id, config_type, value FROM configuration"
        c = connection.cursor()

        try:
            if configType:
                queryWhere = " WHERE "
                for t in configType:
                    queryWhere += "config_type = %s OR "
                query += queryWhere[:-4]

            c.execute(query, configType)
            out = DBHelper.asDict(c)
            for o in out:
                if "value" in o:
                    try:
                        o["value"] = json.loads(o["value"])
                    except JSONDecodeError:
                        o["value"] = []

            return out
        except Exception as e:
            raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()



    @staticmethod
    def add(config_type: str, value: str) -> int:
        c = connection.cursor()

        try:
            with transaction.atomic():
                c.execute("INSERT INTO configuration (config_type, value) VALUES (%s, %s)", [
                    config_type,
                    strip_tags(
                        json.dumps(value)
                    )
                ])
                return c.lastrowid

        except Exception as e:
            raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()
