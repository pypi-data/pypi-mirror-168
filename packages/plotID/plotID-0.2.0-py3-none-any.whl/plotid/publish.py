#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Publish a tagged plot along the corresponding research data.

Export the tagged figure to a directory that also contains the raw data where
the plot is based on. Additionally, the script that produced the plot will be
copied to the destination directory.

Functions:
    publish(PlotIDTransfer object, str or list of str, str or list of str)
    -> None
"""

import os
import shutil
import sys
import warnings
from plotid.save_plot import save_plot
from plotid.plotoptions import PlotIDTransfer


class PublishOptions:
    """
    Container objects which include all publish options provided by plotid.

    Methods
    -------
    __init__
    validate_input
        Check if input is correct type.
    export
        Export the plot and copy specified files to the destiantion folder.
    """

    def __init__(self, figs_and_ids, src_datapaths, dst_path, plot_names,
                 **kwargs):

        if not isinstance(figs_and_ids, PlotIDTransfer):
            raise RuntimeError('figs_and_ids is not an instance of '
                               'PlotIDTransfer.')
        self.figure = figs_and_ids.figs
        self.figure_ids = figs_and_ids.figure_ids
        self.src_datapaths = src_datapaths
        self.dst_path = dst_path
        self.plot_names = plot_names
        self.data_storage = kwargs.get('data_storage', 'individual')
        self.dst_path_head, self.dst_dirname = os.path.split(self.dst_path)

        # If the second string after os.path.split is empty,
        # a trailing slash was given.
        # To get the dir name correctly, split the first string again.
        if not self.dst_dirname:
            self.dst_path_head, self.dst_dirname = os.path.split(
                self.dst_path_head)

    def __str__(self):
        """Representation if an object of this class is printed."""
        return str(self.__class__) + ": " + str(self.__dict__)

    def validate_input(self):
        """
        Validate if input for PublishOptions is correct type.

        Raises
        ------
        FileNotFoundError
            If the path to the source or the destination directory does not
            exist.
        TypeError
            If input data is of wrong type.

        Returns
        -------
        None.

        """
        # Check if IDs are str
        if isinstance(self.figure_ids, str):
            self.figure_ids = [self.figure_ids]
        if isinstance(self.figure_ids, list):
            for identifier in self.figure_ids:
                if not isinstance(identifier, str):
                    raise TypeError('The list of figure_ids contains an object'
                                    ' which is not a string.')
        else:
            raise TypeError('The specified figure_ids are neither a string nor'
                            ' a list of strings.')

        if not os.path.isfile(sys.argv[0]):
            raise FileNotFoundError('Cannot copy original python script. '
                                    'Running publish from a shell is not '
                                    'possible.')

        if isinstance(self.src_datapaths, str):
            self.src_datapaths = [self.src_datapaths]
        if isinstance(self.src_datapaths, list):
            for path in self.src_datapaths:
                if not isinstance(path, str):
                    raise TypeError(f'{path} is not a string.')
                # Check if source directory and files exist
                if not os.path.exists(path):
                    raise FileNotFoundError('The specified source directory'
                                            f'/file {path} does not exist.')
        else:
            raise TypeError('The source directory/files are neither '
                            'a string nor a list.')

        # Check if destination directory is allowed path
        if not os.path.exists(self.dst_path_head):
            raise FileNotFoundError('The specified destination directory '
                                    'does not exist.')

        # Check if plot_name is a string or a list of strings
        if isinstance(self.plot_names, str):
            self.plot_names = [self.plot_names]
        if isinstance(self.plot_names, list):
            for name in self.plot_names:
                if not isinstance(name, str):
                    raise TypeError('The list of plot_names contains an object'
                                    ' which is not a string.')
        else:
            raise TypeError('The specified plot_names is neither a string nor'
                            ' a list of strings.')

        # Check if data_storage is a string
        if not isinstance(self.data_storage, str):
            raise TypeError('The specified data_storage method is not a '
                            'string.')

    def export(self):
        """
        Export the plot and copy specified files to the destination folder.

        Raises
        ------
        RuntimeError
            If user does not want to overwrite existing folder.
        ValueError
            If non-supported data_storage method is given.

        Returns
        -------
        None.

        """
        # Export plot figure to picture.
        plot_paths = save_plot(self.figure, self.plot_names)
        print(plot_paths)
        match self.data_storage:
            case 'centralized':
                self.centralized_data_storage()
            case 'individual':
                for i, plot in enumerate(plot_paths):
                    try:
                        # Create folder with ID as name
                        dst_path = os.path.join(self.dst_path,
                                                self.figure_ids[i])
                        dst_path_invisible = os.path.join(self.dst_path, '.'
                                                          + self.figure_ids[i])

                        # If dir with the same ID already exists ask user
                        # if it should be overwritten.
                        if os.path.isdir(dst_path):
                            warnings.warn(f'Folder "{dst_path}" already exists'
                                          ' – plot has already been published.'
                                          )
                            overwrite_dir = input('Do you want to overwrite '
                                                  'the existing folder? '
                                                  '(yes/no[default])\n')
                            if overwrite_dir in ('yes', 'y'):
                                shutil.rmtree(dst_path)
                            else:
                                raise RuntimeError('publish has finished '
                                                   'without an export.\nRerun '
                                                   'tagplot if you need a new'
                                                   ' ID or consider '
                                                   'overwriting.')

                        self.individual_data_storage(dst_path_invisible, plot)
                        # If export was successful, make the directory visible
                        os.rename(dst_path_invisible, dst_path)
                    except FileExistsError as exc:
                        delete_dir = input('There was an error while '
                                           'publishing the data. Should the '
                                           'partially copied data at '
                                           f'{dst_path_invisible} be'
                                           ' removed? (yes/no[default])\n')
                        if delete_dir in ('yes', 'y'):
                            shutil.rmtree(dst_path_invisible)
                        raise RuntimeError('Publishing was unsuccessful. '
                                           'Try re-running publish.') from exc
            case _:
                raise ValueError(f'The data storage method {self.data_storage}'
                                 ' is not available.')

        print(f'Publish was successful.\nYour plot(s), your'
              f' data and your\nscript {sys.argv[0]}'
              f'\nwere copied to {self.dst_path}.')

    def centralized_data_storage(self):
        """
        [not implemented yet].

        Store the data only in one directory and link all others to it.

        Returns
        -------
        None.

        """
        # Does nothing, not implemented yet

    def individual_data_storage(self, destination, pic_path):
        """
        Store all the data in an individual directory.

        Parameters
        ----------
        destination : str
            Directory where the data should be stored.
        pic_paths : list
            Paths to the picture file that will be stored in destination.

        Returns
        -------
        None.

        """
        # Copy all files to destination directory
        print('Copying data has been started. Depending on the size of'
              ' your data this may take a while...')
        os.makedirs(destination)
        # Copy data to destination folder
        for path in self.src_datapaths:
            try:
                shutil.copytree(path, destination, dirs_exist_ok=True)
            except NotADirectoryError:
                shutil.copy2(path, destination)

        # Copy script that calls this function to folder
        shutil.copy2(sys.argv[0], destination)

        if os.path.isfile(pic_path):
            # Copy plot file to folder
            shutil.copy2(pic_path, destination)
            # Remove by plotID exported .tmp plot
            os.remove(pic_path)
            # Remove .tmp. from file name in destinaion
            name_tmp, orig_ext = os.path.splitext(pic_path)
            orig_name, _ = os.path.splitext(name_tmp)
            final_file_path = orig_name + orig_ext
            os.rename(os.path.join(destination, pic_path),
                      os.path.join(destination, final_file_path))


def publish(figs_and_ids, src_datapath, dst_path, plot_name, **kwargs):
    """
    Save plot, data and measuring script.

    Parameters
    ----------
    figs_and_ids : PlotIDTransfer object
        Contains figures tagged by tagplot() and their corresponding IDs.
    src_datapath : str or list of str
        Path to data that should be published.
    dst_path : str
        Path to the destination directory.
     plot_name : str or list of str
        Name for the exported plot.
    **kwargs : dict, optional
        Extra arguments for additional publish options.

    Other Parameters
    ----------------
    data_storage : str, optional
        Method how the data should be stored. Available options:
            centralized : The raw data will copied only once. All other plots
                will reference this data via sym link.
            individual [default]: The complete raw data will be copied to a
                folder for every plot, respectively.

    Returns
    -------
    None.

    """
    publish_container = PublishOptions(figs_and_ids, src_datapath, dst_path,
                                       plot_name, **kwargs)
    publish_container.validate_input()
    publish_container.export()
