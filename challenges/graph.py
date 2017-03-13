# noinspection PyShadowingBuiltins
class Node:
    def __init__(self, id):
        self._id = id
        self._incoming = []
        self._outgoing = []

    @property
    def id(self):
        return self._id

    @property
    def incoming(self):
        return self._incoming

    @property
    def outgoing(self):
        return self._outgoing

    def add_edge(self, edge):
        if self is edge.head:
            self._incoming.append(edge)
        elif self is edge.tail:
            self._outgoing.append(edge)
        else:
            raise ValueError(
                'The node is neither head nor tail of the edge.'
            )

    def antecessors(self):
        return (edge.tail for edge in self.incoming)

    def successors(self):
        return (edge.head for edge in self.outgoing)

    def __str__(self):
        pre = str([edge.tail.id for edge in self.incoming])
        post = str([edge.head.id for edge in self.outgoing])
        return '{}->({})->{}'.format(pre, self.id, post)

    def __repr__(self):
        return self.__str__()


class Edge:
    def __init__(self, tail, head):
        self._tail = tail
        self._head = head

    @property
    def tail(self):
        return self._tail

    @property
    def head(self):
        return self._head

    def __str__(self):
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
        """Return nodes a sorted list by keys."""
        return list(self._nodes[key] for key in sorted(self._nodes))

    def keys(self):
        """Return keys of nodes in sorted order."""
        return sorted(self._nodes)

    def count(self):
        """Return count of nodes."""
        return len(self._nodes)
