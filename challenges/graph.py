# noinspection PyShadowingBuiltins
class Node:
    def __init__(self, id):
        """ Create a node.

        Not for direct usage. To create node and edges use:

            * Graph.create_node()
            * Graph.create_edge()
        """
        self._id = id
        self._incoming = []
        self._outgoing = []

    @property
    def id(self):
        """ Return the nodes id."""
        return self._id

    @property
    def incoming(self):
        """ Return the incoming EDGES of the node. """
        return self._incoming

    @property
    def outgoing(self):
        """ Return the outgoing EDGES of the node. """
        return self._outgoing

    def add_edge(self, edge):
        """ Add an edge to the node.

        Not for direct usage. To create node and edges use:

            * Graph.create_node()
            * Graph.create_edge()
        """
        if self is edge.head:
            self._incoming.append(edge)
        elif self is edge.tail:
            self._outgoing.append(edge)
        else:
            raise ValueError(
                'The node is neither head nor tail of the edge.'
            )

    def antecessors(self):
        """ Return the incoming NODES of the node.

        The tail nodes of all incoming edges.
        """
        return (edge.tail for edge in self.incoming)

    def successors(self):
        """ Return the outgoing NODES of the node.

        The head nodes of all outgoing edges.
        """
        return (edge.head for edge in self.outgoing)

    def __str__(self):
        """ Return a human readable string representation of the node. """
        pre = str([edge.tail.id for edge in self.incoming])
        post = str([edge.head.id for edge in self.outgoing])
        return '{}->({})->{}'.format(pre, self.id, post)

    def __repr__(self):
        """ Return a human readable string representation of the node. """
        return self.__str__()


class Edge:
    def __init__(self, tail, head):
        """ Create an edge.

        Not for direct usage. To create node and edges use:

            * Graph.create_node()
            * Graph.create_edge()
        """
        self._tail = tail
        self._head = head

    @property
    def tail(self):
        """ Return the tail node. """
        return self._tail

    @property
    def head(self):
        """ Return the head node. """
        return self._head

    def __str__(self):
        """ Return a human readable string representation of the edge. """
        return '({})->({})'.format(self.tail.id, self.head.id)


# noinspection PyShadowingBuiltins
class Graph:
    def __init__(self):
        self._nodes = {}

    def create_node(self, id):
        """Add a standalone node to the graph and return it.

        If a node of this id already exists, it is just returned.
        """
        if id not in self._nodes:
            self._nodes[id] = Node(id)
        return self._nodes[id]

    def create_edge(self, tail, head):
        """Add an edge and return it.

        Create nodes as necessary.

        :tail: Node or id of node
        :head: Node or id of node
        """
        if isinstance(tail, Node):
            tail_node = tail
        else:
            tail_node = self.create_node(tail)
        if isinstance(head, Node):
            head_node = head
        else:
            head_node = self.create_node(head)
        edge = Edge(tail_node, head_node)
        tail_node.add_edge(edge)
        head_node.add_edge(edge)
        return edge

    def node(self, id):
        """Return a node by id."""
        return self._nodes[id]

    def nodes(self):
        """Return all nodes sorted by node id."""
        return list(self._nodes[key] for key in sorted(self._nodes))

    def keys(self):
        """Return keys of nodes in sorted order."""
        return sorted(self._nodes)

    def count(self):
        """Return count of nodes."""
        return len(self._nodes)
