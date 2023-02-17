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
