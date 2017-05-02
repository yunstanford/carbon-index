import fnmatch
import re


def expand_braces(orig):
    """
    Brace expanding patch for python3 borrowed from:
    https://bugs.python.org/issue9584
    """
    r = r'.*(\{.+?[^\\]\})'
    p = re.compile(r)

    s = orig[:]
    res = list()

    m = p.search(s)
    if m is not None:
        sub = m.group(1)
        open_brace = s.find(sub)
        close_brace = open_brace + len(sub) - 1
        if sub.find(',') != -1:
            for pat in sub.strip('{}').split(','):
                res.extend(
                  expand_braces(s[:open_brace] + pat + s[close_brace + 1:])
                )
        else:
            res.extend(
              expand_braces(s[:open_brace] + sub.replace('}', '\\}') + s[close_brace + 1:])
            )
    else:
        res.append(s.replace('\\}', '}'))

    return list(set(res))
