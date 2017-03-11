import unittest

from challenges import Graph, Node, Edge


class NodeTestCase(unittest.TestCase):
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


class EdgeTestCase(unittest.TestCase):
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


class GraphTestCase(unittest.TestCase):
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

    def test_get_node(self):
        node = self.graph.create_node(3)
        self.assertIs(self.graph.get_node(3), node)
