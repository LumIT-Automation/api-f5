import collections


class Misc:
    @staticmethod
    def toDict(layer):
        r = layer
        if isinstance(layer, collections.OrderedDict):
            r = dict(layer)

        try:
            for key, value in r.items():
                r[key] = Misc.toDict(value)
        except AttributeError:
            pass

        return r



    @staticmethod
    def deepRepr(o, r, fatherIsList: bool = False, fatherName: str = "") -> None: # r
        try:
            z = dict()

            v = vars(o)
            if isinstance(v, dict):
                for key, val in v.items():
                    if isinstance(val, str) or isinstance(val, int):
                        if fatherIsList:
                            z[str(key)] = str(val)
                        else:
                            r[str(key)] = str(val)

                    if isinstance(val, list):
                        for j in val:
                            Misc.deepRepr(j, r, fatherIsList=True, fatherName=key)

            if fatherIsList and fatherName:
                if fatherName not in r:
                    r[fatherName] = list()
                r[fatherName].append(z)
        except Exception as e:
            raise e
