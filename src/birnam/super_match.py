# Licensed under a 3-clause BSD style license - see LICENSE
'''
This module provides the high-level framework for the creation of multi-catalogue
"super-matches" for one primary dataset.
'''

import itertools
import multiprocessing
import os

import numpy as np
import pandas as pd


class SuperMatch():
    '''
    A class to create super-matches, the mergers of multiple associations to
    one photometric catalogue across a number of other datasets.

    Parameters
    ----------
    top_level_folder : string
        Location on disk of the folder containing all of the individual
        two-catalogue cross-matches, from which the super-match should be built.
    primary_catalogue_name : string
        The name of the "primary" photometric catalogue, to which all other
        datasets have been cross-matched.
    primary_catalogue_input_location : string
        Location on disk where the primary catalogue is saved, from which to
        extract the list of IDs
    primary_catalogue_input_column_id : int
        The zero-indexed column number of the primary catalogue's ID in the
        input catalogue.
    primary_catalogue_filename : string
        Name of the input dataset of the primary catalogue on disk (including
        extension), from which all cross-matches are performed to each secondary
        dataset.
    super_match_save_folder : string
        Location on disk to which to save out the resulting super-match table.
    list_of_catalogue_names : list or numpy.ndarray of strings
        The names of each catalogue that was cross-matched to
        ``primary_catalogue_name``.
    list_of_secondary_match_folders : list or numpy.ndarray of strings
        List of the locations on disk of where each respective cross-match,
        ``primary_catalogue_name``-to-``list_of_catalogues``, has been saved,
        inside ``top_level_folder``, in the same order as ``list_of_catalogues``.
    list_of_match_filenames : list or numpy.ndarray of strings
        The filename, including extension, of each respective cross-match's
        "match" output file.
    list_of_non_match_filenames : list or numpy.ndarray of strings
        The filename, including extension, of each respective cross-match's
        primary "non-match" output file.
    list_of_match_primary_column_ids : list or numpy.ndarray of ints
        For each respective cross-match, the list should contain the
        zero-indexed column of the ID of the primary catalogue in the match
        table.
    list_of_match_secondary_column_ids : list or numpy.ndarray of ints
        For each respective cross-match, the list should contain the
        zero-indexed column of the ID of the "other", non-primary catalogue in
        the match table.
    list_of_match_probability_ids : list or numpy.ndarray of ints
        For each cross-match run, the zero-indexed column number of the overall
        match probability.
    list_of_non_match_primary_column_ids : list or numpy.ndarray of ints
        For each respective cross-match run, the list should contain the
        zero-indexed column of the ID of the primary catalogue in its non-match
        output table.
    list_of_non_match_probability_ids : list or numpy.ndarray of ints
        For each cross-match run, the zero-indexed column number of the
        probability of the primary source's non-match to the respective
        catalogues.
    n_pool : integer
        Number of threads to use for chunk-level super-match multiprocessing.
    '''

    def __init__(self, top_level_folder, primary_catalogue_name, primary_catalogue_input_location,
                 primary_catalogue_input_column_id, primary_catalogue_filename,
                 super_match_save_folder, list_of_catalogue_names, list_of_secondary_match_folders,
                 list_of_match_filenames, list_of_non_match_filenames,
                 list_of_match_primary_column_ids, list_of_match_secondary_column_ids,
                 list_of_match_probability_ids, list_of_non_match_primary_column_ids,
                 list_of_non_match_probability_ids, n_pool):
        '''
        At the top level of the super-match we assume that *all* cross-matches
        have the same structure within their top-level folder, so we might have
        /top/level/folder/match_pair_folder/chunk_folder/match_name
        for all match pairs and all chunks, and
        /primary/catalogue/input/location/chunk_folder/primary_catalogue_filename
        for all chunks (and hence the same primary catalogue was used in every
        cross-match: primary-A, primary-B, primary-C, ...).

        All chunks within a single cross-match should have the same column
        IDs, so list_of_*_ids will pass through the chunking parallelisation.
        Similarly names should be consistent across chunks, so
        primary_catalogue_name and list_of_catalogue_names should be constant,
        as should list_of_match_filenames and list_of_non_match_filenames.

        So we need to generate, on a per-chunk basis, the primary catalogue input
        location, the super-match output folder, and the list of the output
        cross-match folders from which to load data to create the super-match,
        from our search pattern inputs.
        '''

        # Determine the chunk folders from the primary input catalogue folder,
        # since they should all be enforced to be the same.
        chunk_folders = os.listdir(primary_catalogue_input_location)

        # TODO: folder creation, checking, etc.  # pylint: disable=fixme
        counter = np.arange(0, len(chunk_folders))
        expand_constants = [itertools.repeat(item) for item in [
            primary_catalogue_input_location, chunk_folders, primary_catalogue_filename, top_level_folder,
            list_of_secondary_match_folders, super_match_save_folder, primary_catalogue_name,
            primary_catalogue_input_column_id, list_of_catalogue_names, list_of_match_filenames,
            list_of_non_match_filenames, list_of_match_primary_column_ids,
            list_of_match_secondary_column_ids, list_of_match_probability_ids,
            list_of_non_match_primary_column_ids, list_of_non_match_probability_ids]]
        iter_group = zip(counter, *expand_constants)
        with multiprocessing.Pool(n_pool) as pool:
            for _ in pool.imap_unordered(self.single_chunk_super_match, iter_group,
                                         chunksize=max(1, len(counter) // n_pool)):
                pass

    def single_chunk_super_match(self, p):
        '''
        Helper function for the parallel loop, extracting a individual chunks
        and passing through to the single-chunk function.

        Parameters
        ----------
        p : list
            List of the variables needed to extract one chunk's information.
        '''
        [i, primary_catalogue_input_location, chunk_folders, primary_catalogue_filename, top_level_folder,
         list_of_secondary_match_folders, super_match_save_folder, primary_catalogue_name,
         primary_catalogue_input_column_id, list_of_catalogue_names, list_of_match_filenames,
         list_of_non_match_filenames, list_of_match_primary_column_ids,
         list_of_match_secondary_column_ids, list_of_match_probability_ids,
         list_of_non_match_primary_column_ids, list_of_non_match_probability_ids] = p
        # /primary/catalogue/input/location/chunk_folder/primary_catalogue_filename
        primary_catalogue_chunk_location = os.path.join(
            primary_catalogue_input_location, chunk_folders[i], primary_catalogue_filename)
        # /top/level/folder/match_pair_folder/chunk_folder/
        list_of_secondary_chunk_folders = [
            os.path.join(top_level_folder, list_of_secondary_match_folders[j], chunk_folders[i])
            for j in range(len(list_of_secondary_match_folders))]
        # /super/match/save/folder/chunk_folder/name_super_match.csv
        super_match_chunk_save_filename = os.path.join(
            super_match_save_folder, chunk_folders[i],
            f'{primary_catalogue_name}_super_match.csv')
        os.makedirs(os.path.dirname(super_match_chunk_save_filename), exist_ok=True)
        self.run_super_match(
            primary_catalogue_name, primary_catalogue_chunk_location,
            primary_catalogue_input_column_id, super_match_chunk_save_filename,
            list_of_catalogue_names, list_of_secondary_chunk_folders, list_of_match_filenames,
            list_of_non_match_filenames, list_of_match_primary_column_ids,
            list_of_match_secondary_column_ids, list_of_match_probability_ids,
            list_of_non_match_primary_column_ids, list_of_non_match_probability_ids)

    def run_super_match(self, primary_catalogue_name, primary_catalogue_input_location,
                        primary_catalogue_input_column_id, super_match_save_filename,
                        list_of_catalogue_names, list_of_cross_match_folders,
                        list_of_match_filenames, list_of_non_match_filenames,
                        list_of_match_primary_column_ids, list_of_match_secondary_column_ids,
                        list_of_match_probability_ids, list_of_non_match_primary_column_ids,
                        list_of_non_match_probability_ids):
        '''
        Function to run the creation of a single chunk of a super-match.

        Parameters
        ----------
        primary_catalogue_name : string
            The name of the "primary" photometric catalogue, to which all other
            datasets have been cross-matched.
        primary_catalogue_input_location : string
            Location on disk where the primary catalogue is saved, from which to
            extract the list of IDs
        primary_catalogue_input_column_id : int
            The zero-indexed column number of the primary catalogue's ID in the
            input catalogue.
        super_match_save_filename : string
            Location on disk to which to save out the resulting super-match table.
        list_of_catalogue_names : list or numpy.ndarray of strings
            The names of each catalogue that was cross-matched to
            ``primary_catalogue_name``.
        list_of_cross_match_folders : list or numpy.ndarray of strings
            List of the locations on disk of where each respective cross-match,
            ``primary_catalogue_name``-to-``list_of_catalogue_names``, has been
            saved, in the same order as ``list_of_catalogue_names``.
        list_of_match_filenames : list or numpy.ndarray of strings
            The filename, including extension, of each respective cross-match's
            "match" output file.
        list_of_non_match_filenames : list or numpy.ndarray of strings
            The filename, including extension, of each respective cross-match's
            primary "non-match" output file.
        list_of_match_primary_column_ids : list or numpy.ndarray of ints
            For each respective cross-match, the list should contain the
            zero-indexed column of the ID of the primary catalogue in the match
            table.
        list_of_match_secondary_column_ids : list or numpy.ndarray of ints
            For each respective cross-match, the list should contain the
            zero-indexed column of the ID of the "other", non-primary catalogue in
            the match table.
        list_of_match_probability_ids : list or numpy.ndarray of ints
            For each cross-match run, the zero-indexed column number of the overall
            match probability.
        list_of_non_match_primary_column_ids : list or numpy.ndarray of ints
            For each respective cross-match run, the list should contain the
            zero-indexed column of the ID of the primary catalogue in its non-match
            output table.
        list_of_non_match_probability_ids : list or numpy.ndarray of ints
            For each cross-match run, the zero-indexed column number of the
            probability of the primary source's non-match to the respective
            catalogues.
        '''

        # Create output data array in memory.
        primary_input_catalogue_ids = self.load_catalogue_column(
            primary_catalogue_input_location, primary_catalogue_input_column_id)
        n_rows = len(primary_input_catalogue_ids)
        # shape should be n_rows by (primary ID, ID*n, p_tot, ID_bad, and p_bad),
        # but the structured array handles the column width internally.
        shape = (n_rows,)
        dtype = [(f'{primary_catalogue_name} ID', object),
                 *((f'{secondary_catalogue_name} ID', object) for secondary_catalogue_name in
                   list_of_catalogue_names),
                 ('Probability', float), ('Bad catalogue', object),
                 ('Probability without bad catalogue', float)]

        super_match = np.empty(shape=shape, dtype=dtype)

        # Populate left-hand primary ID, p(tot) = 1, p(without bad) = 1.
        super_match[f'{primary_catalogue_name} ID'] = primary_input_catalogue_ids
        super_match['Probability'] = 1
        super_match['Probability without bad catalogue'] = 1
        super_match['Bad catalogue'] = 'N/A'

        # Loop over catalogues, updating ID and p(tot), also updating
        # p(without bad) and bad_ID.
        for i in range(len(list_of_catalogue_names)):  # pylint: disable=consider-using-enumerate
            # Extract the match and non-match IDs (match x2, non-match x1) and
            # (non-)match probabilities.
            primary_match_ids = self.load_catalogue_column(
                os.path.join(list_of_cross_match_folders[i], list_of_match_filenames[i]),
                list_of_match_primary_column_ids[i])
            secondary_match_ids = self.load_catalogue_column(
                os.path.join(list_of_cross_match_folders[i], list_of_match_filenames[i]),
                list_of_match_secondary_column_ids[i])
            match_probs = self.load_catalogue_column(
                os.path.join(list_of_cross_match_folders[i], list_of_match_filenames[i]),
                list_of_match_probability_ids[i])

            primary_non_match_ids = self.load_catalogue_column(
                os.path.join(list_of_cross_match_folders[i], list_of_non_match_filenames[i]),
                list_of_non_match_primary_column_ids[i])
            non_match_probs = self.load_catalogue_column(
                os.path.join(list_of_cross_match_folders[i], list_of_non_match_filenames[i]),
                list_of_non_match_probability_ids[i])

            for j in range(len(primary_match_ids)):  # pylint: disable=consider-using-enumerate
                ind = np.where(primary_match_ids[j] == primary_input_catalogue_ids)[0][0]
                super_match[
                    f'{list_of_catalogue_names[i]} ID'][ind] = secondary_match_ids[j]
                super_match['Probability'][ind] *= match_probs[j]

                # If this is the worst posterior we've seen -- but it's also
                # below 50% -- then we change the 'bad catalogue' columns,
                # otherwise we just keep ticking that extra posterior over.
                # TODO: relax hard-coded 50% criterion for 'badness'.  # pylint: disable=fixme
                if (match_probs[j] < super_match['Probability without bad catalogue'][ind] and
                        match_probs[j] < 0.5):
                    super_match['Probability without bad catalogue'][ind] = super_match[
                        'Probability'][ind] / match_probs[j]
                    super_match['Bad catalogue'][ind] = list_of_catalogue_names[i]
                else:
                    super_match['Probability without bad catalogue'][ind] *= match_probs[j]

            for j in range(len(primary_non_match_ids)):  # pylint: disable=consider-using-enumerate
                ind = np.where(primary_non_match_ids[j] == primary_input_catalogue_ids)[0][0]
                super_match[f'{list_of_catalogue_names[i]} ID'][ind] = 'N/A'
                super_match['Probability'][ind] *= non_match_probs[j]

                if (non_match_probs[j] < super_match[
                        'Probability without bad catalogue'][ind] and non_match_probs[j] < 0.5):
                    super_match['Probability without bad catalogue'][ind] = super_match[
                        'Probability'][ind] / non_match_probs[j]
                    super_match['Bad catalogue'][ind] = list_of_catalogue_names[i]
                else:
                    super_match['Probability without bad catalogue'][ind] *= non_match_probs[j]

        # Save out via Pandas DataFrame.
        # dtype is a list of tuples of (name, dtype), so we can just pull the
        # column names from the list directly.
        x = pd.DataFrame(super_match, columns=[p[0] for p in dtype])
        x.to_csv(super_match_save_filename, encoding='utf-8', index=False, header=False)

    def load_catalogue_column(self, loc, id_):
        '''
        Load a single column from a catalogue on disk into memory.

        Parameters
        ----------
        loc : string
            Full location on disk of file to load a single column of.
        id_ : int
            The zero-indexed column of the file at ``loc`` to load.

        Returns
        -------
        csv_column : numpy.ndarray
            One-dimensional array of the value in the chosen ``ID``-th column
            in each row of the file.
        '''
        # TODO: relax .csv hard-coded assumption.  # pylint: disable=fixme
        # TODO: add header toggle.  # pylint: disable=fixme
        csv_column = pd.read_csv(loc, header=None, usecols=[id_])[id_].values
        return csv_column
