def test_benchmark(carbon_index_benchmark, benchmark):
	benchmark.pedantic(carbon_index_benchmark.expand_query,
					   args=('ZG.*.product.rental',),
					   iterations=10,
					   rounds=1000)
