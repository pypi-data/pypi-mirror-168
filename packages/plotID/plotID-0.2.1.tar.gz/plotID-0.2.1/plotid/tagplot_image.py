# -*- coding: utf-8 -*-
"""
Tag your picture with an ID.

Functions:
    tagplot_image(PlotOptions instance) -> list
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageOps
from plotid.create_id import create_id, create_qrcode
from plotid.plotoptions import PlotOptions, PlotIDTransfer


def tagplot_image(plotid_object):
    """
    Add IDs to images/pictures with pillow.

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

    # Check if figs is a list of files
    for img in plotid_object.figs:
        if not isinstance(img, str):
            raise TypeError('Name of the image is not a string.')
        if not os.path.isfile(img):
            raise TypeError('File does not exist.')
            # Check if figs is a valid file is done by pillow internally

    color = (128, 128, 128)  # grey
    font = ImageFont.load_default()

    for i, img in enumerate(plotid_object.figs):
        img_id = plotid_object.prefix + create_id(plotid_object.id_method)
        plotid_object.figure_ids.append(img_id)
        img = Image.open(img)

        img_txt = Image.new('L', font.getsize(img_id))
        draw_txt = ImageDraw.Draw(img_txt)
        draw_txt.text((0, 0), img_id, font=font, fill=255)
        txt = img_txt.rotate(plotid_object.rotation, expand=1)
        img.paste(ImageOps.colorize(txt, (0, 0, 0), color),
                  (int(img.width*plotid_object.position[0]),
                   int(img.height*(1-plotid_object.position[1]))), txt)

        if plotid_object.qrcode:
            qrcode = create_qrcode(img_id)
            qrcode.thumbnail((100, 100), Image.ANTIALIAS)
            img.paste(qrcode, box=(img.width-100, img.height-100))
        plotid_object.figs[i] = img

    figs_and_ids = PlotIDTransfer(plotid_object.figs, plotid_object.figure_ids)
    return figs_and_ids
