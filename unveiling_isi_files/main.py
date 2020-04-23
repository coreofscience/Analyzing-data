from wostools import CollectionLazy
import igraph
import pandas as pd
import statistics as st
import click


@click.command()
@click.argument("FILE")
@click.option("--output", "-o", default="output.csv", help="Caracteristicas de la red")
def main(file, output):
    """ Extrae las caracteristicas básicas de la red """
    collection = CollectionLazy.from_filenames(file)
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

    max_cluster = max(graph.biconnected_components().sizes())
    for i in graph.biconnected_components():
        if len(i) == max_cluster:
            cluster_1 = graph.subgraph(i)

    features = pd.DataFrame(index=[file])
    for i in graph, cluster_1:
        if i == graph:
            j = "Complet"
        else:
            j = "Cluster"
        nodes = i.vcount()
        edges = i.ecount()
        features["Nodes " + j] = nodes
        features["Edges " + j] = edges

        max_degree = i.maxdegree()
        degree = i.degree()
        betweenness = i.betweenness()
        closeness = i.closeness()

        diameter = i.diameter()
        density = i.density()
        clusters_biconnected = len(i.biconnected_components())
        features["Diameter " + j] = diameter
        features["Density " + j] = density
        features["Cluster biconected " + j] = clusters_biconnected

        mean_degree = st.mean(degree)
        sd_degree = st.stdev(degree)
        var_degree = st.variance(degree)
        mean_indegree = st.mean(i.indegree())
        mean_outdegree = st.mean(i.outdegree())
        features["Max degree " + j] = max_degree
        features["Mean degree " + j] = mean_degree
        features["Sd degree " + j] = sd_degree
        features["Var degree " + j] = var_degree
        features["Mean indegree " + j] = mean_indegree
        features["Mean outdegree " + j] = mean_outdegree

        mean_betweenness = st.mean(betweenness)
        sd_betw = st.stdev(betweenness)
        var_betw = st.variance(betweenness)
        features["Mean betweenness " + j] = mean_betweenness
        features["Sd betweenness " + j] = sd_betw
        features["Var betweenness " + j] = var_betw

        mean_closeness = st.mean(closeness)
        sd_closeness = st.stdev(closeness)
        var_closeness = st.variance(closeness)
        features["Mean closeness " + j] = mean_closeness
        features["Sd closeness " + j] = sd_closeness
        features["Var closeness " + j] = var_closeness

    features.to_csv(output)


if __name__ == "__main__":
    main()
