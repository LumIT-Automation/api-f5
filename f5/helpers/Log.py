import logging
import traceback


class Log:
    @staticmethod
    def log(o: any, title: str = "") -> None:
        # Sends input logs to the "f5" logger (settings).
        log = logging.getLogger("django")
        if title:
            if title == "_":
                for j in range(80):
                    title = title + "_"
            log.debug(title)

        log.debug(o)

        if title:
            log.debug(title)


    @staticmethod
    def dump(o: any) -> None:
        import re
        log = logging.getLogger("django")

        oOut = dict()
        oVars = vars(o)
        oDir = dir(o)

        for i, v in enumerate(oDir):
            if v in oVars:
                oOut[v] = oVars[v]
            else:
                if not re.search("^__(.*)__$", str(v)):
                    oOut[v] = getattr(o, v)

        log.debug(oOut)



    @staticmethod
    def logException(e: Exception) -> None:
        # Logs the stack trace information and the raw output if any.
        Log.log(traceback.format_exc(), 'Error')

        try:
            Log.log(e.raw, 'Raw f5 data')
        except Exception:
            pass



    @staticmethod
    def actionLog(o: any, user: dict = None) -> None:
        # Sends input logs to the "f5" logger (settings).
        user = {} if user is None else user

        log = logging.getLogger("django")
        try:
            if "username" in user:
                log.debug("["+user['username']+"] "+o)
            else:
                log.debug(o)
        except Exception:
            pass
