import pytest


def test_index_has_metric(carbon_index):
	assert carbon_index.has_metric('ZG.zillow.velocity') is True
	assert carbon_index.has_metric('ZG.zillow.velocity.mondev') is True
	assert carbon_index.has_metric('ZG.zillow.product') is False


def test_index_insert(carbon_index):
	assert carbon_index.has_metric('ZG.hotpads') is False
	assert carbon_index.has_metric('ZG.zillow.velocity.perf') is False
	carbon_index.insert('ZG.hotpads')
	carbon_index.insert('ZG.zillow.velocity.perf')
	assert carbon_index.has_metric('ZG.hotpads') is True
	assert carbon_index.has_metric('ZG.zillow.velocity.perf') is True
	carbon_index.insert('ZG.product')
	assert carbon_index.has_metric('ZG.product') is True


def test_index_expand_query_no_wildcard(carbon_index):
	all_matches = carbon_index.expand_query('ZG.zillow.velocity.mondev')
	assert all_matches == ['ZG.zillow.velocity.mondev']


def test_index_expand_query_not_exist(carbon_index):
	all_matches = carbon_index.expand_query('ZG.zillow.product.mortgage')
	assert all_matches == []


def test_index_expand_query_star(carbon_index):
	all_matches = carbon_index.expand_query('ZG.*.product.rental')
	assert sorted(all_matches) == ['ZG.trulia.product.rental', 'ZG.zillow.product.rental']


def test_index_expand_query_brackets(carbon_index):
	all_matches = carbon_index.expand_query('ZG.zi[a-z]low.product.*')
	assert sorted(all_matches) == ['ZG.zillow.product.listing', 'ZG.zillow.product.rental']


def test_index_expand_query_braces(carbon_index):
	all_matches = carbon_index.expand_query('ZG.{trulia,zillow}.product.*')
	assert sorted(all_matches) == ['ZG.trulia.product.rental', 'ZG.zillow.product.listing', 'ZG.zillow.product.rental']
