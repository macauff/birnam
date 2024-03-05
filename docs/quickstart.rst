***********
Quick Start
***********

To get started quickly with ``birnam``, you will need a set of pre-run ``macauff`` cross-matches, each of which has a common catalogue on one side or other.

Input Data
==========

The input data is a set of cross-match results, some output files (match and non-match) per catalogue-catalogue counterpart association determination. These matches should all be in separate sub-folders in a given space on disk. ``birnam`` also requires knowledge of the location on disk of the primary input catalogue, jointly used as the input into each ``macauff`` cross-match in turn. As per ``macauff``, ``birnam`` assumes a "chunking" system has been used to break large datasets into smaller sky patches; in this case, all chunk sub-folders must agree on the naming convention used.

Input Parameters
================

The input parameters into ``birnam``'s ``SuperMatch`` class are:

``top_level_folder``

Place on disk where all cross-matches have been stored, from which to load two-catalogue composite associations and non-associations. Inside this folder there should be folders per cross-match, inside which will then be the sub-folder chunk directory.

``primary_catalogue_name``

The name of the "primary" catalogue, which must be present in all cross-matches within ``top_level_folder``.

``primary_catalogue_input_location``

Location on disk of the input file containing the catalogue files for the primary. Following ``macauff``, these files must be contained within sub-folders, one per chunk, for example::

    /primary/catalogue/input/location/chunk_folder/primary_catalogue_filename

with ``chunk_folder`` changing.

``primary_catalogue_input_column_id``

Common across all input catalogue chunks, this is the zero-indexed column number of the catalogue's ID, to be used to represent the objects across all output cross-match files and the eventual super-match output file.

``primary_catalogue_filename``

The name, including extension, of the primary catalogue file, common within each sub-chunk folder.

``super_match_save_folder``

Output folder into which to save the composite super-match files.

``list_of_catalogue_names``

A list of the *secondary* catalogues' names, to be saved into the output super-match file(s).

``list_of_secondary_match_folders``

A list, in the same order as ``list_of_catalogue_names``, if the folders within ``top_level_folder`` that contain each cross-match run. Will look something like::

    /top/level/folder/list_of_secondary_match_folders[j]

``list_of_match_filenames``

List, in catalogue-name order, of the filenames of the matched object output files. Should look something like::

    /top/level/folder/list_of_secondary_match_folders[j]/chunk_folder/list_of_match_filenames[j]

``list_of_non_match_filenames``

The same as ``list_of_match_filenames``, albeit for the non-match output table. Note, however, that this is the *primary* catalogue non-matches for each cross-match pair in ``list_of_catalogue_names``!

``list_of_match_primary_column_ids``

List, in catalogue-name order, of the zero-indexed columns of the primary catalogue's ID in the match output cross-match tables.

``list_of_match_secondary_column_ids``

List, in catalogue-name order, of the zero-indexed columns of the secondary catalogue's ID in the match output cross-match tables.

``list_of_match_probability_ids``

List, in catalogue-name order, of the zero-indexed columns of the match probability in the match output cross-match tables.

``list_of_non_match_primary_column_ids``

List, in catalogue-name order, of the zero-indexed columns of the primary catalogue's ID in the non-match output cross-match tables.

``list_of_non_match_probability_ids``

List, in catalogue-name order, of the zero-indexed columns of the (non-)match probability in the non-match output cross-match tables.

``n_pool``

Integer value for the number of threads to use in ``multiprocessing`` when iterating over chunks to generate super-matches for each chunk.

Running the Super-Match
=======================

Running the super-match is as easy as collating the required input parameters and calling the class

.. code-block:: python

    from birnam import SuperMatch

    SuperMatch('top_level_folder', 'primary_cat', 'catalogue_folder', 1, 'primary_catalogue.csv',
                   'super_match_save_folder', ['A', 'B'], ['cm_1', 'cm_2'], ['matches.csv', 'matches.csv'],
                   ['non_matches.csv', 'non_matches.csv'], [0, 0], [1, 1], [2, 2], [0, 0], [1, 1], 2)

Documentation
=============

For the full documentation, click :doc:`here<birnam>`.