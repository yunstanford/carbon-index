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
    carbon_index.insert('ZG.hotpads.ops')
    assert carbon_index.has_metric('ZG.hotpads.ops') is True
    assert carbon_index.has_metric('ZG.hotpads') is True


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


def test_index_expand_pattern(carbon_index):
    assert carbon_index.delete('ZG.zillow.velocity.mondev') is True
    all_matches = carbon_index.expand_pattern('ZG.zillow.*')
    assert sorted(all_matches) == [('ZG.zillow.product', False), ('ZG.zillow.velocity', True)]


def test_index_expand_pattern_edge_case(carbon_index):
    all_matches = carbon_index.expand_pattern('ZG.zillow.*')
    assert sorted(all_matches) == [('ZG.zillow.product', False),
                                   ('ZG.zillow.velocity', False),
                                   ('ZG.zillow.velocity', True)]


def test_index_delete_empty(carbon_index):
    assert carbon_index.delete('') is False


def test_index_delete_not_exist(carbon_index):
    assert carbon_index.delete('ZG.SF.ops') is False


def test_index_delete_remove(carbon_index):
    assert carbon_index.has_metric('ZG.zillow.product.rental') is True
    assert carbon_index.delete('ZG.zillow.product.rental')
    assert carbon_index.has_metric('ZG.zillow.product.rental') is False
    assert carbon_index.root.get('ZG').get('zillow').get('product').count() == 1

    assert carbon_index.delete('ZG.zillow.product.listing') is True
    assert carbon_index.root.get('ZG').get('zillow').get('product') is None
    assert carbon_index.root.get('ZG').get('zillow').count() == 1


def test_index_delete_remove_both_file_and_dir_exist_1(carbon_index):
    assert carbon_index.has_metric('ZG.zillow.velocity') is True
    assert carbon_index.has_metric('ZG.zillow.velocity.mondev') is True
    assert carbon_index.delete('ZG.zillow.velocity.mondev') is True
    assert carbon_index.has_metric('ZG.zillow.velocity.mondev') is False
    assert carbon_index.has_metric('ZG.zillow.velocity') is True


def test_index_delete_remove_both_file_and_dir_exist_2(carbon_index):
    assert carbon_index.has_metric('ZG.zillow.velocity') is True
    assert carbon_index.has_metric('ZG.zillow.velocity.mondev') is True
    assert carbon_index.delete('ZG.zillow.velocity') is True
    assert carbon_index.has_metric('ZG.zillow.velocity') is False
    assert carbon_index.has_metric('ZG.zillow.velocity.mondev') is True
