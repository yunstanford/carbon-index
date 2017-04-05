from .node import TrieNode


class CarbonIndex:
    """
    an index for carbon-cache instances.
    """

    def __init__(self, name='carbon_index'):
        self.name = name
        self.root = TrieNode('root', is_leaf=False)

    def insert(self, metric):
        """
        insert metric to carbon Trie Index.

        args: metric name.
        """
        metric_parts = metric.split('.')
        self._insert(self.root, metric_parts)

    def has_metric(self, metric):
        """
        check if the metric exists.

        args: metric.
        """
        metric_parts = metric.split('.')
        cur = self.root
        for part in metric_parts:
            if not cur.has_child(part):
                return False
            cur = cur.get(part)
        return cur.is_leaf

    def delete(self, metric):
        """
        remove a metric from index.

        args: metric, should not include wildcards.
        """
        pass

    def expand_query(self, query):
        """
        expand a wildcard query
        """
        return self.root.expand_query(query)

    def _insert(self, parent, metric_parts):
        """
        a private helper function for insert metric.
        """
        if len(metric_parts) == 0:
            return
        if len(metric_parts) == 1:
            parent.add(TrieNode(metric_parts[0]))
            return
        parent.add(TrieNode(metric_parts[0], is_leaf=False))
        self._insert(parent.get(metric_parts[0]), metric_parts[1:])
