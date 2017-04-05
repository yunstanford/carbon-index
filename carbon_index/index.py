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
        


    def has_metric(self, metric):


    def delete(self, metric):


    def expand_query(self, metric):

