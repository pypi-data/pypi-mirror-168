# -*- coding: utf-8 -*-
"""
Tag your matplotlib plot with an ID.

Functions:
    tagplot_matplotlib(PlotOptions instance) -> list
"""

import matplotlib
import matplotlib.pyplot as plt
from PIL import Image
from plotid.create_id import create_id, create_qrcode
from plotid.plotoptions import PlotOptions, PlotIDTransfer


def tagplot_matplotlib(plotid_object):
    """
    Add IDs to figures with matplotlib.

    The ID is placed visual on the figure window and returned as string in a
    list together with the figures.

    Parameters
    ----------
    plotid_object : instance of PlotOptions

    Returns
    -------
    PlotIDTransfer object
    """
    # Check if plotid_object is a valid instance of PlotOptions
    if not isinstance(plotid_object, PlotOptions):
        raise TypeError('The given options container is not an instance'
                        'of PlotOptions.')

    # Check if figs is a list of valid figures
    for figure in plotid_object.figs:
        if not isinstance(figure, matplotlib.figure.Figure):
            raise TypeError('Figure is not a valid matplotlib-figure.')

    fontsize = 'small'
    color = 'grey'

    # Loop to create and position the IDs
    for fig in plotid_object.figs:
        fig_id = create_id(plotid_object.id_method)
        fig_id = plotid_object.prefix + fig_id
        plotid_object.figure_ids.append(fig_id)

        plt.figure(fig)
        plt.figtext(x=plotid_object.position[0], y=plotid_object.position[1],
                    s=fig_id, ha='left', wrap=True,
                    rotation=plotid_object.rotation,
                    fontsize=fontsize, color=color)

        if plotid_object.qrcode:
            qrcode = create_qrcode(fig_id)
            qrcode.thumbnail((100, 100), Image.ANTIALIAS)
            fig.figimage(qrcode, fig.bbox.xmax - 100, 0, cmap='bone')
            fig.tight_layout()

    figs_and_ids = PlotIDTransfer(plotid_object.figs, plotid_object.figure_ids)
    return figs_and_ids
