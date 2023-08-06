#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tag your plot with an ID.

For publishing the tagged plot along your research data have a look at the
module publish.

Functions:
    tagplot(figure object, string) -> list
"""

import warnings
from plotid.plotoptions import PlotOptions
from plotid.tagplot_matplotlib import tagplot_matplotlib
from plotid.tagplot_image import tagplot_image


def tagplot(figs, engine, location='east', **kwargs):
    """
    Tag your figure/plot with an ID.

    After determining the plot engine, tagplot calls the corresponding
    function which tags the plot.

    Parameters
    ----------
    figs : list
        Figures that should be tagged.
    engine : str
        Plot engine which should be used to tag the plot.
    location : str, optional
        Location for ID to be displayed on the plot. Default is 'east'.
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
    qcode : boolean, optional
        Experimental support for encoding the ID in a QR Code.

    Raises
    ------
    TypeError
        If specified location is not given as string.
    ValueError
        If an unsupported plot engine is given.

    Returns
    -------
    list
        The resulting list contains two lists each with as many entries as
        figures were given. The first list contains the tagged figures.
        The second list contains the corresponding IDs as strings.
    """
    if isinstance(location, str):
        pass
    else:
        raise TypeError("Location is not a string.")

    match location:
        case 'north':
            rotation = 0
            position = (0.35, 0.975)
        case 'east':
            rotation = 90
            position = (0.975, 0.35)
        case 'south':
            rotation = 0
            position = (0.35, 0.015)
        case 'west':
            rotation = 90
            position = (0.025, 0.35)
        case 'southeast':
            rotation = 0
            position = (0.75, 0.015)
        case 'custom':
            # TODO: Get rotation and position from user input & check if valid
            pass
        case _:
            warnings.warn(f'Location "{location}" is not a defined '
                          'location, TagPlot uses location "east" '
                          'instead.')
            rotation = 90
            position = (0.975, 0.35)

    option_container = PlotOptions(figs, rotation, position, **kwargs)
    option_container.validate_input()

    match engine:
        case 'matplotlib' | 'pyplot':
            return tagplot_matplotlib(option_container)
        case 'image' | 'fallback':
            return tagplot_image(option_container)
        case _:
            raise ValueError(
                f'The plot engine "{engine}" is not supported.')
