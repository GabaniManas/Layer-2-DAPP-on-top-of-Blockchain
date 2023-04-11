import networkx as nx
import powerlaw

def generate_power_law_distribution_graph(number_of_nodes:int):
    """ generate and return a graph following power law degree distribution with fixed alpha value of 1.5

    Args:
        number_of_nodes (int): number of nodes

    Returns:
        G: a graph following power law degree distribution
    """

    alpha = 1.5
    G = nx.expected_degree_graph(nx.utils.powerlaw_sequence(number_of_nodes, alpha) , selfloops=False)
    while not nx.is_connected(G):
        G = nx.expected_degree_graph(nx.utils.powerlaw_sequence(number_of_nodes, alpha) , selfloops=False)
    
    return G