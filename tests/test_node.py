from carbon_index.node import TrieNode


def test_node_get(trie_node):
    seattle = trie_node.get('Seattle')
    assert seattle is not None
    assert seattle.get('zillow') is not None
    assert seattle.get('zillow2') is not None
    assert seattle.get('zil3low') is not None


def test_node_has_child(trie_node):
    assert trie_node.has_child('Seattle') is True
    assert trie_node.has_child('NewYork') is True
    assert trie_node.has_child('SF') is True
    assert trie_node.has_child('Boston') is False


def test_node_get_all_wildcard_star(trie_node):
    all_matches = trie_node.get_all('*')
    all_match_strs = [match.name for match in all_matches]
    assert sorted(all_match_strs) == ['NewYork', 'SF', 'Seattle']


def test_node_get_all_wildcard_star_partial(trie_node):
    seattle = trie_node.get('Seattle')
    all_matches = seattle.get_all('zill*')
    all_match_strs = [match.name for match in all_matches]
    assert sorted(all_match_strs) == ['zillow', 'zillow2']


def test_node_get_all_wildcard_brackets(trie_node):
    seattle = trie_node.get('Seattle')
    all_matches = seattle.get_all('zil[0-9]low')
    assert len(all_matches) == 1
    assert 'zil3low' == all_matches[0].name


def test_node_get_all_wildcard_braces(trie_node):
    seattle = trie_node.get('Seattle')
    all_matches = seattle.get_all('zill{ow,ow2}')
    all_match_strs = [match.name for match in all_matches]
    assert sorted(all_match_strs) == ['zillow', 'zillow2']


def test_node_get_all_wildcard_braces_single_metric(trie_node):
    seattle = trie_node.get('Seattle')
    all_matches = seattle.get_all('{zillow}')
    all_match_strs = [match.name for match in all_matches]
    assert sorted(all_match_strs) == ['zillow']


def test_node_add(trie_node):
    assert trie_node.get('LA') is None
    trie_node.add(TrieNode('LA'))
    assert trie_node.has_child('LA')


def test_node_add_is_leaf(trie_node):
    assert trie_node.get('SF').is_leaf is False
    trie_node.add(TrieNode('SF'))
    assert trie_node.get('SF').is_leaf is True


def test_expand_query_no_wildcard(trie_node):
    queries = trie_node.expand_query('Seattle.zillow')
    assert queries == ['Seattle.zillow']


def test_expand_query_not_exist(trie_node):
    queries = trie_node.expand_query('Seattle.trulia')
    assert queries == []


def test_expand_query_wildcards(trie_node):
    queries = trie_node.expand_query('Seattle.*')
    assert len(queries) == 3
    queries = trie_node.expand_query('*.*')
    assert len(queries) == 6
    assert 'NewYork.hotpads' in queries


def test_is_exist(trie_node):
    assert trie_node.is_exist('Seattle.zillow') is True
    assert trie_node.is_exist('NewYork.hotpads') is True
    assert trie_node.is_exist('Seattle.trulia') is False


def test_is_exist_add_leaf_in_branch_node(trie_node):
    assert trie_node.is_exist('Seattle.zillow') is True
    assert trie_node.is_exist('Seattle') is False
    trie_node.add(TrieNode('Seattle'))
    assert trie_node.is_exist('Seattle') is True


def test_expand_pattern_wildcards(trie_node):
    trie_node.add(TrieNode('realestateDOTcom'))
    assert trie_node.is_exist('realestateDOTcom') is True
    patterns = trie_node.expand_pattern('*')
    assert len(patterns) == 4
    assert sorted(patterns, key=lambda tup: tup[0]) == [('NewYork', False), ('SF', False), ('Seattle', False), ('realestateDOTcom', True)]
