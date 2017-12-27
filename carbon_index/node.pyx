from libcpp.map cimport map
from libcpp.string cimport string
from libcpp.vector cimport vector
from libcpp cimport bool


import fnmatch
from .utils import expand_braces


cdef class TrieNode:
    """
    an standard unit in carbon index.
    """
    cdef public string name
    cdef public bool is_leaf
    cdef public string sep
    cdef public map[string, vector[TrieNode]] children

    def __init__(self, name, is_leaf=True, sep="."):
        self.is_leaf = is_leaf
        self.name = name
        self.sep = "."

    cdef get(self, child_name):
        """
        get child node.

        args: name of child node.
        """
        return self.children[child_name]

    cdef has_child(self, child_name):
        """
        check if child_name exists.

        args: name of a child node.
        """
        return self.children.find(child_name) != self.children.end()

    cdef get_all(self, pattern):
        """
        get all children nodes based on wild card query.

        args: query_pattern.
        """
        matches = []
        patterns = expand_braces(pattern)
        for child in self.children:
            for p in patterns:
                if fnmatch.fnmatch(child, p):
                    matches.append(self.children[child])
        return matches

    cdef delete(self, child_name):
        """
        provide to pop a child node.

        args: name of child node.
        """
        if self.has_child(child_name):
            self.children.pop(child_name)
            return True
        return False

    cdef add(self, child_node):
        """
        append a child node.

        args: child node.

        special case:
        Both ZG.seattle and ZG.seattle.zillow exist, we should take care of it as well.
        """
        if child_node.name in self.children:
            if (not self.children[child_node.name].is_leaf) and child_node.is_leaf:
                self.children[child_node.name].is_leaf = child_node.is_leaf
        else:
            self.children[child_node.name] = child_node

    cdef expand_query(self, query):
        """
        expand a wildcard query.

        args: query.
        return: a list of queries.

        examples: {foo,bar}baz.carbon.cache = [foobaz.carbon.cache, barbaz.carbon.cache]
        """
        sep_index = query.find(self.sep)

        if sep_index < 0:
            return [q.name for q in self.get_all(query) if q.is_leaf]
        else:
            queries = []
            cur_part = query[:sep_index]
            cur_matches = self.get_all(cur_part)
            sub_query = query[sep_index + 1:]
            for match in cur_matches:
                sub_queries = match.expand_query(sub_query)
                for sq in sub_queries:
                    queries.append(".".join([match.name, sq]))
            return queries

    cdef expand_pattern(self, query):
        """
        expand a wildcard query pattern.

        args: query.
        return: a list of tuples (query,is_leaf).

        examples: {foo,bar}baz.carbon.cache = [(foobaz.carbon.cache, True), (barbaz.carbon.cache, True)]
        """
        sep_index = query.find(self.sep)
        queries = []
        if sep_index < 0:
            for q in self.get_all(query):
                queries.append((q.name, q.is_leaf))
                # take care of an edge case:
                # both dir and file exist
                if q.is_leaf and q.count() != 0:
                    queries.append((q.name, False))
            return queries
        else:
            cur_part = query[:sep_index]
            cur_matches = self.get_all(cur_part)
            sub_query = query[sep_index + 1:]
            for match in cur_matches:
                sub_queries = match.expand_pattern(sub_query)
                for sq, is_leaf in sub_queries:
                    queries.append((".".join([match.name, sq]), is_leaf))
            return queries

    cdef is_leaf(self):
        """
        return true if the node is leaf.
        """
        return self.is_leaf

    cdef count(self):
        """
        children count.
        """
        return len(self.children)

    cdef is_exist(self, query):
        """
        return true if query exist. query match starts from child level/next level.

        query here should not include wildcards.
        """
        if query == "":
            return self.is_leaf

        sep_index = query.find(self.sep)

        if sep_index < 0:
            return self.has_child(query) and self.get(query).is_exist("")
        part = query[:sep_index]
        return self.has_child(part) and self.get(part).is_exist(query[sep_index + 1:])
