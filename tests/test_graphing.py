try:
    from builtins import object
except ImportError:
    pass

from transitions import Machine, MachineError
from transitions import HierarchicalMachine
from unittest import TestCase
import tempfile
import os


class TestDiagrams(TestCase):

    def test_agraph_diagram(self):
        states = ['A', 'B', 'C', 'D']
        transitions = [
            {'trigger': 'walk', 'source': 'A', 'dest': 'B'},
            {'trigger': 'run', 'source': 'B', 'dest': 'C'},
            {'trigger': 'sprint', 'source': 'C', 'dest': 'D'}
        ]

        m = Machine(states=states, transitions=transitions, initial='A')
        graph = m.get_graph()

        # Test that graph properties match the Machine
        self.assertEqual(
            set(m.states.keys()), set([n.name for n in graph.nodes()]))
        triggers = set([n.attr['label'] for n in graph.edges()])
        for t in triggers:
            self.assertIsNotNone(getattr(m, t))

        # check for a valid pygraphviz diagram
        self.assertIsNotNone(graph)
        self.assertTrue("digraph" in str(graph))

        # write diagram to temp file
        target = tempfile.NamedTemporaryFile()
        graph.draw(target.name, prog='dot')
        self.assertTrue(os.path.getsize(target.name) > 0)

        # cleanup temp file
        target.close()

    def test_nested_agraph_diagram(self):
        ''' Same as above, but with nested states. '''
        states = ['A', 'B', {'name': 'C', 'children': ['1', '2', '3']}, 'D']
        transitions = [
            {'trigger': 'walk', 'source': 'A', 'dest': 'B'},
            {'trigger': 'run', 'source': 'B', 'dest': 'C'},
            {'trigger': 'sprint', 'source': 'C', 'dest': 'D'}
        ]

        m = HierarchicalMachine(states=states, transitions=transitions, initial='A')
        graph = m.get_graph()

        # Test that graph properties match the Machine
        # print((set(m.states.keys()), )
        node_names = set([n.name for n in graph.nodes()])
        self.assertEqual(set(m.states.keys()) - set('C'), node_names)
        triggers = set([n.attr['label'] for n in graph.edges()])
        for t in triggers:
            self.assertIsNotNone(getattr(m, t))

        # check for a valid pygraphviz diagram
        self.assertIsNotNone(graph)
        self.assertTrue("digraph" in str(graph))

        # write diagram to temp file
        target = tempfile.NamedTemporaryFile()
        graph.draw(target.name, prog='dot')
        self.assertTrue(os.path.getsize(target.name) > 0)

        # cleanup temp file
        target.close()
