from libcpp.string cimport string
from libcpp.vector cimport vector
from libcpp.algorithm cimport sort, unique

import re


EXPAND_BRACES_RE = re.compile(r'.*(\{.*?[^\\]?\})')


# Used instead of s.strip('{}') because strip is greedy.
# We want to remove only ONE leading { and ONE trailing }, if both exist
cdef remove_outer_braces(string s):
    if s[0] == '{' and s[s.size() - 1] == '}':
        return s[1:-1].decode()
    return s


cpdef expand_braces(string s):
    """
      Brace expanding patch for python3 borrowed from:
      https://bugs.python.org/issue9584
    """
    cdef vector[string] res
    cdef vector[string] tmp_vec
    cdef string tmp_str

    s = s.decode()
    m = EXPAND_BRACES_RE.search(s)
    if m is not None:
        sub = m.group(1)
        open_brace, close_brace = m.span(1)
        if ',' in sub:
            for pat in sub.strip('{}').split(','):
                tmp_str = s[:open_brace].decode() + pat + s[close_brace:].decode()
                tmp_vec = expand_braces(tmp_str)
                res.insert(res.end(), tmp_vec.begin(), tmp_vec.end())
        else:
            tmp_str = s[:open_brace].decode() + remove_outer_braces(sub) + s[close_brace:].decode()
            tmp_vec = expand_braces(tmp_str)
            res.insert(res.end(), tmp_vec.begin(), tmp_vec.end())
    else:
        res.push_back(s.replace('\\}', '}'))

    # dedup
    sort(res.begin(), res.end())
    res.erase(unique(res.begin(), res.end()), res.end())

    return res
