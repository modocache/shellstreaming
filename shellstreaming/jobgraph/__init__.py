# -*- coding: utf-8 -*-
"""
    shellstreaming.jobgraph
    ~~~~~~~~~~~~~~~~~~~~~~~

    :synopsis: Provides job graph
"""
import networkx as nx


class JobGraph(nx.DiGraph):
    """Provides utility functions in addition to :class:`networkx.DiGraph`"""

    edge_labels = {}
    """edges' label to draw"""

    def begin_nodes(self):
        """Return nodes who don't have incomming edges.

        **Examples**

        .. code-block:: python
            >>> G = JobGraph()
            >>> G.add_path([0,1,2])
            >>> G.begin_nodes()
            [0]
            >>> G.add_edge(3, 1, stream_edge_id='')
            >>> G.begin_nodes()
            [0, 3]
        """
        return [n for n in self.nodes() if self.in_edges(n) == []]

    def end_nodes(self):
        """Return nodes who don't have outcomming edges.

        **Examples**

        .. code-block:: python
            >>> G = JobGraph()
            >>> G.add_path([0,1,2])
            >>> G.end_nodes()
            [2]
            >>> G.add_edge(1, 3, stream_edge_id='')
            >>> G.end_nodes()
            [2, 3]
        """
        return [n for n in self.nodes() if self.out_edges(n) == []]

    def add_node(
            self, job_id,
            job_class, job_class_args, job_type,
    ):
        """Override :func:`Digraph.add_node` to force put necessary attributes to every node"""
        nx.DiGraph.add_node(
            self, job_id,
            attr_dict={
                'class' : job_class,
                'args'  : job_class_args,
                'type'  : job_type,
            }
        )

    def add_edge(self, src_job_id, dest_job_id, stream_edge_id):
        """Override :func:`Digraph.add_edge` to force put necessary attributes to every edge"""
        nx.DiGraph.add_edge(self, src_job_id, dest_job_id, attr_dict={'stream_edge_id': stream_edge_id})

    def out_stream_edge_ids(self, job_id):
        """Return :class:`StreamEdge` id of each outcomming edge"""
        return [self.edge[job_id][succ]['stream_edge_id'] for succ in self.successors(job_id)]

    def in_stream_edge_ids(self, job_id):
        """Return :class:`StreamEdge` id of each incomming edge"""
        return [self.edge[pred][job_id]['stream_edge_id'] for pred in self.predecessors(job_id)]


class StreamEdge(object):

    def __init__(self, id, src_job_id, dest_job_id=None):
        self.id          = id
        self.src_job_id  = src_job_id
        self.dest_job_id = dest_job_id