import pytest
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
	assert len(all_matches) == 3
	assert TrieNode('Seattle') in all_matches
	assert TrieNode('SF') in all_matches
	assert TrieNode('NewYork') in all_matches


def test_node_get_all_wildcard_star_partial(trie_node):
	seattle = trie_node.get('Seattle')
	all_matches = trie_node.get_all('zill*')
	assert len(all_matches) == 2
	assert TrieNode('zil3low') in all_matches
	assert TrieNode('zillow2') in all_matches


def test_node_get_all_wildcard_brackets(trie_node):
	seattle = trie_node.get('Seattle')
	all_matches = trie_node.get_all('zil[0-9]low')
	assert len(all_matches) == 1
	assert TrieNode('zil3low') in all_matches


def test_node_get_all_wildcard_braces(trie_node):
	seattle = trie_node.get('Seattle')
	all_matches = trie_node.get_all('zill{ow,ow2}')
	assert len(all_matches) == 2
	assert TrieNode('zillow') in all_matches
	assert TrieNode('zillow2') in all_matches


def test_node_add(trie_node):
	assert trie_node.get('LA') is None
	trie_node.add(TrieNode('LA'))
	assert trie_node.has_child('LA')


def test_expand_query_no_wildcard(trie_node):
	queries = trie_node.expand_query('ZG.Seattle.zillow')
	assert queries == ['ZG.Seattle.zillow']


def test_expand_query_not_exist(trie_node):
	queries = trie_node.expand_query('ZG.Seattle.trulia')
	assert queries == []


def test_expand_query_wildcards(trie_node):
	queries = trie_node.expand_query('ZG.Seattle.*')
	assert len(queries) = 3
	queries = trie_node.expand_query('ZG.*.*')
	assert len(queries) = 6
	assert 'ZG.NewYork.hotpads' in queries


def test_is_exist(trie_node):
	assert trie_node.is_exist('Seattle.zillow') is True
	assert trie_node.is_exist('NewYork.hotpads') is True
	assert trie_node.is_exist('Seattle.trulia') is False
