import networkx as nx
import powerlaw

def generate_power_law_distribution_graph(number_of_nodes:int):
    """ generate and return a graph following power law degree distribution 

    Args:
        number_of_nodes (int): number of nodes

    Returns:
        G: a graph following power law degree distribution
    """
    
    # Generate a power law distribution with alpha=2.5 and xmin=1
    pl_dist = powerlaw.Power_Law(xmin=1, parameters=[2.5])

    # Generate samples from the distribution
    samples = pl_dist.generate_random(number_of_nodes)

    degree_sequence = [int(i) for i in samples]
    degree_sequence.sort(reverse=True)

    G = nx.Graph()
    for i in range(number_of_nodes):
        for j in range(i + 1, number_of_nodes):
            if (degree_sequence[i] > 0 and degree_sequence[j] > 0):
                degree_sequence[i] -= 1
                degree_sequence[j] -= 1
                G.add_edge(i, j)
                G.add_edge(j, i)
    return G