import networkx as nx

import networkx_graphql as nxg

g = nx.ladder_graph(5)

schema = nxg.schema(g)

nxg.run(schema, 8073)
