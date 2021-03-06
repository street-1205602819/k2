#!/usr/bin/env python3
#
# Copyright (c)  2020  Xiaomi Corporation (author: Haowen Qiu)
#
# See ../../../LICENSE for clarification regarding multiple authors

# To run this single test, use
#
#  ctest --verbose -R intersect_test_py
#

import unittest

import torch

import k2


class TestIntersection(unittest.TestCase):

    def test_case_1(self):
        # empty fsa
        array_size = k2.IntArray2Size(0, 0)
        fsa_a = k2.Fsa.create_fsa_with_size(array_size)
        fsa_b = k2.Fsa.create_fsa_with_size(array_size)
        intersection = k2.Intersection(fsa_a, fsa_b)
        array_size = k2.IntArray2Size()
        intersection.get_sizes(array_size)
        fsa_out = k2.Fsa.create_fsa_with_size(array_size)
        arc_map_a = k2.IntArray1.create_array_with_size(array_size.size2)
        arc_map_b = k2.IntArray1.create_array_with_size(array_size.size2)
        status = intersection.get_output(fsa_out, arc_map_a, arc_map_b)
        self.assertTrue(status)
        self.assertTrue(k2.is_empty(fsa_out))
        self.assertTrue(arc_map_a.empty())
        self.assertTrue(arc_map_b.empty())

        # test without arc_map
        status = intersection.get_output(fsa_out)
        self.assertTrue(status)
        self.assertTrue(k2.is_empty(fsa_out))

    def test_case_2(self):
        s_a = r'''
        0 1 1
        1 2 0
        1 3 1
        1 4 2
        2 2 1
        2 3 1
        2 3 2
        3 3 0
        3 4 1
        4
        '''

        fsa_a = k2.str_to_fsa(s_a)

        s_b = r'''
        0 1 1
        1 3 1
        1 2 2
        2 3 1
        3
        '''

        fsa_b = k2.str_to_fsa(s_b)
        intersection = k2.Intersection(fsa_a, fsa_b)
        array_size = k2.IntArray2Size()
        intersection.get_sizes(array_size)
        fsa_out = k2.Fsa.create_fsa_with_size(array_size)
        arc_map_a = k2.IntArray1.create_array_with_size(array_size.size2)
        arc_map_b = k2.IntArray1.create_array_with_size(array_size.size2)
        status = intersection.get_output(fsa_out, arc_map_a, arc_map_b)
        self.assertTrue(status)
        expected_arc_indexes = torch.IntTensor([0, 1, 4, 7, 8, 8, 8, 10, 10])
        expected_arcs = torch.IntTensor([[0, 1, 1], [1, 2, 0], [1, 3, 1],
                                         [1, 4, 2], [2, 5, 1], [2, 3, 1],
                                         [2, 6, 2], [3, 3, 0], [6, 6, 0],
                                         [6, 7, 1]])
        expected_arc_map_a = torch.IntTensor([0, 1, 2, 3, 4, 5, 6, 7, 7, 8])
        expected_arc_map_b = torch.IntTensor([0, -1, 1, 2, 1, 1, 2, -1, -1, 3])
        self.assertTrue(torch.equal(fsa_out.indexes, expected_arc_indexes))
        self.assertTrue(torch.equal(fsa_out.data, expected_arcs))
        self.assertTrue(torch.equal(arc_map_a.data, expected_arc_map_a))
        self.assertTrue(torch.equal(arc_map_b.data, expected_arc_map_b))


if __name__ == '__main__':
    unittest.main()
