from unittest import TestCase

from challenges import Graph, Node, Edge


class TestNode(TestCase):
    """Test units of Node."""

    def setUp(self):
        self.node = Node(2)

    def test_node_constructor(self):
        self.assertEqual(self.node._id, 2)

    def test_node_property_access(self):
        self.assertEqual(self.node.id, 2)
        self.node.any = 5
        self.assertEqual(self.node.any, 5)

    def test_add_edge_to_node(self):
        tail = Node(1)
        head = Node(2)
        edge = Edge(tail, head)
        tail.add_edge(edge)
        head.add_edge(edge)
        self.assertIn(edge, tail.outgoing)
        self.assertIn(edge, head.incoming)

    def test_antecessors(self):
        n1, n3 = Node(1), Node(3)
        self.node.add_edge(Edge(n1, self.node))
        self.node.add_edge(Edge(n3, self.node))
        self.assertIn(n1, self.node.antecessors())
        self.assertIn(n3, self.node.antecessors())

    def test_successors(self):
        n1, n3 = Node(1), Node(3)
        self.node.add_edge(Edge(self.node, n1))
        self.node.add_edge(Edge(self.node, n3))
        self.assertIn(n1, self.node.successors())
        self.assertIn(n3, self.node.successors())


class TestEdge(TestCase):
    """Test units of Node."""

    def setUp(self):
        self.tail = Node(1)
        self.head = Node(2)
        self.edge = Edge(self.tail, self.head)

    def test_edge_constructor(self):
        self.assertIs(self.edge._tail, self.tail)
        self.assertIs(self.edge._head, self.head)

    def test_edge_property_access(self):
        self.assertIs(self.edge.tail, self.tail)
        self.assertIs(self.edge.head, self.head)
        self.edge.any = 5
        self.assertEqual(self.edge.any, 5)


class TestGraph(TestCase):
    """Test units of Graph."""

    def setUp(self):
        self.graph = Graph()

    def test_graph_constructor(self):
        self.assertIsInstance(self.graph, Graph)

    def test_create_node(self):
        node = self.graph.create_node(2)
        self.assertIsInstance(node, Node)
        self.assertEqual(node.id, 2)
        self.assertIs(self.graph._nodes[2], node)

    def test_create_existing_node_returns_existing_node(self):
        node1 = self.graph.create_node(2)
        node2 = self.graph.create_node(2)
        self.assertIs(node1, node2)

    def test_create_edge(self):
        edge = self.graph.create_edge(1, 2)
        self.assertEqual(edge.tail.id, 1)
        self.assertEqual(edge.head.id, 2)
        self.assertIn(1, self.graph._nodes)
        self.assertIn(2, self.graph._nodes)
        self.assertIn(edge, edge.tail.outgoing)
        self.assertIn(edge, edge.head.incoming)

    def test_create_edge_from_nodes(self):
        node1 = self.graph.create_node(1)
        node2 = self.graph.create_node(2)
        edge = self.graph.create_edge(node1, node2)
        self.assertIs(node1, edge.tail)
        self.assertIs(node2, edge.head)

    def test_get_node(self):
        node = self.graph.create_node(3)
        self.assertIs(self.graph.node(3), node)

    def test_nodes_are_returned_in_order(self):
        node2 = self.graph.create_node(2)
        node3 = self.graph.create_node(3)
        node1 = self.graph.create_node(1)
        nodes = self.graph.nodes()
        self.assertEqual(3, len(nodes))
        self.assertIs(nodes[0], node1)
        self.assertIs(nodes[1], node2)
        self.assertIs(nodes[2], node3)

    def test_keys_are_returned_ordered(self):
        self.graph.create_node(4)
        self.graph.create_node(8)
        self.graph.create_node(3)
        self.assertEqual(self.graph.keys(), [3, 4, 8])

    def test_count_of_nodes(self):
        self.graph.create_node(2)
        self.graph.create_node(3)
        self.assertEqual(2, self.graph.count())


