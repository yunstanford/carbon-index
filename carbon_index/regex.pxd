from libcpp.string cimport string


cdef extern from "<regex>" namespace "std" nogil:
    cdef cppclass basic_regex[T, V]:
        pass

    string regex_replace[Traits, CharT, STraits, SAlloc, FTraits, FAlloc](
        const string& s,
        const basic_regex& re,
        const string& fmt,
    )

