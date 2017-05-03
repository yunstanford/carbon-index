import fnmatch
import os.path
import re


EXPAND_BRACES_RE = re.compile(r'.*(\{.*?[^\\]?\})')


def expand_braces(s):
    """
      Brace expanding patch for python3 borrowed from:
      https://bugs.python.org/issue9584
    """
    res = list()

    # Used instead of s.strip('{}') because strip is greedy.
    # We want to remove only ONE leading { and ONE trailing }, if both exist
    def remove_outer_braces(s):
        if s[0]== '{' and s[-1]=='}':
            return s[1:-1]
        return s

    m = EXPAND_BRACES_RE.search(s)
    if m is not None:
        sub = m.group(1)
        open_brace, close_brace = m.span(1)
        if ',' in sub:
            for pat in sub.strip('{}').split(','):
                res.extend(expand_braces(s[:open_brace] + pat + s[close_brace:]))
        else:
            res.extend(expand_braces(s[:open_brace] + remove_outer_braces(sub) + s[close_brace:]))
    else:
        res.append(s.replace('\\}', '}'))

    return list(set(res))
