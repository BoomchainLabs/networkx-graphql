"""Benchmarks for executing GraphQL queries against a generated schema."""

import strawberry

GRAPH_QUERY = """
{
  graph {
    name
    nodeCount
    edgeCount
    order
    size
    averageDegree
    nodeTypeCounts { name value }
    edgeTypeCounts { name value }
  }
}
"""

NODES_QUERY = """
{
  nodes {
    id
    type
    label
  }
}
"""

EDGES_QUERY = """
{
  edges {
    id
    type
    label
    weight
  }
}
"""

NEIGHBORHOOD_QUERY = """
{
  edges {
    id
    source { id label type }
    target { id label type }
  }
}
"""

MEASURE_QUERY = """
{
  measure(measure: is_connected) { name value }
}
"""

# the kind of query a GraphQL client (e.g. the built-in GraphiQL playground) sends on connect
INTROSPECTION_QUERY = """
{
  __schema {
    queryType { name }
    types {
      kind
      name
      fields { name type { kind name } }
      interfaces { name }
      enumValues { name }
    }
  }
}
"""


def execute(schema: strawberry.Schema, query: str):
    result = schema.execute_sync(query)
    assert result.errors is None
    return result


def test_query_graph_metadata(benchmark, medium_schema: strawberry.Schema):
    result = benchmark(execute, medium_schema, GRAPH_QUERY)

    assert result.data["graph"]["nodeCount"] == 200


def test_query_nodes(benchmark, medium_schema: strawberry.Schema):
    result = benchmark(execute, medium_schema, NODES_QUERY)

    assert len(result.data["nodes"]) == 200


def test_query_edges(benchmark, medium_schema: strawberry.Schema):
    result = benchmark(execute, medium_schema, EDGES_QUERY)

    assert len(result.data["edges"]) == 600


def test_query_edges_with_nodes(benchmark, medium_schema: strawberry.Schema):
    result = benchmark(execute, medium_schema, NEIGHBORHOOD_QUERY)

    assert len(result.data["edges"]) == 600


def test_query_measure(benchmark, medium_schema: strawberry.Schema):
    result = benchmark(execute, medium_schema, MEASURE_QUERY)

    assert result.data["measure"]["name"] == "is_connected"


def test_query_introspection(benchmark, medium_schema: strawberry.Schema):
    result = benchmark(execute, medium_schema, INTROSPECTION_QUERY)

    assert result.data["__schema"]["types"]
