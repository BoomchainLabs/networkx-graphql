import networkx as nx
import strawberry
from graphinate import GraphModel, GraphType, graphql
from graphinate.builders import GraphQLBuilder
from graphinate.typing import Extractor


def schema(graph: nx.Graph, node_type_extractor: Extractor | None = None) -> strawberry.Schema:
    """Generate a Strawberry GraphQL schema from a NetworkX graph.

    Args:
        graph (nx.Graph): The input NetworkX graph.
        node_type_extractor (Extractor | None, optional): A function to extract node types from the graph nodes.
            If None, all nodes will be treated as the same type 'node'. Defaults to None.

    Returns:
        strawberry.Schema: The generated GraphQL schema.
    """
    graph_model = GraphModel(name=graph.name)

    node_type_extractor = node_type_extractor if callable(node_type_extractor) else 'node'

    @graph_model.node(node_type_extractor)
    def nodes():
        yield from graph.nodes

    @graph_model.edge('edge')
    def edges():
        for edge in graph.edges:
            yield {'source': edge[0], 'target': edge[1]}

    graphql_builder = GraphQLBuilder(graph_model, graph_type=GraphType.of(graph))

    return graphql_builder.build()


def server(graphql_schema: strawberry.Schema, port: int = 8073):
    """Run a GraphQL server with the given schema on the specified port.

    Args:
        graphql_schema (strawberry.Schema): The Strawberry GraphQL schema to serve.
        port (int, optional): The port number to run the server on. Defaults to 8073.
    """
    graphql.server(graphql_schema=graphql_schema, port=port)
