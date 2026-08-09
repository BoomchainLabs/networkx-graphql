"""Benchmarks for GraphQL schema generation from NetworkX graphs."""

from collections.abc import Callable

import networkx as nx
import pytest
import strawberry

from networkx_graphql import schema

GRAPH_TYPES = (nx.Graph, nx.DiGraph, nx.MultiGraph, nx.MultiDiGraph)


def test_schema_empty_graph(benchmark):
    graph = nx.Graph(name="empty")

    result: strawberry.Schema = benchmark(schema, graph)

    assert isinstance(result, strawberry.Schema)


def test_schema_small_graph(benchmark, small_graph: nx.Graph):
    result: strawberry.Schema = benchmark(schema, small_graph)

    assert isinstance(result, strawberry.Schema)


def test_schema_medium_graph(benchmark, medium_graph: nx.Graph):
    result: strawberry.Schema = benchmark(schema, medium_graph)

    assert isinstance(result, strawberry.Schema)


def test_schema_large_graph(benchmark, large_graph: nx.Graph):
    result: strawberry.Schema = benchmark(schema, large_graph)

    assert isinstance(result, strawberry.Schema)


@pytest.mark.parametrize("graph_type", GRAPH_TYPES, ids=lambda graph_type: graph_type.__name__)
def test_schema_graph_type(benchmark, graph_factory: Callable[..., nx.Graph], graph_type: type[nx.Graph]):
    graph = graph_factory(200, 600, graph_type)

    result: strawberry.Schema = benchmark(schema, graph)

    assert isinstance(result, strawberry.Schema)


def test_schema_with_custom_node_type_extractor(benchmark, medium_graph: nx.Graph):
    def node_type_extractor(node) -> str:
        return "even" if node % 2 == 0 else "odd"

    result: strawberry.Schema = benchmark(schema, medium_graph, node_type_extractor=node_type_extractor)

    assert isinstance(result, strawberry.Schema)


def test_schema_definition_language_print(benchmark, medium_schema: strawberry.Schema):
    result = benchmark(medium_schema.as_str)

    assert result
