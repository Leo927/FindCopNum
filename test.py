# -*- coding: utf-8 -*-
import unittest
import networkx as nx
from rootedtree import RootedTree
import matplotlib.pyplot as plt
import copy
import treedrawer
import constant
import random
import copmanager
from label import Label, SV


class LabelTest(unittest.TestCase):
    def setUp(self):
        self.label = Label()
        self.label.append(1, 9)
        self.label.append(-5, constant.PERPEN_SYM)
    

    def test_index_is_ok(self):
        self.assertEqual(self.label[1].attribute, 9)
        self.assertEqual(self.label[2].key, -5)
        with self.assertRaises(IndexError):
            self.label[0]
        self.assertEqual(self.label[-1].key, -5)
        self.assertEqual(self.label[-2].key, 1)

    def test_next_unlabled(self):
        nodes = [5, 4, 3, 2, 1, 0]
        copmanager.labels = {5: Label(), 4: Label(), 3: None, 2: None, 1: None, 0: None}
        self.assertEqual(copmanager.nextUnlabled(nodes), 3)

    def test_split_contain_perpen(self):
        Ib = [4, 2, 1]
        I_perpen = [0, 3]
        copmanager.labels = {4: Label.make(1, 0),
                  3: Label.make(1, constant.PERPEN_SYM),
                  2: Label.make(2, 0),
                  1: Label.make(2, 0),
                  0: Label.make(1, constant.PERPEN_SYM)}
        self.assertEqual(copmanager.splitContainPerp(
            Ib+I_perpen), (I_perpen, Ib))

    def test_get_leading(self):
        LT1u = Label.make(6, constant.PERPEN_SYM)
        copmanager.labels = labels = {1: Label.make(5, constant.PERPEN_SYM), 2: Label.make(
            6, constant.PERPEN_SYM), 3: Label.make(4, 3), 4: Label.make(6, 4), 5: Label.make(7, 5)}
        I_perpen = [1, 2]
        nodes = [1, 2, 3, 4, 5]
        L = copmanager.getLeadingLabels(nodes, I_perpen, LT1u)
        self.assertEqual(L, [labels[4][1], labels[5][1], LT1u[1]])
        distinct, kStar = copmanager.keyRepeated(L)
        self.assertEqual(kStar, 6)
        self.assertEqual(sorted(distinct), [6, 7])

        K = copmanager.decreasingWithMinimum(distinct, kStar)
        self.assertEqual(K, [7, 6])
        h = copmanager.findh(K)
        K = copmanager.updateK(K, h)
        self.assertEqual(h, 1)
        self.assertEqual(K, [8])

        X = copmanager.findX(L, K)
        self.assertEqual(X, Label.make(8, constant.PERPEN_SYM, 0, 0, 0, 0))


class RepeatedKey(unittest.TestCase):
    def setUp(self):
        self.label = [SV(1, 0), SV(2, 0),  SV(
            5, 0), SV(5, constant.PERPEN_SYM)]

    def test_get_largest(self):
        distinct, largest = copmanager.keyRepeated(self.label)
        self.assertEqual(largest, 5)
        self.assertEqual(distinct, [1, 2, 5])


class RootedTreeManipulationTest(unittest.TestCase):
    def setUp(self):
        self.rt = RootedTree(nx.Graph(), 0)
        self.rt.tree.add_edges_from([(0, 1), (0, 2), (1, 3), (3, 4), (4, 5)])

    def test_descendent_check(self):
        self.assertEqual(copmanager.descendant(self.rt, 0), [1, 2])
        self.assertEqual(
            sorted(copmanager.descendant(self.rt, 0, 2)), [1, 2, 3])

    def test_subForest(self):
        rt1 = RootedTree(nx.Graph(), 1)
        rt1.tree.add_edges_from([(1, 3), (3, 4), (4, 5)])
        rt2 = RootedTree(nx.Graph(), 2)
        rt2.tree.add_node(2)
        self.assertEqual(
            str(copmanager.subForest(self.rt, 0)), str([rt1, rt2]))

        rt3 = RootedTree(nx.Graph(), 3)
        rt3.tree.add_edges_from([(3, 4), (4, 5)])
        self.assertEqual(str(copmanager.subForest(self.rt, 1)[0]), str(rt3))


class CopNumTest(unittest.TestCase):
    def test_empty_tree(self):
        tree = nx.Graph()
        tree.add_node(0)
        #self.assertEqual(copmanager.getCopNumber(tree), 0)

if __name__ == "__main__":
    unittest.main()
