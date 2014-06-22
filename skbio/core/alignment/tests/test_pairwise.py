# ----------------------------------------------------------------------------
# Copyright (c) 2013--, scikit-bio development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
# ----------------------------------------------------------------------------

from __future__ import absolute_import, division, print_function

from unittest import TestCase, main

from skbio import (
    global_pairwise_align_protein, local_pairwise_align_protein,
    global_pairwise_align_nucleotide, local_pairwise_align_nucleotide)
from skbio.core.alignment.pairwise import (make_nt_substitution_matrix)


class PairwiseAlignmentTests(TestCase):
    """
        Note: In the high-level tests, the expected results were derived with
        assistance from the EMBOSS web server:
        http://www.ebi.ac.uk/Tools/psa/emboss_needle/
        http://www.ebi.ac.uk/Tools/psa/emboss_water/
        In some cases, placement of non-gap characters surrounded by gap
        characters are slighly different between scikit-bio and the EMBOSS
        server. These differences arise from arbitrary implementation
        differences, and always result in the same score (which tells us that
        the alignments are equivalent). In cases where the expected results
        included here differ from those generated by the EMBOSS server, I note
        the EMBOSS result as a comment below the expected value.

    """

    def test_make_nt_substitution_matrix(self):
        expected = {'A': {'A':  1, 'C': -2, 'G': -2, 'T': -2},
                          'C': {'A': -2, 'C':  1, 'G': -2, 'T': -2},
                          'G': {'A': -2, 'C': -2, 'G':  1, 'T': -2},
                          'T': {'A': -2, 'C': -2, 'G': -2, 'T':  1}}
        self.assertEqual(make_nt_substitution_matrix(1, -2), expected)

        expected = {'A': {'A':  5, 'C': -4, 'G': -4, 'T': -4},
                          'C': {'A': -4, 'C':  5, 'G': -4, 'T': -4},
                          'G': {'A': -4, 'C': -4, 'G':  5, 'T': -4},
                          'T': {'A': -4, 'C': -4, 'G': -4, 'T':  5}}
        self.assertEqual(make_nt_substitution_matrix(5, -4), expected)


    def test_global_pairwise_align_protein(self):
        expected = ("HEAGAWGHEE", "---PAWHEAE", 1.0)
        actual = global_pairwise_align_protein("HEAGAWGHEE", "PAWHEAE",
                                               gap_open_penalty=10.,
                                               gap_extend_penalty=5.)
        self.assertEqual(actual, expected)

        expected = ("HEAGAWGHE-E", "---PAW-HEAE", 24.0)
        # EMBOSS result: P---AW-HEAE
        actual = global_pairwise_align_protein("HEAGAWGHEE", "PAWHEAE",
                                               gap_open_penalty=5.,
                                               gap_extend_penalty=0.5)
        self.assertEqual(actual, expected)

    def test_local_pairwise_align_protein(self):
        expected = ("AWGHE", "AW-HE", 26.0, 4, 1)
        actual = local_pairwise_align_protein("HEAGAWGHEE", "PAWHEAE",
                                               gap_open_penalty=10.,
                                               gap_extend_penalty=5.)
        self.assertEqual(actual, expected)

        expected = ("AWGHE-E", "AW-HEAE", 32.0, 4, 1)
        actual = local_pairwise_align_protein("HEAGAWGHEE", "PAWHEAE",
                                               gap_open_penalty=5.,
                                               gap_extend_penalty=0.5)
        self.assertEqual(actual, expected)

    def test_global_pairwise_align_nucleotide(self):
        m = make_nt_substitution_matrix(5, -4)
        expected = ("G-ACCTTGACCAGGTACC", "GAACTTTGAC---GTAAC", 31.0)
        actual = global_pairwise_align_nucleotide("GACCTTGACCAGGTACC",
                                                  "GAACTTTGACGTAAC",
                                                  gap_open_penalty=10.,
                                                  gap_extend_penalty=0.5,
                                                  substitution_matrix=m)
        self.assertEqual(actual, expected)
    #     expected = ("", "", )
    #     actual = global_pairwise_align_nucleotide("", "",
    #                                            gap_open_penalty=10.,
    #                                            gap_extend_penalty=5.)
    #     self.assertEqual(actual, expected)
    #
    #     expected = ("", "", )
    #     actual = global_pairwise_align_nucleotide("", "",
    #                                            gap_open_penalty=5.,
    #                                            gap_extend_penalty=0.5)
    #     self.assertEqual(actual, expected)

    def test_local_pairwise_align_nucleotide(self):
        m = make_nt_substitution_matrix(2, -3)
        expected = ("ACCTTGAC", "ACTTTGAC", 11, 1, 2)
        actual = local_pairwise_align_nucleotide("GACCTTGACCAGGTACC",
                                                  "GAACTTTGACGTAAC",
                                                  gap_open_penalty=5.,
                                                  gap_extend_penalty=2.,
                                                  substitution_matrix=m)
        self.assertEqual(actual, expected)
