"""Filename matching with shell patterns.
fnmatch(FILENAME, PATTERN) matches according to the local convention.
fnmatchcase(FILENAME, PATTERN) always takes case in account.
The functions operate by translating the pattern into a regular
expression.  They cache the compiled regular expressions for speed.
The function translate(PATTERN) returns a regular expression
corresponding to PATTERN.  (It does not compile it.)
"""

from libcpp.string cimport string

import re
import os
import posixpath
from lru import LRU


__all__ = ["filter", "fnmatch", "fnmatchcase", "translate"]


_MAXCACHE = 100000
_cache = LRU(_MAXCACHE)


cpdef fnmatch(string name, string pat):
    """Test whether FILENAME matches PATTERN.
    Patterns are Unix shell style:
    *       matches everything
    ?       matches any single character
    [seq]   matches any character in seq
    [!seq]  matches any char not in seq
    An initial period in FILENAME is not special.
    Both FILENAME and PATTERN are first case-normalized
    if the operating system requires it.
    If you don't want this, use fnmatchcase(FILENAME, PATTERN).

    *** Fast Version without normcase *** But only works in unix and macos ***
    """
    return fnmatchcase(name, pat)


cpdef filter(names, string pat):
    """Return the subset of the list NAMES that match PAT"""
    result = []
    pat=os.path.normcase(pat)
    try:
        re_pat = _cache[pat]
    except KeyError:
        res = translate(pat)
        _cache[pat] = re_pat = re.compile(res)
    match = re_pat.match
    if os.path is posixpath:
        # normcase on posix is NOP. Optimize it away from the loop.
        for name in names:
            if match(name):
                result.append(name)
    else:
        for name in names:
            if match(os.path.normcase(name)):
                result.append(name)
    return result


cdef fnmatchcase(string name, string pat):
    """Test whether FILENAME matches PATTERN, including case.
    This is a version of fnmatch() which doesn't case-normalize
    its arguments.
    """

    try:
        re_pat = _cache[pat]
    except KeyError:
        res = translate(pat)
        _cache[pat] = re_pat = re.compile(res)
    return re_pat.match(name) is not None


cdef translate(string pat):
    """Translate a shell PATTERN to a regular expression.
    There is no way to quote meta-characters.
    """
    cdef int i = 0
    cdef int n = pat.size()
    cdef string res = ''
    cdef char c
    # cdef string stuff

    while i < n:
        c = pat[i]
        i = i + 1
        if c == '*':
            res = res + '.*'
        elif c == '?':
            res = res + '.'
        elif c == '[':
            j = i
            if j < n and pat[j] == '!':
                j = j + 1
            if j < n and pat[j] == ']':
                j = j + 1
            while j < n and pat[j] != ']':
                j = j + 1
            if j >= n:
                res = res + '\\['
            else:
                stuff = pat[i:j].decode()
                stuff = stuff.replace('\\','\\\\')
                i = j + 1
                if stuff[0] == '!':
                    stuff[0] = '^'
                elif stuff[0] == '^':
                    stuff = '\\' + stuff
                res = res + '[' + stuff + ']'
        else:
            res = res + re.escape((<bytes> c))
    return res + '\Z(?ms)'
