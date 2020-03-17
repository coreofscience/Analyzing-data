from wostools import CollectionLazy
import igraph


def main():
    collection = CollectionLazy.from_filenames("records.txt")
    citation_pairs = collection.citation_pairs()
    citation_pairs = list(citation_pairs)

    vertices = set()
    for a, b in citation_pairs:
        vertices.add(a)
        vertices.add(b)

    vertices = list(vertices)

    graph = igraph.Graph(directed=True)
    graph.add_vertices(vertices)
    graph.add_edges(citation_pairs)

    graph = graph.components(mode="weak").giant()
    graph = graph.simplify()

    selected = graph.vs.select(
        lambda node: not (node.indegree() == 1 and node.outdegree() == 0)
    )
    graph = graph.subgraph(selected)
    print(graph.summary())


if __name__ == "__main__":
    main()
