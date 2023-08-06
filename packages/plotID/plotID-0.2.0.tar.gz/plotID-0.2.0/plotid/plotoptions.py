#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contains the PlotOptions and PlotIDTransfer classes."""


class PlotOptions:
    """
    Container objects which include all plot options provided by plotid.

    Methods
    -------
    __init__
    validate_input : Check if input is correct type.

    Attributes
    ----------
    figs : figure object or list of figures
        Figures that will be tagged.
    figure_ids: str or list of str
        IDs that the figures are tagged with.
    rotation : int
        Rotation angle for the ID.
    position : tuple
        Relative position of the ID on the plot (x,y).
    **kwargs : dict, optional
        Extra arguments for additional plot options.

    Other Parameters
    ----------------
    prefix : str, optional
        Will be added as prefix to the ID.
    id_method : str, optional
        id_method for creating the ID. Create an ID by Unix time is referenced
        as 'time', create a random ID with id_method='random'.
        The default is 'time'.
    qrcode : bool, optional
        Experimental status. Print qrcode on exported plot. Default: False.
    """

    def __init__(self, figs, rotation, position, **kwargs):

        self.figs = figs
        self.figure_ids = kwargs.get('figure_ids', [])
        self.rotation = rotation
        self.position = position
        self.prefix = kwargs.get('prefix', '')
        self.id_method = kwargs.get('id_method', 'time')
        self.qrcode = kwargs.get('qrcode', False)

    def __str__(self):
        """Representation if an object of this class is printed."""
        return str(self.__class__) + ": " + str(self.__dict__)

    def validate_input(self):
        """
        Validate if input for PlotOptions is correct type.

        Raises
        ------
        TypeError
            TypeError is thrown if one of the attributes is not of correct
            type.

        Returns
        -------
        0, if all checks succeed.

        """
        # Input validation for figs is done in submodules tagplot_$engine.py
        if not isinstance(self.prefix, str):
            raise TypeError("Prefix is not a string.")

        if not isinstance(self.id_method, str):
            raise TypeError('The chosen id_method is not a string.')

        # Store figs in a list, even if it is only one.
        if not isinstance(self.figs, list):
            self.figs = [self.figs]

        return 0


class PlotIDTransfer:
    """
    Container to transfer objects from tagplot() to publish().

    Methods
    -------
    __init__
    validate_input : Check if input is correct type.

    Attributes
    ----------
    figs : figure object or list of figures
        Tagged figures.
    figure_ids: str or list of str
        IDs that the figures are tagged with.
    """

    def __init__(self, figs, figure_ids):
        self.figs = figs
        self.figure_ids = figure_ids

    def __str__(self):
        """Representation if an object of this class is printed."""
        return str(self.__class__) + ": " + str(self.__dict__)
