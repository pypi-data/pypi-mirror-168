import logging
import time

import pandas

logger = logging.getLogger(__name__)


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()

        if len(args) <= 1 or type(args[1]) == pandas.core.frame.DataFrame:
            logger.info("[START] %s()" % (method.__qualname__))
        else:
            logger.info("[START]  %s(%s)   " % (method.__qualname__, args[1]))

        result = method(*args, **kw)
        te = time.time()
        logger.debug(
            "[ END ] [%.1f ms] %s() " % ((te - ts) * 1000), method.__qualname__
        )
        return result

    return timed


tab_count_info = [0]


def timeit_info(method):
    global tab_count_info

    def timed(*args, **kw):
        ts = time.time()
        indent = " |  " * tab_count_info[0]
        args_str = []
        for arg in args:
            args_str.append(str(arg))

        fc_name = "%s(%s)" % (
            method.__qualname__,
            ", ".join(
                [a for a in args_str if args_str.index(a) != 0]  ## +
                ##             ["%s = %s" % (a, str(b)) for a,b in kw.items()]
            ),
        )

        logger.info(indent + "[START] %s" % (fc_name))
        tab_count_info[0] += 1
        result = method(*args, **kw)
        tab_count_info[0] -= 1
        te = time.time()
        logger.info(indent + "[ END ] [%7.1fms] %s" % ((te - ts) * 1000, fc_name))
        return result

    return timed


tab_count_debug = [0]


def timeit_debug(method):
    global tab_count_debug

    def timed(*args, **kw):
        ts = time.time()
        indent = " |  " * tab_count_debug[0]
        join_str = []
        args_str = []
        for arg in args:
            args_str.append(str(arg))

        fc_name = "%s(%s)" % (
            method.__qualname__,
            ", ".join(
                [a for a in args_str if args_str.index(a) != 0]  ## +
                ##             ["%s = %s" % (a, str(b)) for a,b in kw.items()]
            ),
        )
        # [str(a) for a in args if args.index(a) !=0 ]
        # ))

        logger.debug(indent + "[START] %s" % (fc_name))
        tab_count_debug[0] += 1
        result = method(*args, **kw)
        tab_count_debug[0] -= 1
        te = time.time()
        logger.debug(indent + "[ END ] [%7.1fms] %s" % ((te - ts) * 1000, fc_name))

        # if len(args) <=1 or type(args[1]) == pandas.core.frame.DataFrame:
        #     logger.info(indent+"[ END ] [%7.1fms] %s()" % ((te - ts) * 1000,method.__qualname__))
        # else :
        #     logger.info(indent+"[ END ] [%7.1fms] %s(%s)" % ((te - ts) * 1000,method.__qualname__,args[1]))
        return result

    return timed
