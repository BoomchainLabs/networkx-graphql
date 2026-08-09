from collections.abc import Callable

import networkx as nx
import pytest

from networkx_graphql import schema

try:  # graphinate logs every node and edge it processes, which would pollute the measurements
    from loguru import logger

    logger.disable("graphinate")
except ImportError:  # pragma: no cover
    pass

SEED = 42


def make_graph(node_count: int, edge_count: int, graph_type: type[nx.Graph] = nx.Graph) -> nx.Graph:
    """Build a deterministic random graph of the given type and size."""
    template = graph_type()
    generated = nx.gnm_random_graph(node_count, edge_count, seed=SEED, directed=template.is_directed())
    graph = graph_type(generated)

    if template.is_multigraph():
        # make the multigraph actually multi, by duplicating every tenth edge
        graph.add_edges_from([(source, target) for source, target, _ in list(graph.edges)[::10]])

    graph.name = f"{graph_type.__name__}-{node_count}-{edge_count}"
    return graph


@pytest.fixture(scope="session")
def graph_factory() -> Callable[..., nx.Graph]:
    return make_graph


@pytest.fixture(scope="session")
def small_graph() -> nx.Graph:
    return make_graph(50, 100)


@pytest.fixture(scope="session")
def medium_graph() -> nx.Graph:
    return make_graph(200, 600)


@pytest.fixture(scope="session")
def large_graph() -> nx.Graph:
    return make_graph(1_000, 3_000)


@pytest.fixture(scope="session")
def medium_schema(medium_graph: nx.Graph):
    """A schema built once, so that query benchmarks do not measure schema generation."""
    return schema(medium_graph)
