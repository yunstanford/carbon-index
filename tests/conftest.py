import pytest
from carbon_index.node import TrieNode


@pytest.fixture
def trie_node():
    # level 1
    ZG = TrieNode('ZG', is_leaf=False)
    # level 2
    seattle = TrieNode('Seattle', is_leaf=False)
    new_york = TrieNode('NewYork', is_leaf=False)
    san_francisco = TrieNode('SF', is_leaf=False)
    # level 3
    zillow = TrieNode('zillow')
    zillow2 = TrieNode('zillow2')
    zillow3 = TrieNode('zil3low')
    hotpads = TrieNode('hotpads')
    trulia = TrieNode('trulia')
    streeteasy = TrieNode('streeteasy')
    # relations
    seattle.add(zillow)
    seattle.add(zillow2)
    seattle.add(zillow3)
    new_york.add(hotpads)
    new_york.add(streeteasy)
    san_francisco.add(trulia)
    ZG.add(seattle)
    ZG.add(new_york)
    ZG.add(san_francisco)
    return ZG
