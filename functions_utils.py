
from dateutil.parser import parse
from inspect import currentframe, getframeinfo

def is_date(string, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try: 
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False


def reporting():
    caller = currentframe().f_back
    func_name = getframeinfo(caller)[2]
    caller = caller.f_back
    from pprint import pprint
    func = caller.f_locals.get(
            func_name, caller.f_globals.get(
                func_name
        )
    )

    return func

