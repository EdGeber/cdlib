from contextlib import contextmanager
import igraph as ig
import networkx as nx
import sys
import os
import time


@contextmanager
def suppress_stdout():
    """

    """
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = devnull
        sys.stderr = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr


def from_nx_to_igraph(g, directed=False):
    """

    :param g:
    :param directed:
    :return:
    """
    gi = ig.Graph(directed=directed)
    gi.add_vertices(list(g.nodes()))
    gi.add_edges(list(g.edges()))
    return gi


def from_igraph_to_nx(ig, directed=False):
    """

    :param ig:
    :param directed:
    :return:
    """
    if directed:
        tp = nx.DiGraph()
    else:
        tp = nx.Graph()

    g = nx.from_edgelist([(names[x[0]], names[x[1]])
                          for names in [ig.vs['name']] for x in ig.get_edgelist()], tp)
    return g


def convert_graph_formats(graph, desired_format, directed=False):
    if isinstance(graph, desired_format):
        return graph
    elif desired_format is nx.Graph:
        return from_igraph_to_nx(graph, directed)
    elif desired_format is ig.Graph:
        return from_nx_to_igraph(graph, directed)
    else:
        raise TypeError("The graph object should be either a networkx or an igraph one.")


def timeit(method):
    """
    Decorator: Compute the execution time of a function
    :param method: the function
    :return: the method runtime
    """

    def timed(*arguments, **kw):
        ts = time.time()
        result = method(*arguments, **kw)
        te = time.time()

        # sys.stdout.write('Time:  %r %2.2f sec\n' % (method.__name__.strip("_"), te - ts))
        # sys.stdout.write('------------------------------------\n')
        # sys.stdout.flush()
        return result, te-ts

    return timed