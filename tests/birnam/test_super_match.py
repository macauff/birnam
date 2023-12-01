# Licensed under a 3-clause BSD style license - see LICENSE
'''
Tests for the "super_match" module.
'''

import os

import numpy as np
from numpy.testing import assert_allclose
from birnam import SuperMatch


class TestSuperMatch():
    def make_match_inputs_outputs(self, save_type, folder, columns, n_rows):
        os.makedirs(folder, exist_ok=True)
        primary_ID = columns[0]
        if save_type == 'matches':
            secondary_ID = columns[1]
            prob = columns[2]
        if save_type == 'non-matches':
            prob = columns[1]

        if save_type == 'input_catalogue':
            text = ''
            for i in range(n_rows):
                text = text + f'{i},{primary_ID[i]}\n'
            with open(f'{folder}/primary_catalogue.csv', 'w') as file:
                file.write(text)
        if save_type == 'matches':
            text = ''
            for i in range(n_rows):
                text = text + f'{primary_ID[i]},{secondary_ID[i]},{prob[i]}\n'
            with open(f'{folder}/matches.csv', 'w') as file:
                file.write(text)
        if save_type == 'non-matches':
            text = ''
            for i in range(n_rows):
                text = text + f'{primary_ID[i]},{prob[i]}\n'
            with open(f'{folder}/non_matches.csv', 'w') as file:
                file.write(text)

    def test_good_run(self):
        # TODO: pad the make_match_inputs_outputs with fake astrometry/photometry to change
        # which column each ID is.
        # TODO: pass filenames to make_match_inputs_outputs to simulate different output names.
        os.system('rm -r catalogue_folder')
        os.system('rm -r top_level_folder')
        os.system('rm -r  super_match_save_folder')
        primary_ids = []
        secondary_ids = []
        probabilities = []
        for i in range(3):
            rng = np.random.default_rng(seed=5478345)
            n_rows = rng.choice(11) + 14
            primary_ID = ['ID_{}'.format(x) for x in rng.choice(9999, size=n_rows)]
            primary_ids.append(primary_ID)
            self.make_match_inputs_outputs('input_catalogue', f'catalogue_folder/chunk_{i}',
                                           [primary_ID], n_rows)
            _2nd_ids = []
            _probs = []
            for j, ID_format in zip([1, 2], ['J_{}', 'G_{}']):
                n_matches = rng.choice(n_rows-int(0.6 * n_rows)) + int(0.6 * n_rows)
                n_nonmatches = n_rows - n_matches
                secondary_ID = [ID_format.format(x) for x in rng.choice(9999, size=n_matches)]
                _2nd_ids.append(secondary_ID)
                probs = rng.uniform(0, 1, size=n_rows)
                _probs.append(probs)
                self.make_match_inputs_outputs(
                    'matches', f'top_level_folder/cm_{j}/chunk_{i}/pairing',
                    [primary_ID[:n_matches], secondary_ID, probs[:n_matches]], n_matches)
                self.make_match_inputs_outputs(
                    'non-matches', f'top_level_folder/cm_{j}/chunk_{i}/pairing',
                    [primary_ID[n_matches:], probs[n_matches:]], n_nonmatches)
            secondary_ids.append(_2nd_ids)
            probabilities.append(_probs)

        SuperMatch('top_level_folder', 'primary_cat', 'catalogue_folder',
                   1, 'primary_catalogue.csv',
                   'super_match_save_folder', ['A', 'B'], ['cm_1', 'cm_2'],
                   'pairing', ['matches.csv', 'matches.csv'],
                   ['non_matches.csv', 'non_matches.csv'], [0, 0], [1, 1], [2, 2], [0, 0], [1, 1])

        for i in range(3):
            assert os.path.exists(f'super_match_save_folder/chunk_{i}/primary_cat_super_match.csv')

            # Avoid re-loading the file with e.g. Pandas and simply check the
            # lines "by hand".
            with open(f'super_match_save_folder/chunk_{i}/primary_cat_super_match.csv', 'r') as f:
                for j, line in enumerate(f.readlines()):
                    pid, id1, id2, p, cat_bad, p_bad = line.split(',')
                    assert pid == primary_ids[i][j]
                    if j < len(secondary_ids[i][0]):
                        assert id1 == secondary_ids[i][0][j]
                    else:
                        assert id1 == 'N/A'
                    if j < len(secondary_ids[i][1]):
                        assert id2 == secondary_ids[i][1][j]
                    else:
                        assert id2 == 'N/A'
                    assert_allclose(float(p),
                                    float(probabilities[i][0][j])*float(probabilities[i][1][j]))
