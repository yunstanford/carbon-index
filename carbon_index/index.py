from .node import TrieNode


class CarbonIndex:
    """
    an index for carbon-cache instances.
    """

    def __init__(self, name='carbon_index', sep='.'):
        self.name = name
        self.root = TrieNode('root', is_leaf=False)
        self.sep = sep

    def insert(self, metric):
        """
        insert metric to carbon Trie Index.

        args: metric name.
        """
        metric_parts = metric.split(self.sep)
        self._insert(self.root, metric_parts)

    def has_metric(self, metric):
        """
        check if the metric exists.

        args: metric.
        """
        metric_parts = metric.split(self.sep)
        cur = self.root
        for part in metric_parts:
            if not cur.has_child(part):
                return False
            cur = cur.get(part)
        return cur.is_leaf

    def delete(self, metric):
        """
        remove a metric from index. wild.

        args: metric, should not include wildcards.

        return: True/False.
        """
        metric_parts = metric.split(self.sep)
        return self._delete(self.root, metric_parts)

    def expand_query(self, query):
        """
        expand a wildcard query
        """
        return self.root.expand_query(query)

    def expand_pattern(self, pattern):
        """
        expand a wildcard query pattern.

        This is different from expand_query, as it may
        return BranchNode.
        """
        return self.root.expand_pattern(pattern)

    def _insert(self, parent, metric_parts):
        """
        a private helper function for insert metric.
        """
        if len(metric_parts) == 0:
            return
        if len(metric_parts) == 1:
            parent.add(TrieNode(metric_parts[0]))
            return
        if not parent.get(metric_parts[0]):
            parent.add(TrieNode(metric_parts[0], is_leaf=False))
        self._insert(parent.get(metric_parts[0]), metric_parts[1:])

    def _delete(self, cur, metric_parts):
        if len(metric_parts) == 0:
            if cur.is_leaf:
                cur.is_leaf = False
                return True
            else:
                return False
        if cur.has_child(metric_parts[0]):
            nxt = cur.get(metric_parts[0])
            deleted = self._delete(nxt, metric_parts[1:])
            if nxt.count() == 0 and (not nxt.is_leaf):
                cur.delete(nxt.name)
            return deleted
        else:
            return False
